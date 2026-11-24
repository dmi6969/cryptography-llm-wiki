# Cryptography 101：用 LLM Wiki 製作教學 HTML 簡報

大學課程作業：先建立密碼學主題的 LLM Wiki，再以 Wiki 為知識來源，製作給初學者的教學 HTML 簡報；整個流程用 LangGraph 建立成有檢查與退回機制的 Loop／Graph，並實際執行。

- **繳交文件**：[`Report/submission.docx`](Report/submission.docx)（依作業要求逐題作答）
- **教學簡報**：[`Slides/index.html`](Slides/index.html)（單一檔案，下載後用瀏覽器開啟）
- **完整報告**：[`Report/final_report.md`](Report/final_report.md)

## 內容

| 資料夾 | 內容 |
|---|---|
| `Wiki/` | LLM Wiki：22 個知識節點（`concepts/`）、15 個來源頁（`sources/`）、知識地圖 `knowledge_map.md`、資料來源清單 `sources.md`、操作紀錄 `log.md`、規範 `WIKI_SCHEMA.md` |
| `Slides/` | 教學 HTML 簡報（35 張、6 章） |
| `Workflow/` | LangGraph 主程式 `graph.py`、三個檢查節點 `validators/`、簡報產生器 `tools/`、設計說明 `workflow.md`、實際執行紀錄 `execution_log.md` 與 `logs/`、HTML 測試截圖 `screenshots/` |
| `Report/` | 繳交文件、完整報告、作業心得 |

## 資料來源

15 篇：NIST 標準（FIPS 197、SP 800-38A／38D／57／175B）、IETF RFC（4949、8017、8446）、大學教材（Handbook of Applied Cryptography、The Joy of Cryptography）、原始論文（Diffie–Hellman 1976、RSA 1978）與入門教材（Crypto 101、Cloudflare）。完整網址與 SHA-256 見 [`Wiki/sources.md`](Wiki/sources.md)。

原始 PDF 與抽取文字（`Wiki/raw/`）未上傳：部分教科書章節的授權僅允許個人保存。

## 重新執行

```bash
python -m venv .venv
.venv/Scripts/pip install langgraph langgraph-checkpoint-sqlite pypdf playwright pyyaml latex2mathml
cd Workflow
python graph.py start --thread run-10      # 會重新下載來源到 Wiki/raw/
python validators/wiki_lint.py            # Wiki Validation
python validators/content_check.py        # Content Validation
python validators/html_test.py manual     # HTML Validation（需要 Microsoft Edge）
```
