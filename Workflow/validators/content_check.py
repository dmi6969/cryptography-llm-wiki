"""Content Validation：檢查 artifacts/slide_content.json（教學內容）。

slide_content.json 格式：
{
  "deck_title": "...",
  "slides": [
    {"no": 1, "id": "cover", "title": "...", "subtitle": "...", "points": [], "sources": []},
    {"no": 2, "id": "why", "title": "...", "lead": "一句話重點",
     "points": [{"text": "...", "nodes": ["intro-what-is-crypto"], "cite": ["S02 p.5"]}],
     "visual": {"type": "...", ...},          # 給 HTML 用的圖示／範例描述
     "sources": ["S02", "S01"]}
  ],
  "examples": {"caesar": {...}, "rsa": {...}, "dh": {...}}
}

檢查項目：
  C1 結構：10–12 張、編號連續、第一張封面、最後一張總結、標題不重複、非封面頁都有重點與來源
  C2 Wiki 依據：每個重點都標註節點；節點存在；節點出現在 query_wiki 對該頁的檢索結果中；
     cite 的來源必須屬於所標節點的來源；投影片 sources 必須是所標節點來源的子集，且涵蓋所有 cite
  C3 技術正確：數值與 facts.json 一致（AES 輪數、區塊大小、金鑰長度、RSA 金鑰長度）；常見誤解不得出現
  C4 範例重算：Caesar、RSA、Diffie–Hellman 範例由程式重新計算
  C5 教學順序：節點的先備概念必須在同頁或更早的投影片出現
  C6 文字負擔：每頁 ≤ 4 個重點（總結頁 ≤ 5）、每點 ≤ 60 字、每頁重點總字數 ≤ 200
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from textnorm import cjk_len  # noqa: E402
from wiki_lint import load_pages  # noqa: E402

MAX_POINTS, MAX_POINTS_SUMMARY, MAX_POINT_LEN, MAX_SLIDE_LEN = 4, 5, 60, 200


def _all_text(slide: dict) -> list[str]:
    out = [slide.get("title", ""), slide.get("lead", ""), slide.get("subtitle", "")]
    out += [d.get("text", "") for d in slide.get("defines", [])]
    for f in slide.get("formulas", []):
        out.append(f.get("expr", ""))
        out += [s[1] for s in f.get("symbols", [])]
    out += [p["text"] for p in slide.get("points", [])]
    v = slide.get("visual") or {}
    for k in ("name", "caption", "items", "rows", "labels", "steps"):
        x = v.get(k)
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, list):
            out += [json.dumps(i, ensure_ascii=False) if not isinstance(i, str) else i for i in x]
    return [t for t in out if t]


def run(root: Path) -> dict:
    wf, wiki = root / "Workflow", root / "Wiki"
    issues: list[dict] = []

    def add(check, sev, where, msg):
        issues.append({"check": check, "severity": sev, "where": where, "msg": msg})

    p = wf / "artifacts" / "slide_content.json"
    if not p.exists():
        add("C1", "error", "slide_content.json", "找不到教學內容檔")
        return _summary(issues, {})
    try:
        deck = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        add("C1", "error", "slide_content.json", f"JSON 格式錯誤：{e}")
        return _summary(issues, {})
    slides = deck.get("slides", [])
    pages = {pg["meta"]["id"]: pg for pg in load_pages(wiki / "concepts")}
    facts = json.loads((wiki / "facts.json").read_text(encoding="utf-8"))
    sources_cfg = {s["id"] for s in json.loads((wf / "config" / "sources.json").read_text(encoding="utf-8"))}
    q = json.loads((wf / "artifacts" / "query_results.json").read_text(encoding="utf-8")) \
        if (wf / "artifacts" / "query_results.json").exists() else {"queries": []}
    hits_by_slide = {x["slide"]: {h["id"] for h in x["hits"]} for x in q["queries"]}

    outline = json.loads((wf / "config" / "slide_outline.json").read_text(encoding="utf-8"))
    lo, hi = outline.get("slide_count", [10, 12])
    NO_TEXT = {"cover", "references"}

    # C1 -------------------------------------------------------------------
    if not lo <= len(slides) <= hi:
        add("C1", "error", "deck", f"投影片數量 {len(slides)}，需要 {lo}–{hi} 張")
    for i, s in enumerate(slides, 1):
        if s.get("no") != i:
            add("C1", "error", f"slide {i}", f"編號不連續（no={s.get('no')}）")
    if slides and slides[0].get("id") != "cover":
        add("C1", "error", "slide 1", "第一張必須是封面")
    # run-07（使用者回饋：來源不用每頁都有）：最後一張是統一的參考資料，倒數第二張是總結
    if slides and slides[-1].get("id") != "references":
        add("C1", "error", f"slide {len(slides)}", "最後一張必須是參考資料")
    if len(slides) > 1 and slides[-2].get("id") != "summary":
        add("C1", "error", f"slide {len(slides) - 1}", "倒數第二張必須是總結")
    titles = [s.get("title") for s in slides]
    for t in {t for t in titles if titles.count(t) > 1}:
        add("C1", "error", "deck", f"標題重複：{t}")
    for s in slides:
        w = f"slide {s.get('no')}"
        if not s.get("title"):
            add("C1", "error", w, "缺少標題")
        if s.get("id") not in NO_TEXT:
            if not s.get("points"):
                add("C1", "error", w, "沒有重點")
            if not s.get("sources"):
                add("C1", "error", w, "沒有標示來源")

    # C2 -------------------------------------------------------------------
    for s in slides:
        if s.get("id") in NO_TEXT:
            continue
        w = f"slide {s['no']}"
        node_srcs: set[str] = set()
        cited: set[str] = set()
        for k, pt in enumerate(s.get("points", []), 1):
            nodes = pt.get("nodes") or []
            if not nodes:
                add("C2", "error", f"{w} 重點{k}", f"沒有標註 Wiki 節點：{pt.get('text', '')[:40]}")
            pt_srcs: set[str] = set()
            for n in nodes:
                if n not in pages:
                    add("C2", "error", f"{w} 重點{k}", f"節點不存在：{n}")
                    continue
                pt_srcs |= set(pages[n]["meta"].get("sources") or [])
                if n not in hits_by_slide.get(s["no"], set()) and s["id"] != "summary":
                    add("C2", "error", f"{w} 重點{k}", f"節點 {n} 不在 query_wiki 對本頁的檢索結果中（內容未經查詢取得）")
            node_srcs |= pt_srcs
            for c in pt.get("cite") or []:
                sid = c.split()[0]
                cited.add(sid)
                if sid not in pt_srcs:
                    add("C2", "error", f"{w} 重點{k}", f"引用 {c}，但所標節點 {nodes} 的來源中沒有 {sid}")
            if not pt.get("cite"):
                add("C2", "warn", f"{w} 重點{k}", "沒有標註頁碼引用（cite）")
        for sid in s.get("sources") or []:
            if sid not in sources_cfg:
                add("C2", "error", w, f"來源 {sid} 不存在")
            elif sid not in node_srcs:
                add("C2", "error", w, f"投影片列出來源 {sid}，但本頁節點的 Wiki 來源中沒有它")
        for sid in cited - set(s.get("sources") or []):
            add("C2", "error", w, f"重點引用了 {sid}，但投影片來源欄沒有列出")

    # C3 -------------------------------------------------------------------
    F = facts["facts"]
    for s in slides:
        w = f"slide {s.get('no')}"
        for t in _all_text(s):
            if "AES" in t:
                rounds_map = F["aes.rounds"]["value"]
                # run-04：「第 1 輪」是序數（第幾輪），不是輪數，排除以免誤判
                for m in re.finditer(r"(?<!第)(?<!第 )(\d+)\s*輪", t):
                    if int(m.group(1)) not in set(rounds_map.values()):
                        add("C3", "error", w, f"AES 輪數 {m.group(1)} 與 FIPS 197 不符：{t[:50]}")
                # v2（selftest 發現的漏洞）：「AES-128 做 12 輪」的 12 是合法值，但版本對錯了 → 逐一比對版本與輪數
                mv = re.search(r"AES-(\d{3})((?:\s*[／/、]\s*\d{3})*)", t)
                mr = re.search(r"(?<!第)(?<!第 )((?:\d+\s*[／/、]\s*)*\d+)\s*輪", t)
                if mv and mr:
                    variants = [mv.group(1)] + re.findall(r"\d{3}", mv.group(2))
                    rounds = [int(x) for x in re.findall(r"\d+", mr.group(1))]
                    if len(variants) == len(rounds):
                        for v, r in zip(variants, rounds):
                            want = rounds_map.get(f"AES-{v}")
                            if want is not None and want != r:
                                add("C3", "error", w, f"AES-{v} 應為 {want} 輪，內容寫 {r} 輪：{t[:50]}")
                for m in re.finditer(r"區塊[^，。；]{0,8}?(\d+)\s*(位元|bits?)", t):
                    if int(m.group(1)) != F["aes.block_bits"]["value"]:
                        add("C3", "error", w, f"AES 區塊大小 {m.group(1)} 與 FIPS 197 不符：{t[:50]}")
            if "RSA" in t:
                for m in re.finditer(r"(\d{3,5})\s*(位元|bits?)", t):
                    v = int(m.group(1))
                    if v in (512, 768, 1024):
                        add("C3", "error", w, f"RSA {v} 位元已低於 NIST 112 位元強度要求：{t[:50]}")
            for mc in facts.get("misconceptions", []):
                if re.search(mc["pattern"], t, re.I):
                    add("C3", "error", w, f"出現常見誤解「{mc['id']}」：{t[:60]}")
        for k, pt in enumerate(s.get("points", []), 1):
            for fk, fv in (pt.get("facts") or {}).items():
                if fk not in F:
                    add("C3", "error", f"{w} 重點{k}", f"使用未登錄事實 {fk}")
                elif F[fk]["value"] != fv:
                    add("C3", "error", f"{w} 重點{k}", f"事實 {fk}={fv} 與 facts.json（{F[fk]['value']}）不符")

    # C4 -------------------------------------------------------------------
    ex = deck.get("examples", {})
    c = ex.get("caesar")
    if c:
        enc = "".join(chr((ord(ch) - 65 + c["shift"]) % 26 + 65) if ch.isalpha() else ch for ch in c["plain"].upper())
        if enc != c["cipher"]:
            add("C4", "error", "examples.caesar", f"Caesar 範例錯誤：{c['plain']} 位移 {c['shift']} 應為 {enc}，內容寫 {c['cipher']}")
    else:
        add("C4", "error", "examples", "缺少 Caesar 範例")
    r = ex.get("rsa")
    if r:
        n, phi = r["p"] * r["q"], (r["p"] - 1) * (r["q"] - 1)
        if n != r["n"]:
            add("C4", "error", "examples.rsa", f"n 應為 {n}")
        if phi != r.get("phi", phi):
            add("C4", "error", "examples.rsa", f"(p−1)(q−1) 應為 {phi}")
        if (r["e"] * r["d"]) % phi != 1:
            add("C4", "error", "examples.rsa", "e·d mod (p−1)(q−1) ≠ 1")
        if pow(r["m"], r["e"], n) != r["c"]:
            add("C4", "error", "examples.rsa", f"加密結果應為 {pow(r['m'], r['e'], n)}，內容寫 {r['c']}")
        if pow(r["c"], r["d"], n) != r["m"]:
            add("C4", "error", "examples.rsa", "解密無法還原明文")
        rf = F["rsa.example"]["value"]
        if any(r.get(k) != rf[k] for k in ("p", "q", "n", "d", "e")):
            add("C4", "error", "examples.rsa", "RSA 範例與 Wiki（RSA 原始論文 §VIII）不一致")
    else:
        add("C4", "error", "examples", "缺少 RSA 範例")
    a = ex.get("aes")
    if a:  # run-04：AES 一輪四步實例，由獨立參考實作重算每個矩陣（含解密方向）
        import aes_ref
        if a.get("input") != F.get("aes.example_input", {}).get("value") or a.get("key") != F.get("aes.example_key", {}).get("value"):
            add("C4", "error", "examples.aes", "AES 範例的輸入或金鑰與 Wiki（FIPS 197 附錄 B）不一致")
        ref = aes_ref.round1_frames(a["input"], a["key"])
        for fr in a.get("frames", []):
            if fr["id"] not in ref:
                add("C4", "error", "examples.aes", f"未知的步驟 {fr['id']}")
                continue
            want = aes_ref.rows_hex(ref[fr["id"]])
            if [r.lower() for r in fr["rows"]] != want:
                add("C4", "error", "examples.aes", f"步驟「{fr['label']}」的 state 應為 {' / '.join(want)}")
        if not any(fr["id"].startswith("dec_") for fr in a.get("frames", [])):
            add("C4", "warn", "examples.aes", "AES 範例沒有示範解密方向")
    d = ex.get("dh")
    if d:
        ya, yb = pow(d["alpha"], d["xa"], d["q"]), pow(d["alpha"], d["xb"], d["q"])
        ka, kb = pow(yb, d["xa"], d["q"]), pow(ya, d["xb"], d["q"])
        if (ya, yb) != (d["ya"], d["yb"]):
            add("C4", "error", "examples.dh", f"公開值應為 Y_A={ya}, Y_B={yb}")
        if not (ka == kb == d["k"]):
            add("C4", "error", "examples.dh", f"共享金鑰應為 {ka}/{kb}，內容寫 {d['k']}")

    # C5 -------------------------------------------------------------------
    first_seen: dict[str, int] = {}
    for s in slides:
        for pt in s.get("points", []):
            for n in pt.get("nodes") or []:
                first_seen.setdefault(n, s["no"])
    for s in slides:
        if s.get("id") == "summary":
            continue
        for pt in s.get("points", []):
            for n in pt.get("nodes") or []:
                if n not in pages:
                    continue
                for pre in pages[n]["meta"].get("prerequisites") or []:
                    fs = first_seen.get(pre)
                    if fs is None:
                        add("C5", "warn", f"slide {s['no']}", f"{n} 的先備概念 {pre} 沒有在簡報中出現")
                    elif fs > s["no"]:
                        add("C5", "error", f"slide {s['no']}",
                            f"教學順序錯誤：{n} 需要先懂 {pre}，但 {pre} 到第 {fs} 張才出現")

    # C7–C10（run-07 依使用者回饋新增）----------------------------------------
    _extra_checks(slides, outline, wf, add, NO_TEXT)

    # C6 -------------------------------------------------------------------
    for s in slides:
        if s.get("id") in NO_TEXT:
            continue
        if len(s.get("defines", [])) > 5:
            add("C6", "error", f"slide {s['no']}", f"名詞小卡 {len(s['defines'])} 張，超過 5 張")
        for d in s.get("defines", []):
            if cjk_len(d.get("text", "")) > 45:
                add("C6", "error", f"slide {s['no']}", f"名詞「{d['term']}」的解釋超過 45 字")
        w = f"slide {s['no']}"
        pts = s.get("points", [])
        lim = MAX_POINTS_SUMMARY if s.get("id") == "summary" else MAX_POINTS
        if len(pts) > lim:
            add("C6", "error", w, f"重點 {len(pts)} 個，超過上限 {lim}（文字堆積）")
        total = 0
        for k, pt in enumerate(pts, 1):
            L = cjk_len(pt["text"])
            total += L
            if L > MAX_POINT_LEN:
                add("C6", "error", f"{w} 重點{k}", f"字數 {L} > {MAX_POINT_LEN}：{pt['text'][:30]}…")
        if total > MAX_SLIDE_LEN:
            add("C6", "error", w, f"重點總字數 {total} > {MAX_SLIDE_LEN}")

    stats = {"slides": len(slides), "points": sum(len(s.get("points", [])) for s in slides),
             "nodes_used": len(first_seen), "wiki_nodes": len(pages)}
    return _summary(issues, stats)


FORMULA_HINT = re.compile(r"[A-Za-zα-ω][₀-₉ⱼ]?\s*=\s*[^，。；]*(mod|\^|⊕|×|E_K|D_K)")
VAR_RE = re.compile(r"(?<![A-Za-z_])([A-Za-zα-ω](?:[₀-₉ⱼ]|_[A-Za-z])?)(?![A-Za-z])")
SOURCEY = re.compile(r"依.{0,12}(繪|畫|改)|引自|取自|改繪|重算|來源|根據|附錄|§|S\d{2}")


def _slide_text(s: dict) -> str:
    return " ｜ ".join(_all_text(s) + [p["text"] for p in s.get("points", [])])


def _extra_checks(slides, outline, wf, add, NO_TEXT):
    glossary = json.loads((wf / "config" / "glossary.json").read_text(encoding="utf-8"))["terms"]
    defined: set[str] = set()
    skip = NO_TEXT | {"roadmap"}
    for s in slides:
        w = f"slide {s['no']}"
        here = {d["term"] for d in s.get("defines", [])}
        for d in s.get("defines", []):
            if not d.get("text"):
                add("C7", "error", w, f"名詞「{d['term']}」沒有解釋文字")
        if s.get("id") not in skip:
            text = _slide_text(s)
            # C7 名詞先解釋：第一次出現的那一張或更早，必須解釋過
            for g in glossary:
                if g["term"] in defined or g["term"] in here:
                    continue
                if re.search(g["pattern"], text):
                    add("C7", "error", w, f"名詞「{g['term']}」第一次出現，但之前和這一張都沒有解釋")
            # C8 公式符號：出現公式就要逐一說明符號
            syms = {k for f in s.get("formulas", []) for k, _ in f.get("symbols", [])}
            for f in s.get("formulas", []):
                # run-08（使用者回饋：公式要用正常的數學排版）：每個公式都要有 LaTeX，且能轉成 MathML
                if not f.get("tex"):
                    add("C8", "error", w, f"公式 {f['expr']} 沒有數學排版（缺 tex）")
                else:
                    try:
                        from latex2mathml.converter import convert as _tex2mml
                        _tex2mml(f["tex"])
                    except Exception as ex:  # noqa: BLE001
                        add("C8", "error", w, f"公式 {f['expr']} 的 LaTeX 無法轉換：{ex}")
                for v in set(VAR_RE.findall(f.get("expr", ""))):
                    if v not in syms:
                        add("C8", "error", w, f"公式 {f['expr']} 的符號「{v}」沒有說明")
                if "mod" in f.get("expr", "") and "mod" not in syms and "mod" not in defined | here:
                    add("C8", "error", w, f"公式 {f['expr']} 用到 mod，但沒有說明")
            for line in [p["text"] for p in s.get("points", [])] + [s.get("lead", "")]:
                if FORMULA_HINT.search(line) and not s.get("formulas"):
                    add("C8", "error", w, f"出現公式但這一張沒有符號說明：{line[:40]}")
        defined |= here
        # C9 圖片名稱：要有名稱，且不寫來源或製作方式
        v = s.get("visual")
        if v:
            if not v.get("name"):
                add("C9", "error", w, "圖片沒有名稱")
            for k in ("name", "caption"):
                if v.get(k) and SOURCEY.search(v[k]):
                    add("C9", "error", w, f"圖片{('名稱' if k == 'name' else '說明')}不需要寫來源或製作方式：{v[k][:40]}")
    # C10 主題來龍去脈：每章要包含指定的角色
    roles_by_ch: dict[str, set] = {}
    for s in slides:
        roles_by_ch.setdefault(s.get("chapter", ""), set()).update(s.get("role", []))
    for ch in outline.get("chapters", []):
        missing = [r for r in ch.get("required_roles", []) if r not in roles_by_ch.get(ch["id"], set())]
        if missing:
            add("C10", "error", ch["id"], f"「{ch['name']}」缺少：{'、'.join(missing)}")
        # run-09（使用者回饋：章與章切換要提醒）：要求轉場的章，第一張必須是承上啟下頁
        if "承上啟下" in ch.get("required_roles", []):
            first = next((s for s in slides if s.get("chapter") == ch["id"]), None)
            if first and "承上啟下" not in first.get("role", []):
                add("C10", "error", ch["id"], f"「{ch['name']}」第一張應該是承上啟下的轉場頁")
            elif first and (not first.get("preview") or not first.get("lead")):
                add("C10", "error", ch["id"], f"「{ch['name']}」的轉場頁需要新問題（lead）與本章預告（preview）")


def _summary(issues: list[dict], stats: dict) -> dict:
    n_err = sum(1 for i in issues if i["severity"] == "error")
    by = {c: {"error": sum(1 for i in issues if i["check"] == c and i["severity"] == "error"),
              "warn": sum(1 for i in issues if i["check"] == c and i["severity"] == "warn")}
          for c in ("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10")}
    return {"passed": n_err == 0, "n_errors": n_err, "n_warnings": len(issues) - n_err,
            "by_check": by, "issues": issues, "stats": stats}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    res = run(Path(__file__).resolve().parents[2])
    print(json.dumps({k: v for k, v in res.items() if k != "issues"}, ensure_ascii=False, indent=2))
    for i in res["issues"]:
        print(f"[{i['check']}][{i['severity']}] {i['where']}: {i['msg']}")
