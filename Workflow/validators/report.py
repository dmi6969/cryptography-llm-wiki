"""Render Workflow/logs/events.jsonl → Workflow/execution_log.md（不手寫，避免虛構紀錄）。"""
from __future__ import annotations

import json
from pathlib import Path

NODE_ZH = {
    "graph": "Graph 控制", "fetch_sources": "① 資料取得", "ingest_sources": "② 資料 Ingestion",
    "organize_wiki": "③ Wiki 知識整理（agent）", "validate_wiki": "④ Wiki Validation",
    "query_wiki": "⑤ 查詢 Wiki", "draft_content": "⑥ 整理教學內容（agent）",
    "validate_content": "⑦ Content Validation", "build_html": "⑧ 產生 HTML 簡報（agent）",
    "test_html": "⑨ HTML Validation", "done": "⑩ 完成", "halt": "✖ 停止（需人工介入）",
    "batch_lint": "③b Batch 快速檢查（v2）", "visual_review": "★ 截圖人工檢查（Graph 外）",
    "validator_selftest": "★ Validator 自我測試（注入錯誤）",
}


def _short(obj, limit=1600) -> str:
    s = json.dumps(obj, ensure_ascii=False, indent=1)
    return s if len(s) <= limit else s[:limit] + "\n …（截斷，完整內容見 logs/ 下的 JSON）"


def render(root: Path) -> None:
    wf = root / "Workflow"
    ev_p = wf / "logs" / "events.jsonl"
    events = [json.loads(l) for l in ev_p.read_text(encoding="utf-8").splitlines() if l.strip()] \
        if ev_p.exists() else []
    out = ["# Execution Log（實際執行紀錄）", "",
           "> 本檔由 `python Workflow/graph.py report` 從 `Workflow/logs/events.jsonl` 自動產生，"
           "每一筆都是 Graph 執行當下寫入的事件；檢查節點的完整結果在 `Workflow/logs/*_validation_*.json`、"
           "`html_test_*.json`。", ""]
    # 總覽表
    out += ["## 總覽", "", "| # | 時間 | Run | 節點 | 嘗試 | 檢查結果 | 路由決策 |", "|---|---|---|---|---|---|---|"]
    for i, e in enumerate(events, 1):
        chk = e.get("check") or {}
        res = "" if not chk else ("✅ 通過" if chk.get("passed") else
                                  f"❌ 未通過（errors={chk.get('errors', len(chk.get('failed', []) or []))}）")
        node = NODE_ZH.get(e["node"], e["node"])
        if e["node"] == "graph":
            o = e.get("output") or {}
            node += "：" + (f"暫停於 {o.get('paused_at')}" if "paused_at" in o else str(o.get("event", "")))
        out.append(f"| {i} | {e['ts'][:19].replace('T', ' ')} | {e['run']} | {node} | "
                   f"{'' if e.get('attempt') is None else e['attempt']} | {res} | {e.get('decision') or ''} |")
    out += ["", "## 各節點詳細紀錄（輸入 / 輸出 / 檢查 / 修正）", ""]
    for i, e in enumerate(events, 1):
        if e["node"] == "graph":
            continue
        out.append(f"### #{i} {NODE_ZH.get(e['node'], e['node'])} — {e['ts'][:19].replace('T', ' ')}"
                   + (f"（attempt {e['attempt']}）" if e.get("attempt") is not None else ""))
        out.append("")
        for k, label in (("input", "輸入"), ("output", "輸出"), ("check", "檢查結果"), ("fix", "修正／agent 說明"),
                         ("decision", "路由決策")):
            v = e.get(k)
            if v in (None, "", {}, []):
                continue
            if isinstance(v, str):
                out.append(f"- **{label}**：{v}")
            elif k == "check" and isinstance(v, dict) and v.get("issues") is not None:
                out.append(f"- **{label}**：{'✅ 通過' if v.get('passed') else '❌ 未通過'}，"
                           f"errors={v.get('errors')}，warnings={v.get('warnings')}")
                bc = v.get("by_check") or {}
                if bc:
                    out.append("  - 各檢查項：" + "，".join(f"{c}: {d['error']}E/{d['warn']}W" for c, d in bc.items()))
                errs = [x for x in v["issues"] if x.get("severity") == "error"]
                for x in errs[:40]:
                    out.append(f"  - `[{x['check']}]` {x.get('where', '')}：{x['msg']}")
                if len(errs) > 40:
                    out.append(f"  - …其餘 {len(errs) - 40} 筆見 JSON")
            elif k == "fix" and isinstance(v, dict):
                out.append(f"- **{label}**：{v.get('note', '')}")
            else:
                out += [f"- **{label}**：", "", "```json", _short(v), "```"]
        out.append("")
    (wf / "execution_log.md").write_text("\n".join(out) + "\n", encoding="utf-8")
