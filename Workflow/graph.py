"""Cryptography LLM Wiki — LangGraph workflow (Loop / Graph).

真正可執行的 StateGraph：
  * 程式節點（自動）：fetch_sources, ingest_sources, validate_wiki, query_wiki,
    validate_content, test_html, done, halt
  * Agent 節點（LangGraph interrupt，暫停等待 Claude Code agent 完成後 resume）：
    organize_wiki, draft_content, build_html
  * 三個檢查節點各自有 conditional edge：通過 → 下一階段；失敗 → 回到生成節點；
    重試超過 MAX_RETRIES → halt（需人工介入）。
  * 狀態以 SQLite checkpoint 持久化，可跨程序暫停 / 繼續。
  * 所有節點的輸入、輸出、檢查結果、修正紀錄寫入 logs/events.jsonl，
    `python graph.py report` 轉成 execution_log.md。

用法：
  python graph.py start   --thread run-01
  python graph.py resume  --thread run-01 --note "agent 做了什麼"
  python graph.py status  --thread run-01
  python graph.py wiki-log --op ingest --msg "..."
  python graph.py report
  python graph.py mermaid
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sqlite3
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

sys.stdout.reconfigure(encoding="utf-8")

WF = Path(__file__).resolve().parent
ROOT = WF.parent
WIKI = ROOT / "Wiki"
RAW = WIKI / "raw"
SLIDES = ROOT / "Slides"
LOGS = WF / "logs"
ART = WF / "artifacts"
CFG = WF / "config"
EVENTS = LOGS / "events.jsonl"
DB = WF / "state" / "checkpoints.sqlite"
MAX_RETRIES = 3
UA = "Mozilla/5.0 (compatible; course-wiki-fetcher/1.0)"

sys.path.insert(0, str(WF))


# ----------------------------------------------------------------- helpers
def now() -> str:
    return dt.datetime.now().astimezone().isoformat(timespec="seconds")


def jload(p: Path, default=None):
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else default


def jsave(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def snapshot(base: Path, exclude: tuple[Path, ...] = ()) -> dict[str, str]:
    snap = {}
    if not base.exists():
        return snap
    for f in sorted(base.rglob("*")):
        if f.is_file() and not any(ex in f.parents for ex in exclude):
            snap[f.relative_to(ROOT).as_posix()] = sha256_file(f)[:12]
    return snap


def diff_snap(before: dict, after: dict) -> dict:
    return {
        "added": sorted(set(after) - set(before)),
        "modified": sorted(k for k in after if k in before and after[k] != before[k]),
        "removed": sorted(set(before) - set(after)),
    }


def log_event(run_id: str, node: str, *, attempt: int | None = None, input: Any = None,
              output: Any = None, check: Any = None, fix: Any = None, decision: str | None = None) -> None:
    EVENTS.parent.mkdir(parents=True, exist_ok=True)
    ev = {"ts": now(), "run": run_id, "node": node, "attempt": attempt, "input": input,
          "output": output, "check": check, "fix": fix, "decision": decision}
    with EVENTS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(ev, ensure_ascii=False) + "\n")


def wiki_log(op: str, msg: str) -> None:
    """Append to Wiki/log.md (LLM Wiki chronological log, append-only)."""
    p = WIKI / "log.md"
    if not p.exists():
        p.write_text("# Wiki Log（只追加，不修改）\n\n格式：`## [時間] 操作 | 說明`\n", encoding="utf-8")
    stamp = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    with p.open("a", encoding="utf-8") as fh:
        fh.write(f"\n## [{stamp}] {op} | {msg}\n")


def sources_cfg() -> list[dict]:
    return jload(CFG / "sources.json")


def batches_cfg() -> list[dict]:
    return jload(CFG / "batches.json")


# ------------------------------------------------------------------- state
class St(TypedDict, total=False):
    run_id: str
    fetch: dict
    ingest: dict
    wiki_batches_done: int
    batch_lint: dict
    batch_tries: dict
    retries: dict
    attempts: dict
    last: dict
    snaps: dict
    status: str


def _bump(d: dict | None, key: str) -> dict:
    d = dict(d or {})
    d[key] = d.get(key, 0) + 1
    return d


# ---------------------------------------------------------- program nodes
def fetch_sources(st: St) -> dict:
    RAW.mkdir(parents=True, exist_ok=True)
    manifest_p = RAW / "manifest.json"
    manifest = jload(manifest_p, {})
    results = {}
    for s in sources_cfg():
        path = RAW / f"{s['id']}.{s['format']}"
        prev = manifest.get(s["id"], {})
        if path.exists() and prev.get("sha256") == sha256_file(path):
            results[s["id"]] = {**prev, "cached": True}
            continue
        rec = {"url": s["url"], "file": path.name}
        for tries in range(1, 4):  # 網路層重試，最多 3 次
            try:
                req = urllib.request.Request(s["url"], headers={"User-Agent": UA})
                with urllib.request.urlopen(req, timeout=90) as r:
                    data = r.read()
                    rec.update(status=r.status, content_type=r.headers.get("Content-Type", ""))
                path.write_bytes(data)
                rec.update(bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                           fetched_at=now(), tries=tries, cached=False)
                rec.pop("error", None)
                break
            except Exception as e:  # noqa: BLE001
                rec.update(status="error", error=repr(e), tries=tries)
                time.sleep(2 * tries)
        if rec.get("status") != 200:
            # run-06 發現：Cloudflare 的機器人防護擋 Python urllib（403），同一個工具重試幾次都一樣。
            # 改用 curl 再試一次（不同的 HTTP 用戶端），並記錄使用了備援。
            import subprocess
            try:
                cp = subprocess.run(["curl", "-s", "-L", "--max-time", "90", "-A", UA, "-o", str(path),
                                     "-w", "%{http_code}", s["url"]], capture_output=True, text=True, timeout=120)
                if cp.stdout.strip() == "200" and path.exists() and path.stat().st_size > 0:
                    data = path.read_bytes()
                    rec.update(status=200, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                               fetched_at=now(), fallback="curl", urllib_error=rec.pop("error", None))
            except Exception as e:  # noqa: BLE001
                rec["fallback_error"] = repr(e)
        results[s["id"]] = rec
    manifest.update(results)
    jsave(manifest_p, manifest)
    ok_ids = [k for k, v in results.items() if v.get("status") == 200]
    bad = {k: v.get("error") for k, v in results.items() if v.get("status") != 200}
    log_event(st["run_id"], "fetch_sources",
              input={"sources": [s["id"] for s in sources_cfg()]},
              output={k: {kk: v.get(kk) for kk in ("status", "bytes", "sha256", "cached", "tries")}
                      for k, v in results.items()},
              check={"passed": not bad, "ok": len(ok_ids), "failed": bad})
    wiki_log("fetch", f"取得 {len(ok_ids)}/{len(results)} 篇來源" + (f"；失敗 {list(bad)}" if bad else ""))
    return {"fetch": {"ok": not bad, "ok_ids": ok_ids, "failed": bad}}


def _extract_pages(path: Path, fmt: str) -> list[tuple[int, str]]:
    if fmt == "pdf":
        from pypdf import PdfReader
        rd = PdfReader(str(path))
        return [(i + 1, p.extract_text() or "") for i, p in enumerate(rd.pages)]
    if fmt == "html":  # run-06：網頁來源，去掉 script/style 與標籤，整頁視為 p.1
        import html as _html
        import re as _re
        raw = path.read_text(encoding="utf-8", errors="replace")
        raw = _re.sub(r"(?is)<(script|style|noscript|svg|nav|footer|header)[^>]*>.*?</\1>", " ", raw)
        raw = _re.sub(r"(?i)<br\s*/?>|</(p|li|h[1-6]|div|tr)>", "\n", raw)
        text = _html.unescape(_re.sub(r"<[^>]+>", " ", raw))
        text = "\n".join(l.strip() for l in text.splitlines() if l.strip())
        return [(1, text)]
    txt = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    return [(i + 1, t) for i, t in enumerate(txt.split("\f"))]  # RFC 以 form feed 分頁


def ingest_sources(st: St) -> dict:
    from validators.textnorm import LIGATURE_LOSS_THRESHOLD, ligature_loss_markers, squash
    report = {}
    for s in sources_cfg():
        src = RAW / f"{s['id']}.{s['format']}"
        if not src.exists():
            report[s["id"]] = {"ok": False, "error": "file missing"}
            continue
        try:
            pages = _extract_pages(src, s["format"])
        except Exception as e:  # noqa: BLE001
            report[s["id"]] = {"ok": False, "error": repr(e)}
            continue
        out = RAW / f"{s['id']}.extracted.txt"
        with out.open("w", encoding="utf-8") as fh:
            for n, t in pages:
                fh.write(f"\n=== [page {n}] ===\n{t}\n")
        chars = sum(len(t) for _, t in pages)
        empty = sum(1 for _, t in pages if len(t.strip()) < 30)
        whole = squash(" ".join(t for _, t in pages))
        missing = [k for k in s.get("expect", []) if squash(k) not in whole]
        # v2（run-01 batch 3 發現 FIPS 197 的 fi 連字遺失後加入）：抽取品質檢查提前到 ingest
        lig = ligature_loss_markers(" ".join(t for _, t in pages))
        warnings = []
        if lig >= LIGATURE_LOSS_THRESHOLD:
            warnings.append(f"ligature-loss: {lig} 個 fi 連字遺失症狀字（如 specifed）；引文比對需摺疊 fi→f")
        report[s["id"]] = {"ok": chars > 2000 and not missing, "pages": len(pages), "chars": chars,
                           "near_empty_pages": empty, "expected_missing": missing,
                           "ligature_loss_markers": lig, "warnings": warnings,
                           "extracted": out.name}
    jsave(RAW / "ingest_report.json", report)
    bad = [k for k, v in report.items() if not v.get("ok")]
    warned = {k: v["warnings"] for k, v in report.items() if v.get("warnings")}
    log_event(st["run_id"], "ingest_sources",
              input={"files": [f"{s['id']}.{s['format']}" for s in sources_cfg()]},
              output=report, check={"passed": not bad, "failed": bad, "warnings": warned})
    wiki_log("ingest", f"抽取文字 {len(report) - len(bad)}/{len(report)} 篇" + (f"；失敗 {bad}" if bad else ""))
    render_sources_md()
    snaps = dict(st.get("snaps") or {})
    snaps["wiki"] = snapshot(WIKI, exclude=(RAW,))
    # v2：LLM Wiki 是持續累積的——已存在節點的 batch 不重建（增量模式）
    existing = {p.stem for p in (WIKI / "concepts").glob("*.md")}
    done_n = 0
    for b in batches_cfg():
        if all(n in existing for n in b["nodes"]):
            done_n += 1
        else:
            break
    return {"ingest": {"ok": not bad, "failed": bad, "warnings": warned}, "snaps": snaps,
            "retries": {"wiki": 0, "content": 0, "html": 0}, "attempts": {}, "last": {},
            "wiki_batches_done": done_n}


def render_sources_md() -> None:
    """sources.md 由程式依 config + manifest + 來源頁自動產生，避免手寫錯誤。"""
    manifest = jload(RAW / "manifest.json", {})
    ingest = jload(RAW / "ingest_report.json", {})
    node_map: dict[str, list[str]] = {}
    try:
        from validators.wiki_lint import load_pages
        for pg in load_pages(WIKI / "concepts"):
            for sid in pg["meta"].get("sources", []) or []:
                node_map.setdefault(sid, []).append(pg["meta"].get("id", "?"))
    except Exception:  # noqa: BLE001
        pass
    lines = ["# 資料來源清單（Sources）", "",
             "> 本檔由 `Workflow/graph.py` 依 `config/sources.json`、`raw/manifest.json`、"
             "`raw/ingest_report.json` 與概念頁自動產生。SHA-256 可用來確認 ingest 的是同一份檔案。", "",
             "| ID | 標題 | 作者／發布者 | 年份 | 網址 | 用途 | 取得狀態 | 抽取頁數 | SHA-256（前 16 碼） | 對應知識節點 |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for s in sources_cfg():
        m, g = manifest.get(s["id"], {}), ingest.get(s["id"], {})
        status = f"HTTP {m.get('status')}" if m else "未取得"
        nodes = ", ".join(f"[[{n}]]" for n in sorted(node_map.get(s["id"], []))) or "（待整理）"
        lines.append(f"| {s['id']} | {s['title']} | {s['author']} | {s['year']} | <{s['url']}> | "
                     f"{s['purpose']} | {status} | {g.get('pages', '-')} | `{(m.get('sha256') or '')[:16]}` | {nodes} |")
    lines += ["", "來源頁（每篇一頁的摘要與使用章節）：`Wiki/sources/`。原始檔與抽取文字在 `Wiki/raw/`（僅保留於本機，"
              "HAC 章節的授權僅允許個人保存，不公開散布）。", ""]
    fetched = [m.get("fetched_at") for m in manifest.values() if m.get("fetched_at")]
    if fetched:
        lines.append(f"取得時間：{min(fetched)} ～ {max(fetched)}")
    (WIKI / "sources.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_wiki(st: St) -> dict:
    from validators import wiki_lint
    res = wiki_lint.run(ROOT)
    attempts = _bump(st.get("attempts"), "wiki")
    n = attempts["wiki"]
    retries = dict(st.get("retries") or {})
    if res["passed"]:
        decision = "pass"
        render_sources_md()
    elif retries.get("wiki", 0) < MAX_RETRIES:
        decision = "retry"
        retries["wiki"] = retries.get("wiki", 0) + 1
    else:
        decision = "halt"
    res["decision"] = decision
    jsave(LOGS / f"wiki_validation_{st['run_id']}_{n}.json", res)
    log_event(st["run_id"], "validate_wiki", attempt=n,
              input={"pages": res["stats"]},
              check={"passed": res["passed"], "errors": res["n_errors"], "warnings": res["n_warnings"],
                     "by_check": res["by_check"], "issues": res["issues"][:80]},
              decision=decision)
    wiki_log("lint", f"第 {n} 次 Wiki Validation：{'通過' if res['passed'] else '未通過'}，"
             f"errors={res['n_errors']} warnings={res['n_warnings']} → {decision}")
    last = dict(st.get("last") or {})
    last["wiki"] = res
    return {"attempts": attempts, "retries": retries, "last": last}


def query_wiki(st: St) -> dict:
    from validators.query import run_queries
    res = run_queries(ROOT)
    jsave(ART / "query_results.json", res)
    empty = [q["slide"] for q in res["queries"] if q["needs_wiki"] and not q["hits"]]
    log_event(st["run_id"], "query_wiki",
              input={"queries": [{"slide": q["slide"], "terms": q["terms"]} for q in res["queries"]]},
              output={q["slide"]: [h["id"] for h in q["hits"]] for q in res["queries"]},
              check={"passed": not empty, "slides_without_hits": empty})
    wiki_log("query", f"為 {len(res['queries'])} 張投影片查詢 Wiki；無結果：{empty or '無'}")
    snaps = dict(st.get("snaps") or {})
    snaps["content"] = snapshot(ART)
    return {"snaps": snaps}


def validate_content(st: St) -> dict:
    from validators import content_check
    res = content_check.run(ROOT)
    attempts = _bump(st.get("attempts"), "content")
    n = attempts["content"]
    retries = dict(st.get("retries") or {})
    if res["passed"]:
        decision = "pass"
    elif retries.get("content", 0) < MAX_RETRIES:
        decision = "retry"
        retries["content"] = retries.get("content", 0) + 1
    else:
        decision = "halt"
    res["decision"] = decision
    jsave(LOGS / f"content_validation_{st['run_id']}_{n}.json", res)
    log_event(st["run_id"], "validate_content", attempt=n, input=res.get("stats"),
              check={"passed": res["passed"], "errors": res["n_errors"], "warnings": res["n_warnings"],
                     "by_check": res["by_check"], "issues": res["issues"][:80]},
              decision=decision)
    last = dict(st.get("last") or {})
    last["content"] = res
    snaps = dict(st.get("snaps") or {})
    snaps["html"] = snapshot(SLIDES)
    return {"attempts": attempts, "retries": retries, "last": last, "snaps": snaps}


def test_html(st: St) -> dict:
    from validators import html_test
    attempts = _bump(st.get("attempts"), "html")
    n = attempts["html"]
    res = html_test.run(ROOT, tag=f"{st['run_id']}_{n}")
    retries = dict(st.get("retries") or {})
    if res["passed"]:
        decision = "pass"
    elif retries.get("html", 0) < MAX_RETRIES:
        decision = "retry"
        retries["html"] = retries.get("html", 0) + 1
    else:
        decision = "halt"
    res["decision"] = decision
    jsave(LOGS / f"html_test_{st['run_id']}_{n}.json", res)
    log_event(st["run_id"], "test_html", attempt=n, input=res.get("stats"),
              check={"passed": res["passed"], "errors": res["n_errors"], "warnings": res["n_warnings"],
                     "by_check": res["by_check"], "issues": res["issues"][:80]},
              decision=decision)
    last = dict(st.get("last") or {})
    last["html"] = res
    return {"attempts": attempts, "retries": retries, "last": last}


def done(st: St) -> dict:
    log_event(st["run_id"], "done", output={"attempts": st.get("attempts"), "retries": st.get("retries")})
    render_execution_log()
    return {"status": "done"}


def halt(st: St) -> dict:
    log_event(st["run_id"], "halt", output={"attempts": st.get("attempts"), "retries": st.get("retries")},
              decision="needs-human")
    render_execution_log()
    return {"status": "halted: retries exhausted, needs human"}


# ------------------------------------------------------------ agent nodes
def _agent_node(st: St, node: str, stage: str, base: Path, exclude=(), task: str = "",
                extra: dict | None = None) -> tuple[Any, dict]:
    last = (st.get("last") or {}).get(stage) or {}
    issues = [i for i in last.get("issues", []) if i.get("severity") == "error"]
    retry_no = (st.get("retries") or {}).get(stage, 0)
    payload = {"node": node, "task": task, "retry": retry_no,
               "issues_to_fix": issues[:60], **(extra or {})}
    resume = interrupt(payload)  # ← 暫停，等待 agent 完成後 resume
    after = snapshot(base, exclude=exclude)
    before = (st.get("snaps") or {}).get(stage, {})
    changes = diff_snap(before, after)
    log_event(st["run_id"], node, attempt=retry_no,
              input={"issues_from_last_validation": len(issues), **(extra or {})},
              output={"changed_files": changes}, fix=resume)
    snaps = dict(st.get("snaps") or {})
    snaps[stage] = after
    return resume, {"snaps": snaps}


def organize_wiki(st: St) -> dict:
    done_n = st.get("wiki_batches_done", 0)
    batches = batches_cfg()
    building = done_n < len(batches)
    validated = bool((st.get("last") or {}).get("wiki"))
    if building:
        extra = {"mode": "build", "batch": batches[done_n],
                 "batch_lint_issues": (st.get("batch_lint") or {}).get("issues", [])[:30]}
        task = "依 batch 整理 Wiki 頁面（先與使用者討論重點）"
    elif validated:
        extra, task = {"mode": "fix"}, "依 Wiki Validation 的錯誤修正 Wiki"
    else:  # v2：Wiki 已存在（LLM Wiki 是持續累積的），只需檢查是否要更新
        extra, task = {"mode": "incremental"}, "Wiki 已存在：檢查新 ingest 結果是否需要更新頁面"
    resume, upd = _agent_node(st, "organize_wiki", "wiki", WIKI, exclude=(RAW,), task=task, extra=extra)
    note = resume.get("note") if isinstance(resume, dict) else str(resume)
    if building:
        b = batches[done_n]
        # v2：每個 batch 寫完立即做 W4/W5 快速檢查（檢查提前），失敗就留在同一個 batch 修正
        from validators.wiki_lint import quick_lint
        ql = quick_lint(ROOT, b["nodes"])
        tries = dict(st.get("batch_tries") or {})
        key = str(b["batch"])
        tries[key] = tries.get(key, 0) + 1
        log_event(st["run_id"], "batch_lint", attempt=tries[key], input={"batch": b["batch"], "nodes": b["nodes"]},
                  check={"passed": ql["passed"], "errors": ql["n_errors"], "warnings": 0, "by_check": {},
                         "issues": ql["issues"]},
                  decision="next-batch" if ql["passed"] or tries[key] > MAX_RETRIES else "redo-batch")
        wiki_log("organize", f"batch {b['batch']} {b['name']}：{note}（batch lint：{'通過' if ql['passed'] else str(ql['n_errors']) + ' errors'}）")
        upd["batch_lint"] = ql
        upd["batch_tries"] = tries
        if ql["passed"] or tries[key] > MAX_RETRIES:
            upd["wiki_batches_done"] = done_n + 1
    else:
        wiki_log("organize", f"{extra['mode']}（retry {(st.get('retries') or {}).get('wiki', 0)}）：{note}")
    return upd


def draft_content(st: St) -> dict:
    _, upd = _agent_node(st, "draft_content", "content", ART,
                         task="以 query_results 為依據撰寫 artifacts/slide_content.json")
    return upd


def build_html(st: St) -> dict:
    _, upd = _agent_node(st, "build_html", "html", SLIDES,
                         task="依 slide_content.json 產生 Slides/index.html")
    return upd


# ------------------------------------------------------------------ routes
def route_after_organize(st: St) -> str:
    return "organize_wiki" if st.get("wiki_batches_done", 0) < len(batches_cfg()) else "validate_wiki"


def _route(stage: str, nxt: str, back: str):
    def r(st: St) -> str:
        d = ((st.get("last") or {}).get(stage) or {}).get("decision")
        return {"pass": nxt, "retry": back}.get(d, "halt")
    r.__name__ = f"route_{stage}"
    return r


def build_graph():
    g = StateGraph(St)
    for name, fn in [("fetch_sources", fetch_sources), ("ingest_sources", ingest_sources),
                     ("organize_wiki", organize_wiki), ("validate_wiki", validate_wiki),
                     ("query_wiki", query_wiki), ("draft_content", draft_content),
                     ("validate_content", validate_content), ("build_html", build_html),
                     ("test_html", test_html), ("done", done), ("halt", halt)]:
        g.add_node(name, fn)
    g.add_edge(START, "fetch_sources")
    g.add_edge("fetch_sources", "ingest_sources")
    g.add_edge("ingest_sources", "organize_wiki")
    g.add_conditional_edges("organize_wiki", route_after_organize,
                            {"organize_wiki": "organize_wiki", "validate_wiki": "validate_wiki"})
    g.add_conditional_edges("validate_wiki", _route("wiki", "query_wiki", "organize_wiki"),
                            {"query_wiki": "query_wiki", "organize_wiki": "organize_wiki", "halt": "halt"})
    g.add_edge("query_wiki", "draft_content")
    g.add_edge("draft_content", "validate_content")
    g.add_conditional_edges("validate_content", _route("content", "build_html", "draft_content"),
                            {"build_html": "build_html", "draft_content": "draft_content", "halt": "halt"})
    g.add_edge("build_html", "test_html")
    g.add_conditional_edges("test_html", _route("html", "done", "build_html"),
                            {"done": "done", "build_html": "build_html", "halt": "halt"})
    g.add_edge("done", END)
    g.add_edge("halt", END)
    return g


def compiled():
    DB.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB), check_same_thread=False)
    return build_graph().compile(checkpointer=SqliteSaver(conn))


# ------------------------------------------------------------------ report
def render_execution_log() -> None:
    from validators.report import render
    render(ROOT)


def _print_result(app, cfg, res) -> None:
    state = app.get_state(cfg)
    if res and "__interrupt__" in res:
        intr = res["__interrupt__"][0].value
        log_event(state.values.get("run_id", "?"), "graph", output={"paused_at": list(state.next),
                                                                     "payload_task": intr.get("task")})
        print(f"⏸  PAUSED at {state.next} — {intr.get('task')}")
        print(json.dumps({k: v for k, v in intr.items() if k != 'issues_to_fix'}, ensure_ascii=False, indent=2))
        if intr.get("issues_to_fix"):
            print(f"issues_to_fix ({len(intr['issues_to_fix'])}):")
            for i in intr["issues_to_fix"]:
                print(f"  - [{i.get('check')}] {i.get('where', '')}: {i.get('msg')}")
    else:
        print(f"■ FINISHED — status={state.values.get('status')}")
    print(f"retries={state.values.get('retries')} attempts={state.values.get('attempts')}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["start", "resume", "status", "report", "mermaid", "wiki-log", "sources-md", "note"])
    ap.add_argument("--thread", default="run-01")
    ap.add_argument("--note", default="")
    ap.add_argument("--op", default="note")
    ap.add_argument("--msg", default="")
    a = ap.parse_args()
    if a.cmd == "report":
        render_execution_log(); print("execution_log.md rendered"); return
    if a.cmd == "sources-md":
        render_sources_md(); print("sources.md rendered"); return
    if a.cmd == "wiki-log":
        wiki_log(a.op, a.msg); print("logged"); return
    if a.cmd == "note":  # Graph 之外的人工／agent 檢查（例如看截圖），同樣寫進事件紀錄
        log_event(a.thread, a.op, fix={"note": a.msg}); print("noted"); return
    if a.cmd == "mermaid":
        print(build_graph().compile().get_graph().draw_mermaid()); return
    app = compiled()
    cfg = {"configurable": {"thread_id": a.thread}}
    if a.cmd == "start":
        log_event(a.thread, "graph", output={"event": "start"})
        res = app.invoke({"run_id": a.thread}, cfg)
    elif a.cmd == "resume":
        res = app.invoke(Command(resume={"note": a.note, "ts": now()}), cfg)
    else:
        st = app.get_state(cfg)
        print("next:", st.next)
        print(json.dumps({k: v for k, v in st.values.items() if k not in ("last", "snaps")},
                         ensure_ascii=False, indent=2))
        return
    _print_result(app, cfg, res)


if __name__ == "__main__":
    main()
