"""query_wiki 節點：依 slide_outline.json 的關鍵詞檢索 Wiki 概念頁（LLM Wiki 的 Query 操作）。

做法（可重現、不靠 LLM）：
  * 標題或別名（aliases）含關鍵詞：+5 分
  * 內文出現關鍵詞：每次 +1，最多 +3
  * 分數 ≥ 4 的頁面依分數排序，最多取 5 個
輸出每個命中頁的定義、重點、範例、常見誤解與來源，作為 draft_content 的唯一知識依據。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wiki_lint import load_pages  # noqa: E402

MIN_SCORE, TOP_K = 4, 5


def _section(p: dict, name: str) -> str:
    return p["sections"].get(name, "").strip()


def run_queries(root: Path) -> dict:
    outline = json.loads((root / "Workflow" / "config" / "slide_outline.json").read_text(encoding="utf-8"))
    pages = load_pages(root / "Wiki" / "concepts")
    out = []
    for s in outline["slides"]:
        scored = []
        for p in pages:
            m = p["meta"]
            names = [str(m.get("title", ""))] + [str(a) for a in (m.get("aliases") or [])]
            body = p["body"].lower()
            score, why = 0, []
            for t in s["terms"]:
                tl = t.lower()
                if any(tl in n.lower() for n in names):
                    score += 5
                    why.append(f"title/alias:{t}")
                c = min(3, body.count(tl))
                if c:
                    score += c
                    why.append(f"body:{t}×{c}")
            if score >= MIN_SCORE:
                scored.append((score, p, why))
        scored.sort(key=lambda x: -x[0])
        hits = []
        for score, p, why in scored[:TOP_K]:
            m = p["meta"]
            hits.append({"id": m["id"], "title": m["title"], "score": score, "why": why,
                         "sources": m.get("sources", []), "prerequisites": m.get("prerequisites", []),
                         "definition": _section(p, "## 定義"),
                         "key_points": _section(p, "## 重點"),
                         "example": _section(p, "## 範例"),
                         "misconceptions": _section(p, "## 常見誤解")})
        out.append({"slide": s["no"], "id": s["id"], "title": s["title"], "terms": s["terms"],
                    "needs_wiki": s["needs_wiki"], "hits": hits})
    # 人可讀版本
    md = ["# Query Results（query_wiki 節點輸出）", "",
          "> 由 `validators/query.py` 自動產生：每張投影片用大綱中的關鍵詞檢索 Wiki，列出命中的節點與分數。",
          "> draft_content 只能使用這裡列出的節點。", ""]
    for q in out:
        md.append(f"## Slide {q['slide']}：{q['title']}")
        md.append(f"- 關鍵詞：{', '.join(q['terms']) or '（不需要）'}")
        if not q["hits"]:
            md.append("- 命中：無" + ("（⚠ 需要 Wiki 依據卻沒有結果）" if q["needs_wiki"] else ""))
        for h in q["hits"]:
            md.append(f"- **{h['id']}**（{h['title']}）score={h['score']}；來源 {', '.join(h['sources'])}；依據 {'; '.join(h['why'])}")
        md.append("")
    (root / "Workflow" / "artifacts").mkdir(parents=True, exist_ok=True)
    (root / "Workflow" / "artifacts" / "query_results.md").write_text("\n".join(md), encoding="utf-8")
    return {"queries": out}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    r = run_queries(Path(__file__).resolve().parents[2])
    for q in r["queries"]:
        print(q["slide"], q["title"], [(h["id"], h["score"]) for h in q["hits"]])
