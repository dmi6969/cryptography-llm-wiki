"""build_html 用的產生器（run-07 起）：slide_content.json ＋ visuals.html ＋ slides_shell.html → Slides/index.html。

- 投影片上的每段文字（標題、重點、名詞小卡、公式符號表、圖名）都直接取自已通過 Content Validation 的內容檔，
  不在 HTML 裡另外手打，避免內容和畫面不一致。
- 每張圖的 HTML 放在 visuals.html 的 <template id="v-<slide id>">。
- 參考資料頁由 config/sources.json 產生（使用者回饋：來源不用每頁都有，統一放最後）。
用法：python tools/render_slides.py
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

WF = Path(__file__).resolve().parents[1]
ROOT = WF.parent
TOOLS = WF / "tools"
SHELL = TOOLS / "slides_shell.html"

EXTRA_CSS = """
/* ---------- run-07：名詞小卡、公式符號表、圖名、參考資料 ---------- */
.textcol { display: flex; flex-direction: column; gap: 10px; min-width: 0; }
.textcol .points { gap: 9px; }
.slide-inner { gap: 10px; }
.rightcol { display: flex; flex-direction: column; gap: 12px; min-width: 0; }
.points li { font-size: 16.5px; line-height: 1.5; }
.defs { border-radius: 12px; background: var(--key-soft); padding: 8px 12px; }
.defs-h, .fx-h { margin: 0 0 4px; font-family: var(--font-mono); font-size: 11.5px; letter-spacing: .08em; color: var(--key); text-transform: uppercase; }
.defs dl, .syms { margin: 0; display: grid; grid-template-columns: max-content minmax(0, 1fr); gap: 2px 12px; font-size: 13.5px; line-height: 1.45; }
.defs dt { font-weight: 700; color: var(--ink); }
.defs dd, .syms dd { margin: 0; color: var(--muted); min-width: 0; }
.formula { border-radius: 12px; border: 1px solid var(--line); background: var(--surface); padding: 8px 12px; }
.formula .fx-h { color: var(--accent); }
.fx { margin: 0 0 4px; font-family: var(--font-mono); font-size: 15px; font-weight: 600; color: var(--accent); overflow-wrap: anywhere; }
.syms dt { font-family: var(--font-mono); font-weight: 700; color: var(--ink); }
/* run-08：MathML 數學排版 */
math { font-family: "Cambria Math", "STIX Two Math", "Latin Modern Math", math, serif; }
.fx { font-family: var(--font-body); color: var(--accent); overflow-x: auto; }
.fx math[display="block"] { margin: 2px 0 6px; font-size: 1.22em; text-align: left; math-style: normal; }
.syms dt math { font-size: 1.12em; }
sub, sup { font-size: .72em; line-height: 0; }
.figname { font-size: 13.5px; color: var(--ink); font-weight: 600; text-align: center; }
.vt { margin: 0; font-size: 13px; font-weight: 700; color: var(--muted); }
.vt.dec { color: var(--ok); }
.vnote { margin: 0; font-size: 13px; color: var(--muted); }
.mono { font-family: var(--font-mono); }
.road { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap: 10px; }
.road li { padding: 12px; border-radius: 12px; border: 1px solid var(--line); background: var(--surface); font-weight: 600; display: flex; gap: 10px; align-items: center; }
.road b { display: grid; place-items: center; width: 28px; height: 28px; border-radius: 50%; background: var(--accent-soft); color: var(--accent); font-family: var(--font-mono); flex: none; }
.road-note { margin: 0; font-size: 14px; color: var(--muted); text-align: center; }
.goal { grid-template-columns: 40px minmax(0,1fr); }
.goal svg { grid-row: span 2; }
.ks { display: flex; flex-direction: column; gap: 12px; }
.ks-row { display: grid; grid-template-columns: 7.5em minmax(0, 1fr); gap: 4px 10px; align-items: center; font-size: 14px; }
.ks-bar { height: 14px; border-radius: 7px; background: var(--bg); overflow: hidden; border: 1px solid var(--line); }
.ks-bar i { display: block; height: 100%; background: var(--accent); }
.ks-v { grid-column: 2; font-size: 13px; color: var(--muted); }
.lockbox { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.pill { padding: 6px 14px; border-radius: 999px; font-weight: 700; font-size: 14px; }
.pill.pub { background: var(--accent-soft); color: var(--accent); }
.pill.key { background: var(--key-soft); color: var(--key); }
.tools { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; align-items: start; }
.clock-wrap, .tools > div { display: flex; flex-direction: column; gap: 8px; align-items: center; }
.clock { position: relative; width: 130px; height: 130px; border-radius: 50%; border: 2px solid var(--line); }
.clock span { position: absolute; left: 50%; top: 50%; width: 26px; height: 26px; margin: -13px 0 0 -13px; display: grid; place-items: center; border-radius: 50%; background: var(--bg); font-family: var(--font-mono); font-size: 13px;
  transform: rotate(calc(var(--i) * 51.43deg)) translateY(-50px) rotate(calc(var(--i) * -51.43deg)); }
.clock span.hit { background: var(--key-soft); color: var(--key); font-weight: 700; outline: 1.5px solid var(--key); }
.xor { border-collapse: collapse; font-family: var(--font-mono); font-size: 16px; }
.xor th, .xor td { width: 42px; height: 36px; text-align: center; border: 1px solid var(--line); }
.xor th { color: var(--muted); background: var(--bg); }
.xor td.one { background: var(--accent-soft); color: var(--accent); font-weight: 700; }
.sub-wrap { overflow-x: auto; }
.subst, .vig { border-collapse: collapse; font-family: var(--font-mono); font-size: 13px; width: 100%; }
.subst th, .vig th { font-family: var(--font-body); font-size: 12px; color: var(--muted); font-weight: 500; padding: 3px 6px; text-align: left; white-space: nowrap; }
.subst td, .vig td { text-align: center; padding: 3px 1px; border-bottom: 1px solid var(--line); }
.subst tr:nth-child(2) td, .subst tr:nth-child(4) td, .vig tr:last-child td { color: var(--accent); }
.vig tr.k td { color: var(--key); font-size: 12px; }
.subst td.h, .vig td.h { background: var(--key-soft); font-weight: 700; }
.vig td.h2 { background: var(--accent-soft); font-weight: 700; }
.tp { display: flex; flex-direction: column; gap: 6px; font-family: var(--font-mono); }
.tp-row { display: grid; grid-template-columns: 4.5em repeat(6, minmax(0, 1fr)); gap: 6px; text-align: center; font-size: 17px; }
.tp-row .tp-h { font-family: var(--font-body); font-size: 12.5px; color: var(--muted); text-align: left; align-self: center; }
.tp-row span:not(.tp-h) { padding: 6px 0; border-radius: 6px; background: var(--bg); }
.tp-row.k span:not(.tp-h) { background: var(--key-soft); color: var(--key); font-size: 14px; }
.tp-row.ct span:not(.tp-h) { color: var(--accent); background: var(--accent-soft); }
.tp-row .h { outline: 1.5px solid var(--key); }
.break { display: flex; flex-direction: column; gap: 10px; }
.bk { display: grid; grid-template-columns: 6em minmax(0,1fr); gap: 2px 12px; padding: 10px 12px; border-radius: 10px; border: 1px solid var(--line); background: var(--surface); font-size: 14px; }
.bk b { grid-row: span 2; align-self: center; }
.bk em { font-style: normal; color: var(--warn); }
.pc { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; font-size: 14px; }
.pro, .con { padding: 8px 10px; border-radius: 8px; }
.pro { background: var(--accent-soft); color: var(--accent); }
.con { background: var(--warn-soft); color: var(--warn); }
.bs { display: flex; flex-direction: column; gap: 6px; }
.bs-row { display: flex; gap: 8px; justify-content: center; flex-wrap: wrap; font-family: var(--font-mono); font-size: 14px; }
.bs-row.arrows { color: var(--muted); font-size: 12px; gap: 30px; }
.blkc { padding: 6px 12px; border-radius: 8px; border: 1px solid var(--line); background: var(--surface); letter-spacing: .12em; }
.blkc.ct { color: var(--accent); border-color: var(--accent); }
.bs-row.st span { padding: 4px 8px; border-radius: 6px; background: var(--key-soft); color: var(--key); }
.bytes { display: flex; flex-direction: column; gap: 8px; align-items: center; }
.bitrow { display: flex; gap: 4px; font-family: var(--font-mono); font-size: 18px; }
.bitrow span { width: 30px; height: 34px; display: grid; place-items: center; border-radius: 6px; background: var(--accent-soft); color: var(--accent); font-weight: 600; }
.bitrow span.sep { width: 8px; background: none; }
.bitlab { display: flex; gap: 18px; font-size: 12.5px; color: var(--muted); flex-wrap: wrap; justify-content: center; }
.bigx { margin: 0; font-size: 20px; font-weight: 700; }
.by-grid { display: grid; grid-template-columns: repeat(4, 24px); gap: 3px; }
.by-grid i { display: block; height: 24px; border-radius: 4px; background: var(--accent-soft); border: 1px solid var(--line); }
.tl3 { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; text-align: center; font-size: 14px; }
.tl3 li { padding: 8px; border-radius: 8px; background: var(--bg); }
.tl3 b { display: block; font-family: var(--font-mono); color: var(--accent); }
.s4 { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.s4c { display: flex; flex-direction: column; gap: 4px; padding: 10px 12px; border-radius: 10px; border: 1px solid var(--line); background: var(--surface); font-size: 14px; }
.s4c .mono { color: var(--accent); font-size: 13px; }
.s4c small { color: var(--muted); }
.s4c.key { border-color: var(--key); background: var(--key-soft); }
.dir { display: flex; flex-direction: column; gap: 8px; }
.dir-row { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; font-family: var(--font-mono); font-size: 13px; }
.dir-row span { padding: 5px 9px; border-radius: 8px; border: 1px solid var(--line); background: var(--surface); }
.dir-row span.key { border-color: var(--key); background: var(--key-soft); color: var(--key); }
.dir-row.dec span:not(.key) { border-color: var(--ok); color: var(--ok); }
.dir-row i { font-style: normal; color: var(--muted); }
.canvases.two { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.canvases.one { grid-template-columns: minmax(0, 60%); justify-content: center; }
.chain.three { grid-template-columns: minmax(0,1fr) auto minmax(0,1fr) auto minmax(0,1fr); }
.gcm { margin-top: 4px; padding: 10px 12px; border-radius: 10px; border: 1px dashed var(--ok); font-size: 14px; display: flex; flex-wrap: wrap; gap: 6px 10px; align-items: center; }
.tagbox { padding: 2px 8px; border-radius: 6px; background: var(--ok); color: var(--surface); font-size: 12.5px; }
.mb { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.mbc { display: flex; flex-direction: column; gap: 6px; align-items: center; text-align: center; padding: 16px 12px; border-radius: 12px; border: 1px solid var(--line); background: var(--surface); font-size: 14px; }
.mbc svg { width: 40px; height: 40px; fill: none; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
.mbc.pub svg { stroke: var(--accent); } .mbc.key svg { stroke: var(--key); }
.mbc.pub b { color: var(--accent); } .mbc.key b { color: var(--key); }
.rk { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 6px; }
.rk li { display: grid; grid-template-columns: 4em minmax(0,1fr); gap: 10px; padding: 7px 12px; border-radius: 8px; border: 1px solid var(--line); background: var(--surface); font-size: 14px; }
.rk li.key { border-color: var(--key); } .rk li.pub { border-color: var(--accent); }
.rkey { margin: 0; display: flex; gap: 14px; justify-content: center; flex-wrap: wrap; font-family: var(--font-mono); }
.sig { display: grid; grid-template-columns: minmax(0,1fr) auto minmax(0,1fr); gap: 10px; align-items: center; }
.okv { color: var(--ok); font-weight: 700; }
.refs { list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 6px 22px; font-size: 13px; line-height: 1.45; }
.refs li { display: grid; grid-template-columns: 2.6em minmax(0, 1fr); gap: 6px; }
.refs .sid { font-family: var(--font-mono); font-weight: 700; color: var(--accent); }
.refs a { color: var(--ink); text-decoration: none; border-bottom: 1px dotted var(--muted); overflow-wrap: anywhere; }
.refs small { color: var(--muted); }
.slide-body.single { grid-template-columns: 1fr; }
/* run-09：轉場頁 */
.divider .slide-inner { justify-content: center; }
.divider .slide-body { flex: none; }
.divider .slide-inner { gap: 22px; }
.divider h2 { display: flex; align-items: center; gap: 14px; font-size: clamp(26px, 3vw, 38px); }
.chno { display: grid; place-items: center; width: 52px; height: 52px; border-radius: 14px; background: var(--accent); color: var(--surface); font-family: var(--font-mono); font-size: 26px; flex: none; }
.div3 { grid-template-columns: minmax(0, 1fr) minmax(0, 1.15fr) minmax(0, .9fr); gap: 18px; align-items: start; }
.div3 > div { border-radius: 14px; padding: 14px 16px; display: flex; flex-direction: column; gap: 8px; min-width: 0; }
.recap { background: var(--surface); border: 1px solid var(--line); }
.recap .points li { font-size: 15px; }
.turn { background: var(--accent-soft); border: 1px solid var(--accent); }
.turn .q { margin: 0; font-family: var(--font-display); font-size: 20px; font-weight: 600; line-height: 1.5; color: var(--ink); }
.next { background: var(--surface); border: 1px dashed var(--line); }
.next ol { margin: 0; padding-left: 1.3em; display: flex; flex-direction: column; gap: 6px; font-size: 15px; }
.dh { margin: 0; font-family: var(--font-mono); font-size: 12px; letter-spacing: .08em; color: var(--muted); text-transform: uppercase; }
.turn .dh { color: var(--accent); font-weight: 700; }
.chain2 { display: flex; flex-direction: column; gap: 7px; }
.c2 { display: grid; grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr); gap: 8px; align-items: center; font-size: 14px; }
.c2 .pb { padding: 7px 10px; border-radius: 8px; background: var(--warn-soft); color: var(--warn); }
.c2 .sol { padding: 7px 10px; border-radius: 8px; background: var(--accent-soft); color: var(--accent); font-weight: 600; }
.c2 i { font-style: normal; color: var(--muted); }
.c2 small { display: block; font-weight: 400; color: var(--muted); font-size: 12px; }
@media (max-width: 860px) {
  .tools, .mb, .pc, .s4, .road { grid-template-columns: 1fr; }
  .refs { grid-template-columns: 1fr; }
  .div3 { grid-template-columns: 1fr; }
  .c2 { grid-template-columns: 1fr; }
  .sig { grid-template-columns: 1fr; }
}
"""


def make_shell() -> str:
    """第一次執行時，從 run-05 版的 index.html 取出外殼（樣式、控制列、互動程式）存成 slides_shell.html。"""
    if SHELL.exists():
        return SHELL.read_text(encoding="utf-8")
    src = (ROOT / "Slides" / "index.html").read_text(encoding="utf-8")
    head, rest = src.split('<main class="deck" id="deck">', 1)
    _, tail = rest.split("</main>", 1)
    tail = re.sub(r"const AES = \{.*?\};\n", "const AES = /*AES_DATA*/null;\n", tail, count=1, flags=re.S)
    tail = tail.replace('<span id="counter" aria-live="polite">1 / 12</span>', '<span id="counter" aria-live="polite">1 / {{N}}</span>')
    head = head.replace("</style>", EXTRA_CSS + "</style>", 1)
    shell = head + '<main class="deck" id="deck">\n{{SLIDES}}\n</main>' + tail
    SHELL.write_text(shell, encoding="utf-8")
    return shell


def e(s) -> str:
    return html.escape(str(s), quote=True)


def render() -> Path:
    shell = make_shell()
    deck = json.loads((WF / "artifacts" / "slide_content.json").read_text(encoding="utf-8"))
    outline = json.loads((WF / "config" / "slide_outline.json").read_text(encoding="utf-8"))
    sources = json.loads((WF / "config" / "sources.json").read_text(encoding="utf-8"))
    chapters = {c["id"]: c["name"] for c in outline["chapters"]}
    tpl = dict(re.findall(r'<template id="v-([\w-]+)">(.*?)</template>', (TOOLS / "visuals.html").read_text(encoding="utf-8"), re.S))
    slides = deck["slides"]
    out = []
    for i, s in enumerate(slides):
        ch = chapters.get(s.get("chapter", ""), "")
        cls = "slide active" if i == 0 else "slide"
        if s["id"] == "cover":
            route = "".join(f'<li><span class="n">{k}</span>{e(c["name"].split("·")[-1].strip())}</li>'
                            for k, c in enumerate([c for c in outline["chapters"] if c["id"].startswith("ch")], 1))
            out.append(f'''<section class="{cls} cover" data-topic="Cryptography 101" aria-label="第 1 張：封面">
  <div class="slide-inner">
    <p class="eyebrow">Cryptography 101 · 給初學者的入門</p>
    <h1>Cryptography <span>101</span></h1>
    <p class="subtitle">{e(s["subtitle"])}</p>
    <p class="lead">{e(s["lead"])}</p>
    <div class="cipher-strip" aria-label="HELLO 每個字母往後移 3 位變成 KHOOR"><span class="box">HELLO</span><span class="op">— 每個字母往後移 3 位 →</span><span class="box ct">KHOOR</span></div>
    <ol class="route" aria-label="課程路線">{route}</ol>
  </div>
</section>''')
            continue
        if s["id"] == "references":
            items = "".join(f'<li><span class="sid">{e(x["id"])}</span><span><a href="{e(x["url"])}" target="_blank" rel="noopener">{e(x["title"])}</a><br><small>{e(x["author"])}，{e(x["year"])}</small></span></li>' for x in sources)
            out.append(f'''<section class="{cls}" data-topic="{e(ch)}" aria-label="第 {i + 1} 張：{e(s["title"])}">
  <div class="slide-inner">
    <header class="slide-head"><p class="eyebrow">{e(ch)}</p><h2>{e(s["title"])}</h2>
      <p class="lead">本簡報的內容都整理自以下 {len(sources)} 份資料（NIST 標準、IETF RFC、大學教材、原始論文與入門教材）</p></header>
    <div class="slide-body single"><ol class="refs">{items}</ol></div>
  </div>
</section>''')
            continue
        if "承上啟下" in s.get("role", []):  # run-09：章與章之間的轉場頁（回顧 → 新問題 → 預告）
            pts = "".join(f"<li>{e(p['text'])}</li>" for p in s.get("points", []))
            prev = "".join(f"<li>{e(x)}</li>" for x in s.get("preview", []))
            card = "".join(f'<div class="defs"><p class="defs-h">名詞小卡</p><dl><dt>{e(d["term"])}</dt><dd>{e(d["text"])}</dd></dl></div>' for d in s.get("defines", []))
            num = re.search(r"\d+", ch).group(0) if re.search(r"\d+", ch) else ""
            out.append(f'''<section class="{cls} divider" data-topic="{e(ch)}" aria-label="第 {i + 1} 張：{e(s["title"])}">
  <div class="slide-inner">
    <header class="slide-head"><p class="eyebrow">{e(ch)}</p><h2><span class="chno">{num}</span>{e(s["title"])}</h2></header>
    <div class="slide-body div3">
      <div class="recap"><p class="dh">剛剛學到</p><ul class="points">{pts}</ul></div>
      <div class="turn"><p class="dh">但是……</p><p class="q">{e(s["lead"])}</p>{card}</div>
      <div class="next" data-glossary-skip><p class="dh">這一章會看到</p><ol>{prev}</ol></div>
    </div>
  </div>
</section>''')
            continue
        pts = "".join(f"<li>{e(p['text'])}</li>" for p in s.get("points", []))
        left = [f'<ul class="points">{pts}</ul>']
        if s.get("defines"):
            dl = "".join(f"<dt>{e(d['term'])}</dt><dd>{e(d['text'])}</dd>" for d in s["defines"])
            left.append(f'<div class="defs"><p class="defs-h">名詞小卡</p><dl>{dl}</dl></div>')
        right = []
        for f in s.get("formulas", []):  # 公式與符號表放左欄（run-07 HTML 第 1 次測試：放右欄會溢出）
            # run-08（使用者回饋）：公式用 LaTeX 撰寫，產生時轉成 MathML，由瀏覽器做正式的數學排版
            from latex2mathml.converter import convert as tex2mml
            st = f.get("symbols_tex", {})
            def _sym(k):  # 符號名稱也用數學排版：有 symbols_tex 用它，單一字母直接當成數學變數，mod 等文字維持原樣
                if k in st:
                    return tex2mml(st[k])
                if re.fullmatch(r"[A-Za-zα-ω]", k):
                    return tex2mml(k)
                return e(k)
            sy = "".join(f"<dt>{_sym(k)}</dt><dd>{e(v)}</dd>" for k, v in f["symbols"])
            math = tex2mml(f["tex"], display="block")
            left.append(f'<div class="formula"><p class="fx-h">公式與符號</p><div class="fx" data-expr="{e(f["expr"])}" role="math" aria-label="{e(f["expr"])}">{math}</div><dl class="syms">{sy}</dl></div>')
        v = s.get("visual")
        if v:
            body = tpl.get(s["id"], "")
            if not body:
                raise SystemExit(f"visuals.html 缺少 v-{s['id']}")
            extra = " panel" if s["id"] not in ("rsa-encrypt",) else " panel"
            right.append(f'<figure class="visual{extra}">{body}<figcaption class="figname">{e(v["name"])}</figcaption></figure>')
        body_cls = "slide-body aes-body" if s["id"] == "aes-example" else "slide-body"
        out.append(f'''<section class="{cls}" data-topic="{e(ch)}" aria-label="第 {i + 1} 張：{e(s["title"])}">
  <div class="slide-inner">
    <header class="slide-head"><p class="eyebrow">{e(ch)}</p><h2>{e(s["title"])}</h2><p class="lead">{e(s.get("lead", ""))}</p></header>
    <div class="{body_cls}">
      <div class="textcol">{"".join(left)}</div>
      <div class="rightcol">{"".join(right)}</div>
    </div>
  </div>
</section>''')
    aes = deck["examples"]["aes"]
    aes_data = {"input": aes["input"], "key_rows": aes["key_rows"], "roundkey_rows": aes["roundkey_rows"],
                "frames": [{k: f[k] for k in ("id", "label", "op", "before", "with", "explain", "hl", "rows")} for f in aes["frames"]]}
    page = shell.replace("/*{{EXTRA_CSS}}*/", EXTRA_CSS).replace("{{SLIDES}}", "\n\n".join(out)).replace("{{N}}", str(len(slides))) \
                .replace("/*AES_DATA*/null", json.dumps(aes_data, ensure_ascii=False))
    dest = ROOT / "Slides" / "index.html"
    dest.write_text(page, encoding="utf-8")
    return dest


if __name__ == "__main__":
    p = render()
    print("rendered", p, p.stat().st_size, "bytes")
