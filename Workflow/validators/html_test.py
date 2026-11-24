"""HTML Validation：用 Playwright 驅動本機 Microsoft Edge（headless）實際開啟 Slides/index.html 測試。

檢查項目：
  H1 開啟：file:// 直接開啟、無 console error / page error / 載入失敗的資源
  H2 內容完整：投影片數量 = slide_content.json；每頁標題、每個重點、每個來源 ID 都出現在對應投影片
  H3 切換：初始 1/N；→ 鍵、← 鍵、下一頁／上一頁按鈕；第一頁按 ← 不越界、最後一頁按 → 不越界；
           任何時刻只有目前那一頁可見
  H4 頁數與進度條：頁碼文字與進度條寬度隨切換更新（最後一頁 100%）
  H5 全螢幕：按鈕呼叫 requestFullscreen，並記錄 document.fullscreenElement 實際狀態
  H6 排版：1280×720 每頁內容不溢出投影片；390×844（手機）不得出現水平捲動
  H7 互動示範：Caesar 滑桿加密結果正確；ECB/CBC 畫布有畫出內容且 ECB 與原圖結構相同；DH/RSA 數值顯示正確
     （v2 新增：ECB 圖兩個主要顏色的 WCAG 對比度 ≥ 3:1，確保肉眼看得出輪廓）
     （run-04 新增：AES 逐步圖解每一步的 state 與內容檔一致；Caesar 解密；操作模式分頁一次只顯示一個）
並為每頁截圖存證（Workflow/screenshots/<tag>/）。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

INIT = """
window.__fsCalls = 0;
const _rf = Element.prototype.requestFullscreen;
Element.prototype.requestFullscreen = function(...a){ window.__fsCalls++; return _rf ? _rf.apply(this, a) : Promise.resolve(); };
"""


def _norm(s: str) -> str:
    return re.sub(r"\s+", "", s or "")


def run(root: Path, tag: str = "manual") -> dict:
    issues: list[dict] = []

    def add(check, sev, where, msg):
        issues.append({"check": check, "severity": sev, "where": where, "msg": msg})

    html = root / "Slides" / "index.html"
    deck = json.loads((root / "Workflow" / "artifacts" / "slide_content.json").read_text(encoding="utf-8"))
    exp = deck["slides"]
    shots = root / "Workflow" / "screenshots" / tag
    shots.mkdir(parents=True, exist_ok=True)
    stats: dict = {"file": str(html.relative_to(root)), "bytes": html.stat().st_size if html.exists() else 0}
    if not html.exists():
        add("H1", "error", "index.html", "檔案不存在")
        return _summary(issues, stats)

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)
        ctx = browser.new_context(viewport={"width": 1280, "height": 720})
        page = ctx.new_page()
        page.add_init_script(INIT)
        console_err, page_err, failed = [], [], []
        page.on("console", lambda m: console_err.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: page_err.append(str(e)))
        page.on("requestfailed", lambda r: failed.append(r.url))
        page.goto(html.as_uri())
        page.wait_for_timeout(600)
        stats["external_requests"] = page.evaluate(
            "performance.getEntriesByType('resource').map(e=>e.name).filter(u=>!u.startsWith('file:'))")

        # H1 -------------------------------------------------------------
        for e in console_err:
            add("H1", "error", "console", e[:150])
        for e in page_err:
            add("H1", "error", "pageerror", e[:150])
        for u in failed:
            add("H1", "error", "request", f"資源載入失敗：{u}")

        # H2 -------------------------------------------------------------
        n = page.locator(".slide").count()
        stats["slides_in_dom"] = n
        if n != len(exp):
            add("H2", "error", "deck", f"DOM 有 {n} 張投影片，內容檔有 {len(exp)} 張")
        for i, s in enumerate(exp):
            if i >= n:
                break
            el = page.locator(".slide").nth(i)
            text = _norm(el.text_content())
            h = el.locator("h1, h2").first
            title = _norm(h.text_content()) if h.count() else ""
            if _norm(s["title"]) not in title:
                add("H2", "error", f"slide {i + 1}", f"標題不符：預期「{s['title']}」，實際「{title[:40]}」")
            for k, pt in enumerate(s.get("points", []), 1):
                if _norm(pt["text"]) not in text:
                    add("H2", "error", f"slide {i + 1}", f"缺少重點{k}：{pt['text'][:30]}")
            # run-07：名詞小卡、公式符號說明、圖片名稱都要真的出現在畫面上
            for d in s.get("defines", []):
                if _norm(d["term"]) not in text or _norm(d["text"]) not in text:
                    add("H2", "error", f"slide {i + 1}", f"缺少名詞解釋：{d['term']}")
            for f in s.get("formulas", []):
                # run-08：公式必須以 MathML 實際排版出來（不是純文字 c_i、M^e）
                ok = page.evaluate("""([i, ex]) => { const el = document.querySelectorAll('.slide')[i];
                    const box = [...el.querySelectorAll('[data-expr]')].find(x => x.dataset.expr === ex);
                    const m = box && box.querySelector('math');
                    return !!(m && m.getBoundingClientRect().height > 0 || (m && getComputedStyle(m).display !== 'none')); }""", [i, f["expr"]])
                if not ok:
                    add("H2", "error", f"slide {i + 1}", f"公式沒有用數學排版顯示：{f['expr']}")
                for sym, meaning in f.get("symbols", []):
                    if _norm(meaning) not in text:
                        add("H2", "error", f"slide {i + 1}", f"公式 {f['expr']} 缺少符號 {sym} 的說明")
            vname = (s.get("visual") or {}).get("name")
            if vname and _norm(vname) not in text:
                add("H2", "error", f"slide {i + 1}", f"缺少圖片名稱：{vname}")
        # run-07（使用者回饋：來源不用每頁都有）：最後的參考資料頁要列出所有用到的來源
        used = sorted({sid for s in exp for sid in s.get("sources", [])})
        ref = next((k for k, s in enumerate(exp) if s.get("id") == "references"), None)
        if ref is None:
            add("H2", "error", "deck", "沒有參考資料頁")
        else:
            rtext = _norm(page.locator(".slide").nth(ref).text_content())
            for sid in used:
                if sid not in rtext:
                    add("H2", "error", "references", f"參考資料頁沒有列出 {sid}")
        # H8（run-07）：名詞先解釋——用實際畫面文字檢查
        import re as _re
        gl = json.loads((root / "Workflow" / "config" / "glossary.json").read_text(encoding="utf-8"))["terms"]
        defined = set()
        for i, s in enumerate(exp):
            here = {d["term"] for d in s.get("defines", [])}
            if s.get("id") not in ("cover", "roadmap", "references") and i < n:
                # 逐個文字節點用分隔符接起來：相鄰元素（例如「演算法：公開」「金鑰：保密」）不會黏成假名詞
                dom = page.evaluate("""(i) => { const el = document.querySelectorAll('.slide')[i];
                    const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); const out = [];
                    while (w.nextNode()) { if (!w.currentNode.parentElement.closest('[data-glossary-skip]')) out.push(w.currentNode.nodeValue); }
                    return out.join(' ｜ '); }""", i)  # run-09：轉場頁的「本章預告」可以先提到名詞
                for g in gl:
                    if g["term"] not in defined | here and _re.search(g["pattern"], dom):
                        add("H8", "error", f"slide {i + 1}", f"畫面上第一次出現「{g['term']}」，但之前沒有解釋")
            defined |= here
        # H9（run-08，使用者回饋）：畫面文字不能出現沒排版的數學寫法（x^2、E_K、c_i）
        for i, s in enumerate(exp):
            if i >= n:
                break
            raw = page.evaluate("""(i) => { const el = document.querySelectorAll('.slide')[i];
                const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT); const out = [];
                while (w.nextNode()) { if (!w.currentNode.parentElement.closest('math')) out.push(w.currentNode.nodeValue); }
                return out.join(' ｜ '); }""", i)
            for m in _re.finditer(r"[A-Za-z0-9α-ω)\]]\^|(?<![A-Za-z])[A-Za-z]_[A-Za-z0-9{]", raw):
                add("H9", "error", f"slide {i + 1}", f"出現沒有排版的數學寫法：…{raw[max(0, m.start() - 8):m.end() + 8]}…")
                break

        # H3 / H4 --------------------------------------------------------
        def state():
            return page.evaluate("""() => {
              const vis = [...document.querySelectorAll('.slide')].map(s => {
                const cs = getComputedStyle(s), r = s.getBoundingClientRect();
                return cs.visibility !== 'hidden' && cs.display !== 'none' && parseFloat(cs.opacity) > 0.5
                       && r.width > 0 && r.height > 0; });
              const bar = document.querySelector('#progress-bar');
              const track = bar ? bar.parentElement.getBoundingClientRect().width : 0;
              return { visible: vis.map((v,i)=>v?i+1:0).filter(Boolean),
                       counter: (document.querySelector('#counter')||{}).textContent || '',
                       progress: bar && track ? bar.getBoundingClientRect().width / track : -1 };
            }""")

        def expect(where, idx):
            page.wait_for_timeout(450)
            st = state()
            ok = True
            if st["visible"] != [idx]:
                add("H3", "error", where, f"可見投影片應只有 {idx}，實際 {st['visible']}")
                ok = False
            if _norm(st["counter"]) != f"{idx}/{n}":
                add("H4", "error", where, f"頁碼應為 {idx}/{n}，實際「{st['counter']}」")
                ok = False
            want = idx / n
            if abs(st["progress"] - want) > 0.03:
                add("H4", "error", where, f"進度條應約 {want:.0%}，實際 {st['progress']:.0%}")
                ok = False
            return ok

        nav = []
        nav.append(("初始", expect("初始", 1)))
        page.keyboard.press("ArrowLeft"); nav.append(("第 1 頁按 ←", expect("第 1 頁按 ←", 1)))
        page.keyboard.press("ArrowRight"); nav.append(("→", expect("→", 2)))
        page.click("#next"); nav.append(("下一頁按鈕", expect("下一頁按鈕", 3)))
        page.click("#prev"); nav.append(("上一頁按鈕", expect("上一頁按鈕", 2)))
        page.keyboard.press("ArrowLeft"); nav.append(("←", expect("←", 1)))
        for _ in range(n + 2):
            page.keyboard.press("ArrowRight")
        nav.append(("連按 → 到最後", expect("連按 → 到最後", n)))
        page.keyboard.press("ArrowLeft"); nav.append(("最後一頁按 ←", expect("最後一頁按 ←", n - 1)))
        stats["navigation"] = {k: v for k, v in nav}

        # H5 -------------------------------------------------------------
        if page.locator("#fullscreen").count() == 0:
            add("H5", "error", "fullscreen", "找不到全螢幕按鈕 #fullscreen")
        else:
            page.click("#fullscreen")
            page.wait_for_timeout(500)
            calls = page.evaluate("window.__fsCalls")
            fs_el = page.evaluate("!!document.fullscreenElement")
            stats["fullscreen"] = {"requestFullscreen_calls": calls, "fullscreenElement_after_click": fs_el}
            if calls < 1:
                add("H5", "error", "fullscreen", "按下全螢幕按鈕沒有呼叫 requestFullscreen")
            if fs_el:
                page.evaluate("document.exitFullscreen && document.exitFullscreen()")
                page.wait_for_timeout(300)

        # H6 desktop + screenshots --------------------------------------
        page.keyboard.press("Home")
        page.wait_for_timeout(300)
        overflow = []
        for i in range(n):
            page.evaluate(f"window.goTo && window.goTo({i})")
            page.wait_for_timeout(420)
            o = page.evaluate(f"""() => {{
              const s = document.querySelectorAll('.slide')[{i}];
              const inner = s.querySelector('.slide-inner') || s;
              const sr = s.getBoundingClientRect();
              const bad = [...inner.querySelectorAll('*')].filter(e => {{
                 const r = e.getBoundingClientRect();
                 return r.width > 0 && (r.bottom > sr.bottom + 2 || r.right > sr.right + 2 || r.left < sr.left - 2);
              }}).slice(0,3).map(e => e.tagName + '.' + (e.className||'') + ':' + (e.textContent||'').trim().slice(0,30));
              return {{ sh: inner.scrollHeight, ch: inner.clientHeight, bad }};
            }}""")
            if o["sh"] > o["ch"] + 2 or o["bad"]:
                overflow.append(i + 1)
                add("H6", "error", f"slide {i + 1}", f"1280×720 內容溢出（scrollHeight {o['sh']} > {o['ch']}）：{o['bad']}")
            page.screenshot(path=str(shots / f"desktop-slide-{i + 1:02d}.png"))
        stats["desktop_overflow_slides"] = overflow

        # H7 interactive --------------------------------------------------
        demo = {}
        try:
            ci = next(i for i, s in enumerate(exp) if (s.get("visual") or {}).get("type") == "caesar-demo")
            page.evaluate(f"window.goTo({ci})"); page.wait_for_timeout(400)
            for shift, plain, want in ((3, "HELLO", "KHOOR"), (1, "HAL", "IBM"), (0, "ABC", "ABC")):
                page.fill("#caesar-input", plain)
                page.evaluate(f"""() => {{ const r = document.querySelector('#caesar-shift'); r.value = {shift};
                                  r.dispatchEvent(new Event('input', {{bubbles:true}})); }}""")
                got = _norm(page.text_content("#caesar-output"))
                demo[f"caesar {plain}+{shift}"] = got
                if got != want:
                    add("H7", "error", "caesar-demo", f"{plain} 位移 {shift} 應為 {want}，畫面顯示 {got}")
        except StopIteration:
            add("H7", "error", "caesar-demo", "找不到 Caesar 互動示範")
        try:
            ei = next(i for i, s in enumerate(exp) if (s.get("visual") or {}).get("type") == "ecb-demo")
            page.evaluate(f"window.goTo({ei})"); page.wait_for_timeout(500)
            ecb = page.evaluate("""() => {
              const ids = ['ecb-orig','ecb-ecb','ecb-cbc'];
              const px = ids.map(id => { const c = document.getElementById(id); if (!c) return null;
                 const d = c.getContext('2d').getImageData(0,0,c.width,c.height).data; return Array.from(d); });
              if (px.some(x => !x)) return {missing: true};
              const distinct = px.map(a => new Set(a.filter((_,i)=>i%4===0)).size);
              // ECB 結構相同：原圖相同顏色的像素，在 ECB 圖中也相同；CBC 則否
              const same = (a,b) => { let agree=0, tot=0; for (let i=0;i<a.length;i+=4*7){ for (let j=i+4*13;j<Math.min(a.length,i+4*400);j+=4*97){
                 const eqA = a[i]===a[j]&&a[i+1]===a[j+1]&&a[i+2]===a[j+2]; const eqB = b[i]===b[j]&&b[i+1]===b[j+1]&&b[i+2]===b[j+2];
                 if (eqA){ tot++; if (eqB) agree++; } } } return tot? agree/tot : 0; };
              // v2（run-01 人工看截圖才發現 ECB 兩色太接近）：ECB 圖兩個最常見顏色的 WCAG 對比度
              const top2 = a => { const m = new Map(); for (let i=0;i<a.length;i+=4){ const k=a[i]+','+a[i+1]+','+a[i+2]; m.set(k,(m.get(k)||0)+1); }
                 return [...m.entries()].sort((x,y)=>y[1]-x[1]).slice(0,2).map(e=>e[0].split(',').map(Number)); };
              const lum = c => { const f = v => { v/=255; return v<=0.03928? v/12.92 : Math.pow((v+0.055)/1.055,2.4); };
                 return 0.2126*f(c[0])+0.7152*f(c[1])+0.0722*f(c[2]); };
              const cr = (a,b) => { const L1=Math.max(lum(a),lum(b)), L2=Math.min(lum(a),lum(b)); return (L1+0.05)/(L2+0.05); };
              const t = top2(px[1]);
              return {distinct, ecbStructure: same(px[0],px[1]), cbcStructure: same(px[0],px[2]),
                      ecbContrast: t.length===2 ? cr(t[0],t[1]) : 0};
            }""")
            demo["ecb"] = ecb
            if ecb.get("missing"):
                add("H7", "error", "ecb-demo", "找不到三個畫布 #ecb-orig/#ecb-ecb/#ecb-cbc")
            else:
                if min(ecb["distinct"]) < 2:
                    add("H7", "error", "ecb-demo", f"畫布沒有畫出內容（distinct={ecb['distinct']}）")
                if ecb["ecbStructure"] < 0.9:
                    add("H7", "error", "ecb-demo", f"ECB 圖沒有保留原圖結構（{ecb['ecbStructure']:.2f}），示範不成立")
                if ecb["cbcStructure"] > 0.5:
                    add("H7", "error", "ecb-demo", f"CBC 圖仍保留原圖結構（{ecb['cbcStructure']:.2f}），示範不成立")
                if ecb.get("ecbContrast", 0) < 3.0:
                    add("H7", "error", "ecb-demo",
                        f"ECB 圖兩個主要顏色對比度只有 {ecb.get('ecbContrast', 0):.2f}:1（< 3:1），初學者看不出輪廓")
        except StopIteration:
            add("H7", "error", "ecb-demo", "找不到 ECB 示範")
        ex = deck.get("examples", {})
        # run-04：AES 逐步圖解——每一步畫面上的 4×4 state 都要和內容檔（已由 C4 重算驗證）一致
        ai = next((i for i, s in enumerate(exp) if (s.get("visual") or {}).get("type") == "aes-walkthrough"), None)
        if ai is not None and "aes" in ex:
            page.evaluate(f"window.goTo({ai})"); page.wait_for_timeout(400)
            ok_steps = 0
            for k, fr in enumerate(ex["aes"]["frames"]):
                btn = page.locator(f'.aes-step[data-step="{k}"]')
                if btn.count() == 0:
                    add("H7", "error", "aes-walkthrough", f"找不到第 {k + 1} 步的按鈕（{fr['label']}）")
                    continue
                btn.click(); page.wait_for_timeout(150)
                cells = [c.strip().lower() for c in page.locator("#aes-after .cell").all_text_contents()]
                want = " ".join(fr["rows"]).lower().split()
                expl = _norm(page.text_content("#aes-explain") or "")
                if cells != want:
                    add("H7", "error", "aes-walkthrough", f"「{fr['label']}」畫面上的 state 與內容不符：{' '.join(cells)[:60]}")
                elif not expl:
                    add("H7", "error", "aes-walkthrough", f"「{fr['label']}」沒有說明文字")
                else:
                    ok_steps += 1
            demo["aes_steps_ok"] = f"{ok_steps}/{len(ex['aes']['frames'])}"
        elif "aes" in ex:
            add("H7", "error", "aes-walkthrough", "內容檔有 AES 實例，但 HTML 沒有 AES 逐步圖解")
        # run-04：Caesar 解密方向
        if page.locator("#caesar-mode-dec").count():
            ci = next(i for i, s in enumerate(exp) if (s.get("visual") or {}).get("type") == "caesar-demo")
            page.evaluate(f"window.goTo({ci})"); page.wait_for_timeout(300)
            page.click("#caesar-mode-dec")
            page.fill("#caesar-input", "KHOOR")
            page.evaluate("""() => { const r = document.querySelector('#caesar-shift'); r.value = 3;
                              r.dispatchEvent(new Event('input', {bubbles:true})); }""")
            got = _norm(page.text_content("#caesar-output"))
            demo["caesar decrypt KHOOR-3"] = got
            if got != "HELLO":
                add("H7", "error", "caesar-demo", f"解密 KHOOR（k=3）應為 HELLO，畫面顯示 {got}")
            page.click("#caesar-mode-enc")
        # run-04：操作模式分頁圖解——每次只顯示一個分頁
        tabs = page.locator(".mode-tab")
        if tabs.count():
            mi = page.evaluate("[...document.querySelectorAll('.slide')].indexOf(document.querySelector('.mode-tab').closest('.slide'))")
            page.evaluate(f"window.goTo({mi})"); page.wait_for_timeout(300)
            for j in range(tabs.count()):
                tabs.nth(j).click(); page.wait_for_timeout(120)
                # 檢查「實際上看得到」（computed display 與高度），不只看 hidden 屬性——
                # run-04 第 1 次測試時，CSS 的 display:flex 蓋過了 hidden，4 個分頁同時顯示，舊寫法抓不到
                vis = page.evaluate("""() => [...document.querySelectorAll('.mode-panel')].map(p =>
                    getComputedStyle(p).display !== 'none' && p.getBoundingClientRect().height > 0)""")
                if vis.count(True) != 1 or not vis[j]:
                    add("H7", "error", "mode-tabs", f"點第 {j + 1} 個分頁後，可見分頁為 {vis}")
            tabs.nth(0).click()
            demo["mode_tabs"] = tabs.count()
        body = _norm(page.text_content("body"))
        if "dh" in ex and _norm(f"K={ex['dh']['k']}") not in body:
            add("H7", "error", "dh-demo", f"畫面沒有顯示共享金鑰 K = {ex['dh']['k']}")
        if "rsa" in ex and str(ex["rsa"]["c"]) not in body:
            add("H7", "error", "rsa", f"畫面沒有顯示 RSA 密文 {ex['rsa']['c']}")
        stats["demos"] = demo

        # H6 mobile --------------------------------------------------------
        m = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        mp = m.new_page()
        mp.goto(html.as_uri()); mp.wait_for_timeout(500)
        mob = []
        overlap_js = f"""(i) => {{
            // run-04 截圖檢查發現：手機上內容太長時 .slide-body 被壓縮，內容溢出蓋到下方來源欄。
            // 檢查：.slide-body 的內容不能超出它自己的框，且來源欄必須在內容下方（不重疊）。
            const s = document.querySelectorAll('.slide')[i];
            const body = s.querySelector('.slide-body'), foot = s.querySelector('.sources');
            if (!body) return null;
            const b = body.getBoundingClientRect(), f = foot ? foot.getBoundingClientRect() : null;
            const kids = [...body.querySelectorAll('*')].map(e => e.getBoundingClientRect()).filter(r => r.height > 0);
            const contentBottom = Math.max(b.bottom, ...kids.map(r => r.bottom));
            return {{ overflow: Math.round(contentBottom - b.bottom), gap: f ? Math.round(f.top - contentBottom) : 999 }};
        }}"""
        for i in range(n):
            mp.evaluate(f"window.goTo && window.goTo({i})"); mp.wait_for_timeout(380)
            w = mp.evaluate("[document.documentElement.scrollWidth, window.innerWidth]")
            if w[0] > w[1] + 1:
                mob.append(i + 1)
                add("H6", "error", f"slide {i + 1}", f"手機寬度出現水平捲動（scrollWidth {w[0]} > {w[1]}）")
            ov = mp.evaluate(overlap_js, i)
            if ov and (ov["overflow"] > 2 or ov["gap"] < -2):
                mob.append(i + 1)
                add("H6", "error", f"slide {i + 1}",
                    f"390×844 內容與來源欄重疊（內容超出框 {ov['overflow']}px，來源欄與內容距離 {ov['gap']}px）")
            if i in (0, 3, 7, 10):
                mp.screenshot(path=str(shots / f"mobile-slide-{i + 1:02d}.png"))
        stats["mobile_hscroll_slides"] = mob
        browser.close()
    return _summary(issues, stats)


def _summary(issues, stats):
    n_err = sum(1 for i in issues if i["severity"] == "error")
    by = {c: {"error": sum(1 for i in issues if i["check"] == c and i["severity"] == "error"),
              "warn": sum(1 for i in issues if i["check"] == c and i["severity"] == "warn")}
          for c in ("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9")}
    return {"passed": n_err == 0, "n_errors": n_err, "n_warnings": len(issues) - n_err,
            "by_check": by, "issues": issues, "stats": stats}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    r = run(Path(__file__).resolve().parents[2], tag=sys.argv[1] if len(sys.argv) > 1 else "manual")
    print(json.dumps({k: v for k, v in r.items() if k != "issues"}, ensure_ascii=False, indent=2))
    for i in r["issues"]:
        print(f"[{i['check']}][{i['severity']}] {i['where']}: {i['msg']}")
