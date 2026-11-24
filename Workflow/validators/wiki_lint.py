"""Wiki Validation（LLM Wiki 的 Lint 操作）。

檢查項目（每項產生 error / warn；有任何 error 即未通過）：
  W1 資料取得：每篇來源 HTTP 200、有 SHA-256、成功抽取文字、預期關鍵字存在
  W2 來源頁：每篇來源有來源頁，標題／網址與設定一致，列出對應節點
  W3 知識覆蓋：已核准架構中的節點都存在；各主題必要術語都有出現
  W4 頁面格式：frontmatter 欄位、必要段落、至少一條引文、內文引用的來源已列在 sources
  W5 可追溯性：每條引文必須能在原文抽取文字的「所標頁碼」逐字找到
  W6 關聯完整：[[連結]] / relations / prerequisites 目標存在、關聯型別合法、無孤立頁、先備關係無循環
  W7 重複：重複 id / 標題、定義段落高度相似
  W8 矛盾：頁面 frontmatter 的 facts 與 facts.json 標準值一致；標準值本身有原文引文；
     常見誤解（misconception）不得出現在「常見誤解」段落以外
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from textnorm import LIGATURE_LOSS_THRESHOLD, ligature_loss_markers, squash  # noqa: E402

CITE_RE = re.compile(r'^- \[(S\d{2}) p\.(\d+)(?: ([^\]]+))?\] "(.+)"\s*$')
INLINE_RE = re.compile(r"\[(S\d{2})(?: p\.\d+)?[^\]]*\]")
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")


# ------------------------------------------------------------ page parsing
def parse_page(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError as e:
                meta = {"_yaml_error": str(e)}
            body = parts[2]
    sections: dict[str, str] = {}
    cur = "_intro"
    for line in body.splitlines():
        if line.startswith("## "):
            cur = line.strip()
            sections[cur] = ""
        else:
            sections[cur] = sections.get(cur, "") + line + "\n"
    return {"path": path, "meta": meta, "body": body, "sections": sections}


def load_pages(folder: Path) -> list[dict]:
    return [parse_page(p) for p in sorted(folder.glob("*.md"))] if folder.exists() else []


LOSSY: set[str] = set()  # 有 fi 連字遺失的來源 id（比對時摺疊 fi→f）


def load_source_pages(raw: Path) -> dict[str, dict[int, str]]:
    """raw/Sxx.extracted.txt → {source_id: {page: squashed_text}}"""
    out: dict[str, dict[int, str]] = {}
    LOSSY.clear()
    for f in sorted(raw.glob("S*.extracted.txt")):
        sid = f.name.split(".")[0]
        text = f.read_text(encoding="utf-8")
        fold = ligature_loss_markers(text) >= LIGATURE_LOSS_THRESHOLD
        if fold:
            LOSSY.add(sid)
        pages: dict[int, str] = {}
        cur, buf = None, []
        for line in text.splitlines():
            m = re.match(r"^=== \[page (\d+)\] ===$", line)
            if m:
                if cur is not None:
                    pages[cur] = squash("\n".join(buf), fold)
                cur, buf = int(m.group(1)), []
            else:
                buf.append(line)
        if cur is not None:
            pages[cur] = squash("\n".join(buf), fold)
        out[sid] = pages
    return out


def find_quote(pages: dict[int, str], page: int, quote: str, sid: str = "") -> tuple[bool, int | None]:
    q = squash(quote, sid in LOSSY)
    if q in pages.get(page, ""):
        return True, page
    # 引文跨頁：本頁 + 下一頁 / 上一頁 + 本頁
    for a, b in ((page, page + 1), (page - 1, page)):
        if a in pages and b in pages and q in pages[a] + pages[b]:
            return True, page
    for p, t in pages.items():
        if q in t:
            return False, p
    return False, None


def trigrams(s: str) -> set[str]:
    s = squash(s)
    return {s[i:i + 3] for i in range(max(0, len(s) - 2))}


# ------------------------------------------------------------------- lint
def run(root: Path) -> dict:
    wiki, wf = root / "Wiki", root / "Workflow"
    cfg = wf / "config"
    req = json.loads((cfg / "wiki_requirements.json").read_text(encoding="utf-8"))
    sources = json.loads((cfg / "sources.json").read_text(encoding="utf-8"))
    batches = json.loads((cfg / "batches.json").read_text(encoding="utf-8"))
    src_by_id = {s["id"]: s for s in sources}
    issues: list[dict] = []

    def add(check, sev, where, msg):
        issues.append({"check": check, "severity": sev, "where": where, "msg": msg})

    # W1 ---------------------------------------------------------------
    manifest = json.loads((wiki / "raw" / "manifest.json").read_text(encoding="utf-8")) \
        if (wiki / "raw" / "manifest.json").exists() else {}
    ingest = json.loads((wiki / "raw" / "ingest_report.json").read_text(encoding="utf-8")) \
        if (wiki / "raw" / "ingest_report.json").exists() else {}
    for s in sources:
        m, g = manifest.get(s["id"]), ingest.get(s["id"])
        if not m or m.get("status") != 200 or not m.get("sha256"):
            add("W1", "error", s["id"], f"來源未成功取得：{m}")
        if not g or not g.get("ok"):
            add("W1", "error", s["id"], f"文字抽取失敗或缺少預期關鍵字：{g}")
        elif g.get("near_empty_pages", 0) > 0.3 * g.get("pages", 1):
            add("W1", "warn", s["id"], f"{g['near_empty_pages']}/{g['pages']} 頁幾乎沒有文字（可能是掃描圖）")
    raw_pages = load_source_pages(wiki / "raw")

    # load pages ---------------------------------------------------------
    concepts = load_pages(wiki / "concepts")
    srcpages = load_pages(wiki / "sources")
    cids = [p["meta"].get("id") for p in concepts]
    sids_pages = {p["meta"].get("id"): p for p in srcpages}
    all_ids = set(cids) | set(sids_pages) | {"knowledge_map", "sources", "log"}

    # W2 ---------------------------------------------------------------
    for s in sources:
        sp = sids_pages.get(s["id"])
        if not sp:
            add("W2", "error", s["id"], "缺少來源頁 Wiki/sources/" + s["id"] + "-*.md")
            continue
        if sp["meta"].get("url") != s["url"]:
            add("W2", "error", s["id"], f"來源頁網址與設定不一致：{sp['meta'].get('url')}")
        if sp["meta"].get("title") != s["title"]:
            add("W2", "error", s["id"], f"來源頁標題與設定不一致：{sp['meta'].get('title')}")
        nodes = sp["meta"].get("nodes") or []
        if not nodes:
            add("W2", "error", s["id"], "來源頁未列出對應節點 nodes")
        for n in nodes:
            if n not in cids:
                add("W2", "error", s["id"], f"來源頁列出的節點不存在：{n}")
        for sec in ("## 摘要", "## 本 Wiki 使用的章節"):
            if sec not in sp["sections"]:
                add("W2", "error", s["id"], f"來源頁缺少段落 {sec}")

    # W3 ---------------------------------------------------------------
    expected_nodes = {n: b["topic"] for b in batches for n in b["nodes"]}
    for n, topic in expected_nodes.items():
        if n not in cids:
            add("W3", "error", n, f"已核准架構中的節點不存在（主題 {topic}）")
    for topic, terms in req["required_terms"].items():
        text = " ".join(p["body"] for p in concepts if p["meta"].get("topic") == topic).lower()
        for t in terms:
            if t.lower() not in text:
                add("W3", "error", topic, f"主題 {topic} 的頁面未涵蓋必要概念「{t}」")

    # W4 / W5 ----------------------------------------------------------
    for p in concepts:
        meta, where = p["meta"], p["path"].name
        if "_yaml_error" in meta:
            add("W4", "error", where, f"frontmatter YAML 錯誤：{meta['_yaml_error']}")
            continue
        for k in ("id", "title", "topic", "aliases", "sources", "prerequisites", "relations"):
            if k not in meta:
                add("W4", "error", where, f"frontmatter 缺少欄位 {k}")
        if meta.get("id") and p["path"].stem != meta["id"]:
            add("W4", "error", where, f"檔名與 id 不一致：{meta.get('id')}")
        if meta.get("topic") and expected_nodes.get(meta.get("id")) not in (None, meta["topic"]):
            add("W4", "error", where, f"topic 應為 {expected_nodes[meta['id']]}")
        for sec in req["required_sections"]:
            if sec not in p["sections"]:
                add("W4", "error", where, f"缺少段落 {sec}")
        declared = set(meta.get("sources") or [])
        cites = []
        for line in p["sections"].get("## 來源引文", "").splitlines():
            if line.strip().startswith("- "):
                m = CITE_RE.match(line.strip())
                if not m:
                    add("W4", "error", where, f"引文格式錯誤：{line.strip()[:80]}")
                else:
                    cites.append(m.groups())
        if not cites:
            add("W4", "error", where, "沒有任何原文引文（無法追溯）")
        cited_ids = {c[0] for c in cites}
        for sid in declared - cited_ids:
            add("W4", "error", where, f"frontmatter 列出來源 {sid}，但沒有該來源的引文")
        for sid in cited_ids - declared:
            add("W4", "error", where, f"引文來自 {sid}，但 frontmatter sources 未列出")
        body_wo_cites = "\n".join(v for k, v in p["sections"].items() if k != "## 來源引文")
        for sid in set(INLINE_RE.findall(body_wo_cites)):
            if sid not in declared:
                add("W4", "error", where, f"內文引用 [{sid}] 但 sources 未列出")
            if sid not in src_by_id:
                add("W4", "error", where, f"內文引用不存在的來源 {sid}")
        if not INLINE_RE.search(p["sections"].get("## 重點", "")):
            add("W4", "error", where, "「重點」段落沒有標註任何來源 [Sxx]")
        for sid, page, loc, quote in cites:
            if len(squash(quote)) < req["min_quote_chars"]:
                add("W5", "error", where, f"引文太短，無法有效比對：{quote}")
                continue
            if sid not in raw_pages:
                add("W5", "error", where, f"{sid} 沒有抽取文字，無法驗證引文")
                continue
            ok, found = find_quote(raw_pages[sid], int(page), quote, sid)
            if not ok:
                if found:
                    add("W5", "error", where, f"引文頁碼錯誤：[{sid} p.{page}] 實際在 p.{found}：{quote[:60]}")
                else:
                    add("W5", "error", where, f"引文在 {sid} 原文中找不到（可能是改寫或虛構）：{quote[:70]}")

    # W6 ---------------------------------------------------------------
    allowed = set(req["allowed_relation_types"])
    inbound: dict[str, int] = {c: 0 for c in cids}
    prereq: dict[str, list[str]] = {}
    for p in concepts:
        meta, where = p["meta"], p["path"].name
        for t in LINK_RE.findall(p["body"]):
            if t not in all_ids:
                add("W6", "error", where, f"連結目標不存在：[[{t}]]")
        for r in meta.get("relations") or []:
            if not isinstance(r, dict) or r.get("type") not in allowed:
                add("W6", "error", where, f"關聯型別不合法：{r}")
                continue
            if r.get("target") not in cids:
                add("W6", "error", where, f"關聯目標不存在：{r.get('target')}")
            else:
                inbound[r["target"]] += 1
        prereq[meta.get("id")] = list(meta.get("prerequisites") or [])
        for t in prereq[meta.get("id")]:
            if t not in cids:
                add("W6", "error", where, f"先備概念不存在：{t}")
    for p in srcpages:
        for t in LINK_RE.findall(p["body"]):
            if t not in all_ids:
                add("W6", "error", p["path"].name, f"連結目標不存在：[[{t}]]")
    kmap = (wiki / "knowledge_map.md").read_text(encoding="utf-8") if (wiki / "knowledge_map.md").exists() else ""
    if not kmap:
        add("W6", "error", "knowledge_map.md", "缺少知識地圖")
    elif "```mermaid" not in kmap:
        add("W6", "error", "knowledge_map.md", "知識地圖缺少 Mermaid 圖")
    kmap_links = set(LINK_RE.findall(kmap))
    for c in cids:
        if c not in kmap_links:
            add("W6", "error", "knowledge_map.md", f"索引未列出節點 [[{c}]]（孤立頁）")
        out_n = len(next(p for p in concepts if p["meta"].get("id") == c)["meta"].get("relations") or [])
        if out_n + inbound.get(c, 0) == 0:
            add("W6", "error", c, "節點沒有任何關聯（孤立節點）")
    for s in sources:
        if s["id"] not in kmap_links and f"[[{s['id']}" not in kmap:
            add("W6", "warn", "knowledge_map.md", f"索引未列出來源頁 {s['id']}")
    # 先備關係循環檢查
    state: dict[str, int] = {}

    def dfs(u, stack):
        state[u] = 1
        for v in prereq.get(u, []):
            if state.get(v) == 1:
                add("W6", "error", u, f"先備關係有循環：{' → '.join(stack + [u, v])}")
            elif state.get(v) is None and v in prereq:
                dfs(v, stack + [u])
        state[u] = 2
    for u in prereq:
        if state.get(u) is None:
            dfs(u, [])

    # W7 ---------------------------------------------------------------
    seen_ids, seen_titles = {}, {}
    for p in concepts:
        i, t = p["meta"].get("id"), p["meta"].get("title")
        if i in seen_ids:
            add("W7", "error", i, f"重複 id：{seen_ids[i]} 與 {p['path'].name}")
        seen_ids[i] = p["path"].name
        if t in seen_titles:
            add("W7", "error", i, f"重複標題：{t}")
        seen_titles[t] = i
    defs = [(p["meta"].get("id"), trigrams(p["sections"].get("## 定義", ""))) for p in concepts]
    for a in range(len(defs)):
        for b in range(a + 1, len(defs)):
            A, B = defs[a][1], defs[b][1]
            if not A or not B:
                continue
            j = len(A & B) / len(A | B)
            if j >= req["near_duplicate_error"]:
                add("W7", "error", f"{defs[a][0]} / {defs[b][0]}", f"定義高度重複（Jaccard={j:.2f}）")
            elif j >= req["near_duplicate_warn"]:
                add("W7", "warn", f"{defs[a][0]} / {defs[b][0]}", f"定義相似（Jaccard={j:.2f}），請確認沒有重複")

    # W8 ---------------------------------------------------------------
    facts_p = wiki / "facts.json"
    facts = json.loads(facts_p.read_text(encoding="utf-8")) if facts_p.exists() else None
    if facts is None:
        add("W8", "error", "facts.json", "缺少關鍵事實表（無法做矛盾檢查）")
        facts = {"facts": {}, "misconceptions": []}
    for k, f in facts.get("facts", {}).items():
        sid, page, quote = f.get("source"), f.get("page"), f.get("quote", "")
        if sid not in raw_pages:
            add("W8", "error", f"facts.{k}", f"事實的來源 {sid} 沒有抽取文字")
            continue
        ok, found = find_quote(raw_pages[sid], int(page or 0), quote, sid)
        if not ok:
            add("W8", "error", f"facts.{k}", f"事實標準值的引文無法在 {sid} p.{page} 找到"
                + (f"（實際在 p.{found}）" if found else ""))
    for p in concepts:
        for k, v in (p["meta"].get("facts") or {}).items():
            if k not in facts.get("facts", {}):
                add("W8", "error", p["meta"].get("id"), f"使用未登錄的事實 {k}（請先加入 facts.json 並附引文）")
            elif facts["facts"][k]["value"] != v:
                add("W8", "error", p["meta"].get("id"),
                    f"事實矛盾：{k}={v}，facts.json 為 {facts['facts'][k]['value']}")
    for mc in facts.get("misconceptions", []):
        rx = re.compile(mc["pattern"], re.I)
        for p in concepts:
            text = "\n".join(v for k, v in p["sections"].items() if k != "## 常見誤解")
            for line in text.splitlines():
                if rx.search(line):
                    add("W8", "error", p["meta"].get("id"),
                        f"出現常見誤解「{mc['id']}」（只能放在『常見誤解』段落說明）：{line.strip()[:80]}")

    # summary ----------------------------------------------------------
    n_err = sum(1 for i in issues if i["severity"] == "error")
    by_check: dict[str, dict[str, int]] = {}
    for c in ("W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8"):
        by_check[c] = {"error": sum(1 for i in issues if i["check"] == c and i["severity"] == "error"),
                       "warn": sum(1 for i in issues if i["check"] == c and i["severity"] == "warn")}
    n_quotes = sum(len([l for l in p["sections"].get("## 來源引文", "").splitlines() if CITE_RE.match(l.strip())])
                   for p in concepts)
    return {"passed": n_err == 0, "n_errors": n_err, "n_warnings": len(issues) - n_err,
            "by_check": by_check, "issues": issues,
            "stats": {"concept_pages": len(concepts), "source_pages": len(srcpages), "quotes": n_quotes,
                      "facts": len(facts.get("facts", {}))}}


def quick_lint(root: Path, node_ids: list[str]) -> dict:
    """v2：每個 batch 寫完就先檢查該 batch 頁面的格式（W4）與引文可追溯性（W5）。

    run-01 的引文跨頁錯誤要等 5 個 batch 全部寫完、跑 Wiki Validation 才發現；
    把這兩項檢查提前到每個 batch 之後，錯誤可以在剛寫完、記憶還新的時候修正。
    （W2/W3/W6 等全域檢查需要整個 Wiki 完成，仍留在 validate_wiki。）
    """
    res = run(root)
    files = {f"{n}.md" for n in node_ids}
    issues = [i for i in res["issues"] if i["check"] in ("W4", "W5") and i["where"] in files]
    n_err = sum(1 for i in issues if i["severity"] == "error")
    return {"passed": n_err == 0, "n_errors": n_err, "issues": issues, "nodes": node_ids}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    res = run(Path(__file__).resolve().parents[2])
    print(json.dumps({k: v for k, v in res.items() if k != "issues"}, ensure_ascii=False, indent=2))
    for i in res["issues"]:
        print(f"[{i['check']}][{i['severity']}] {i['where']}: {i['msg']}")
