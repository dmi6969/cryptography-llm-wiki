"""Validator 自我測試（mutation test）：在專案副本中注入已知錯誤，確認三個檢查節點都抓得到。

目的：Content Validation 與 HTML Validation 在 run-01 第一次就通過——要排除「檢查太寬鬆所以才通過」的可能。
每個案例都在獨立副本中執行，不會動到正式檔案。結果寫入 logs/validator_selftest.json。

用法：python validators/selftest.py <暫存資料夾>
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import content_check  # noqa: E402
import html_test  # noqa: E402
import wiki_lint  # noqa: E402


def sub(path: Path, old: str, new: str, count: int = 1) -> None:
    t = path.read_text(encoding="utf-8")
    if old not in t:
        raise RuntimeError(f"注入失敗：{path.name} 找不到「{old[:40]}」")
    path.write_text(t.replace(old, new, count), encoding="utf-8")


def edit_json(path: Path, fn) -> None:
    d = json.loads(path.read_text(encoding="utf-8"))
    fn(d)
    path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")


def swap_slides(d):
    # 依 id 交換（run-09 加入轉場頁後，固定位置 5、6 已不是工具頁與 Caesar 頁，原案例失效）
    s = d["slides"]
    a = next(i for i, x in enumerate(s) if x["id"] == "tools")
    b = next(i for i, x in enumerate(s) if x["id"] == "caesar")
    s[a], s[b] = s[b], s[a]
    for i, x in enumerate(s, 1):
        x["no"] = i


CASES = [
    # (id, 說明, 驗證器, 預期檢查碼, 注入函式)
    ("W5-fabricated-quote", "把 AES 引文的 128 bits 改成 256 bits（虛構引文）", "wiki", "W5",
     lambda r: sub(r / "Wiki/concepts/sym-aes.md", "decrypt data in blocks of 128 bits.\"", "decrypt data in blocks of 256 bits.\"")),
    ("W5-wrong-page", "把引文頁碼 p.4 改成 p.30", "wiki", "W5",
     lambda r: sub(r / "Wiki/concepts/sym-aes.md", "[S04 p.4 §3] \"The AES algorithm is capable", "[S04 p.30 §3] \"The AES algorithm is capable")),
    ("W8-fact-contradiction", "概念頁宣稱 AES-128 做 12 輪", "wiki", "W8",
     lambda r: sub(r / "Wiki/concepts/sym-aes.md", "aes.rounds: {AES-128: 10,", "aes.rounds: {AES-128: 12,")),
    ("W6-broken-link", "加入不存在的節點連結 [[mode-xts]]", "wiki", "W6",
     lambda r: sub(r / "Wiki/concepts/mode-overview.md", "## 關聯\n", "## 關聯\n\n- 另見 [[mode-xts]]\n")),
    ("W2-missing-source-page", "刪除來源頁 S11", "wiki", "W2",
     lambda r: (r / "Wiki/sources/S11-sp800-38d.md").unlink()),
    ("W8-misconception", "在重點段落寫入過時說法「HTTPS 用 RSA 加密 session key」", "wiki", "W8",
     lambda r: sub(r / "Wiki/concepts/app-hybrid-tls.md", "## 重點\n", "## 重點\n\n- HTTPS 是用 RSA 加密 session key 再傳給伺服器 [S10 p.8]。\n")),
    ("C2-no-wiki-node", "投影片重點沒有標註 Wiki 節點", "content", "C2",
     lambda r: edit_json(r / "Workflow/artifacts/slide_content.json", lambda d: d["slides"][1]["points"][0].update(nodes=[]))),
    ("C3-wrong-rounds", "投影片寫「AES-128 做 12 輪」", "content", "C3",
     lambda r: edit_json(r / "Workflow/artifacts/slide_content.json",
                         lambda d: d["slides"][6]["points"][1].update(text="AES-128 做 12 輪運算"))),
    ("C4-wrong-rsa", "RSA 範例密文寫成 949", "content", "C4",
     lambda r: edit_json(r / "Workflow/artifacts/slide_content.json", lambda d: d["examples"]["rsa"].update(c=949))),
    ("C5-wrong-order", "把 AES 那頁移到對稱式加密之前", "content", "C5",
     lambda r: edit_json(r / "Workflow/artifacts/slide_content.json", swap_slides)),
    ("C6-text-overload", "第 2 張塞到 6 個重點", "content", "C6",
     lambda r: edit_json(r / "Workflow/artifacts/slide_content.json",
                         lambda d: d["slides"][1]["points"].extend(d["slides"][1]["points"][:2]))),
    # run-07：使用者回饋轉成的新檢查
    ("C7-term-before-definition", "拿掉 mod 的名詞解釋（Caesar 頁會先用到 mod）", "content", "C7",
     lambda r: edit_json(r / "Workflow/artifacts/slide_content.json",
                         lambda d: next(s for s in d["slides"] if s["id"] == "tools").update(
                             defines=[x for x in next(s for s in d["slides"] if s["id"] == "tools")["defines"] if x["term"] != "mod"]))),
    ("C8-symbol-unexplained", "RSA 加密公式拿掉 n 的說明", "content", "C8",
     lambda r: edit_json(r / "Workflow/artifacts/slide_content.json",
                         lambda d: next(s for s in d["slides"] if s["id"] == "rsa-encrypt")["formulas"][0].update(
                             symbols=[x for x in next(s for s in d["slides"] if s["id"] == "rsa-encrypt")["formulas"][0]["symbols"] if x[0] != "n"]))),
    ("C9-figure-source-wording", "圖片名稱寫成「依 HAC 圖 1.6 改繪」", "content", "C9",
     lambda r: edit_json(r / "Workflow/artifacts/slide_content.json",
                         lambda d: next(s for s in d["slides"] if s["id"] == "terms")["visual"].update(name="依 HAC 圖 1.6 改繪"))),
    ("C10-missing-real-world", "第 3 章拿掉所有「現實應用」", "content", "C10",
     lambda r: edit_json(r / "Workflow/artifacts/slide_content.json",
                         lambda d: [s.update(role=[x for x in s.get("role", []) if x != "現實應用"]) for s in d["slides"] if s.get("chapter") == "ch3"])),
    ("H8-term-before-definition-dom", "HTML 第 3 張多一句先提到 RSA", "html", "H8",
     lambda r: sub(r / "Slides/index.html", "<li>機密性：只有被授權的人看得到內容</li>",
                   "<li>機密性：只有被授權的人看得到內容</li><li>例如 RSA</li>")),
    # run-08：數學排版
    ("C8-no-tex", "RSA 加密公式拿掉 LaTeX（只剩純文字）", "content", "C8",
     lambda r: edit_json(r / "Workflow/artifacts/slide_content.json",
                         lambda d: next(s for s in d["slides"] if s["id"] == "rsa-encrypt")["formulas"][0].pop("tex"))),
    ("H9-raw-math", "HTML 第 3 張多一句沒排版的 x^2", "html", "H9",
     lambda r: sub(r / "Slides/index.html", "<li>機密性：只有被授權的人看得到內容</li>",
                   "<li>機密性：只有被授權的人看得到內容</li><li>例如 x^2</li>")),
    # run-09：章與章之間的承上啟下
    ("C10-no-transition", "拿掉第 4 章的轉場頁（AES 直接跳到 ECB）", "content", "C10",
     lambda r: edit_json(r / "Workflow/artifacts/slide_content.json",
                         lambda d: d.update(slides=[dict(s, no=i) for i, s in enumerate([x for x in d["slides"] if x["id"] != "ch4-intro"], 1)]))),
    ("H5-no-fullscreen", "移除全螢幕按鈕", "html", "H5",
     lambda r: sub(r / "Slides/index.html", 'id="fullscreen"', 'id="fs-removed"')),
    ("H2-missing-point", "HTML 漏掉第 3 張的一個重點", "html", "H2",
     lambda r: sub(r / "Slides/index.html",
                   "<li>網路上任何人都可能偷聽，但只看得到看不懂的密文</li>", "")),  # run-07 版內容
]


def run(tmp: Path) -> dict:
    base = tmp / "base"
    if base.exists():
        shutil.rmtree(base)
    for d in ("Wiki", "Workflow/config", "Workflow/artifacts", "Slides"):
        shutil.copytree(ROOT / d, base / d)
    results = []
    for cid, desc, kind, code, inject in CASES:
        case = tmp / cid
        if case.exists():
            shutil.rmtree(case)
        shutil.copytree(base, case)
        inject(case)
        if kind == "wiki":
            res = wiki_lint.run(case)
        elif kind == "content":
            res = content_check.run(case)
        else:
            res = html_test.run(case, tag=f"selftest-{cid}")
        hits = [i for i in res["issues"] if i["check"] == code and i["severity"] == "error"]
        results.append({"case": cid, "injected": desc, "validator": kind, "expected_check": code,
                        "caught": bool(hits) and not res["passed"],
                        "evidence": hits[0]["msg"][:120] if hits else None})
        print(f"{'✅' if results[-1]['caught'] else '❌'} {cid}: {results[-1]['evidence']}")
    # 對照組：未注入錯誤的副本必須全部通過
    control = {"wiki": wiki_lint.run(base)["passed"], "content": content_check.run(base)["passed"]}
    out = {"cases": results, "caught": sum(r["caught"] for r in results), "total": len(results),
           "control_unmodified_passes": control}
    (ROOT / "Workflow/logs/validator_selftest.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


if __name__ == "__main__":
    r = run(Path(sys.argv[1]))
    print(f"caught {r['caught']}/{r['total']}；未注入對照組通過：{r['control_unmodified_passes']}")
