"""把 Wiki 的 Markdown 頁面打包成一個可瀏覽的網頁（發布成 Artifact 用）。

用法：python tools/build_wiki_viewer.py <輸出 html 路徑>
- Markdown 在建置時轉成 HTML（不依賴執行期函式庫）
- [[id]] 轉成頁內連結（#id），```mermaid 轉成 <pre class="mermaid">（由 Artifact 原生渲染）
- 輸出不含 <!doctype>/<html>/<head>/<body>（Artifact 發布時會自動包上）
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parents[2]
WIKI = ROOT / "Wiki"


def slug(page_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9-]", "-", page_id)


def split_front(text: str) -> tuple[dict, str]:
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1]) or {}, parts[2]
    return {}, text


def md_to_html(body: str, titles: dict[str, str]) -> str:
    mermaid_blocks: list[str] = []

    def keep_mermaid(m):
        mermaid_blocks.append(m.group(1))
        return f"\n\nMERMAIDBLOCK{len(mermaid_blocks) - 1}\n\n"

    body = re.sub(r"```mermaid\n(.*?)```", keep_mermaid, body, flags=re.S)

    def link(m):
        target = m.group(1).strip()
        label = m.group(2) or titles.get(target, target)
        return f'<a class="wl" href="#{slug(target)}">{html.escape(label)}</a>'

    body = re.sub(r"\[\[([^\]|#]+)(?:\|([^\]]+))?\]\]", link, body)
    out = markdown.markdown(body, extensions=["tables", "fenced_code", "sane_lists"])
    for i, blk in enumerate(mermaid_blocks):
        out = out.replace(f"<p>MERMAIDBLOCK{i}</p>", f'<pre class="mermaid">{html.escape(blk)}</pre>')
    # 原文引文：把 [Sxx p.N ...] "..." 標記成引文樣式
    out = re.sub(r'<li>\[(S\d{2}) (p\.\d+)([^\]]*)\] "(.+?)"</li>',
                 lambda m: f'<li class="q"><span class="qref"><a class="wl" href="#{m.group(1)}">{m.group(1)}</a> {m.group(2)}{html.escape(m.group(3))}</span>'
                           f'<q>{m.group(4)}</q></li>', out)
    return out


def meta_box(meta: dict, titles: dict[str, str]) -> str:
    rows = []

    def links(ids):
        return "、".join(f'<a class="wl" href="#{slug(i)}">{html.escape(titles.get(i, i))}</a>' for i in ids) or "—"

    if meta.get("type") == "source":
        rows.append(("原始網址", f'<a href="{html.escape(meta["url"])}" target="_blank" rel="noopener">{html.escape(meta["url"])}</a>'))
        rows.append(("發布者", html.escape(str(meta.get("publisher", "")))))
        rows.append(("年份", html.escape(str(meta.get("year", "")))))
        rows.append(("使用此來源的節點", links(meta.get("nodes") or [])))
    else:
        rows.append(("主題", html.escape(str(meta.get("topic", "")))))
        rows.append(("來源", links(meta.get("sources") or [])))
        rows.append(("先備概念", links(meta.get("prerequisites") or [])))
        rel = meta.get("relations") or []
        rows.append(("關聯", "、".join(f'<span class="rt">{html.escape(r["type"])}</span> <a class="wl" href="#{slug(r["target"])}">{html.escape(titles.get(r["target"], r["target"]))}</a>' for r in rel) or "—"))
        if meta.get("facts"):
            rows.append(("關鍵事實（與 facts.json 一致）", "<code>" + html.escape(json.dumps(meta["facts"], ensure_ascii=False)) + "</code>"))
    return '<dl class="meta">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + "</dl>"


def build() -> str:
    pages: list[dict] = []
    titles: dict[str, str] = {}
    # 總覽頁
    for pid, fname, title in (("knowledge-map", "knowledge_map.md", "知識地圖（索引）"),
                              ("sources-list", "sources.md", "資料來源清單"),
                              ("schema", "WIKI_SCHEMA.md", "Wiki 規範"),
                              ("log", "log.md", "Wiki 操作紀錄")):
        pages.append({"id": pid, "title": title, "group": "總覽", "meta": {}, "body": (WIKI / fname).read_text(encoding="utf-8")})
        titles[pid] = title
    titles["knowledge_map"], titles["sources"] = "知識地圖（索引）", "資料來源清單"
    topic_names = {"T1": "T1 Introduction", "T2": "T2 Classical", "T3": "T3 Symmetric", "T4": "T4 Modes", "T5": "T5 Asymmetric & Apps", "T6": "T6 基礎工具與教學法"}
    order = [n for b in json.loads((ROOT / "Workflow/config/batches.json").read_text(encoding="utf-8")) for n in b["nodes"]]
    concept_files = {p.stem: p for p in (WIKI / "concepts").glob("*.md")}
    for cid in order:
        meta, body = split_front(concept_files[cid].read_text(encoding="utf-8"))
        pages.append({"id": cid, "title": meta["title"], "group": topic_names[meta["topic"]], "meta": meta, "body": body})
        titles[cid] = meta["title"]
    for p in sorted((WIKI / "sources").glob("S*.md")):
        meta, body = split_front(p.read_text(encoding="utf-8"))
        pages.append({"id": meta["id"], "title": f'{meta["id"]} {meta["title"]}', "group": "來源頁", "meta": meta, "body": body})
        titles[meta["id"]] = f'{meta["id"]}'
    # 內容
    nav, arts = [], []
    groups: dict[str, list[dict]] = {}
    for pg in pages:
        groups.setdefault(pg["group"], []).append(pg)
    for g, items in groups.items():
        nav.append(f'<p class="ng">{html.escape(g)}</p><ul>' + "".join(
            f'<li><a href="#{slug(p["id"])}" data-target="{slug(p["id"])}">{html.escape(p["title"])}</a></li>' for p in items) + "</ul>")
    for i, pg in enumerate(pages):
        body = re.sub(r"^# .*\n", "", pg["body"].lstrip(), count=1)  # 頁面標題另外顯示
        arts.append(f'<article class="page{" on" if i == 0 else ""}" id="{slug(pg["id"])}"><p class="crumb">{html.escape(pg["group"])}</p>'
                    f'<h1>{html.escape(pg["title"])}</h1>'
                    + (meta_box(pg["meta"], titles) if pg["meta"] else "")
                    + md_to_html(body, titles) + "</article>")
    tpl = (Path(__file__).parent / "wiki_viewer_template.html").read_text(encoding="utf-8")
    return tpl.replace("{{NAV}}", "\n".join(nav)).replace("{{PAGES}}", "\n".join(arts)) \
              .replace("{{COUNT}}", str(len([p for p in pages if p["group"] not in ("總覽", "來源頁")])))


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.write_text(build(), encoding="utf-8")
    print("written", out, out.stat().st_size, "bytes")
