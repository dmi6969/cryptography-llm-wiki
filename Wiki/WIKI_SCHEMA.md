# Wiki Schema（LLM Wiki 規範檔）

本 Wiki 採用 Karpathy 提出的 LLM Wiki 三層模式：

| 層 | 位置 | 誰維護 | 規則 |
|---|---|---|---|
| 原始資料（Raw sources） | `Wiki/raw/` | 程式（fetch / ingest 節點） | 不可修改；記錄 SHA-256；僅保留於本機 |
| Wiki 頁面 | `Wiki/sources/`、`Wiki/concepts/`、`knowledge_map.md`、`facts.json` | LLM agent（與使用者討論後撰寫） | 必須遵守下方格式，所有技術敘述可追溯到原文 |
| 規範（Schema） | 本檔 + `Workflow/config/*.json` | 使用者與 agent 共同約定 | 修改需在 `log.md` 記錄 |

操作：**Ingest**（加入來源並更新頁面）、**Query**（為簡報查詢 Wiki）、**Lint**（Wiki Validation）。
`log.md` 為只追加的操作紀錄；`knowledge_map.md` 兼作索引（index）。

## 頁面類型

### 1. 來源頁 `Wiki/sources/Sxx-<slug>.md`

```yaml
---
id: S04
type: source
title: <必須與 config/sources.json 完全一致>
url: <必須與 config/sources.json 完全一致>
nodes: [sym-aes, ...]   # 使用本來源的概念節點
---
```
必要段落：`## 摘要`、`## 本 Wiki 使用的章節`（列出章節／PDF 頁碼）。

### 2. 概念頁 `Wiki/concepts/<id>.md`

```yaml
---
id: classical-caesar           # 與檔名相同
title: Caesar Cipher（凱撒密碼）
topic: T2                      # T1–T5
aliases: [Caesar cipher, shift cipher, 凱撒密碼]
sources: [S02, S03]            # 每個來源都必須至少有一條引文
prerequisites: [intro-terminology]
relations:
  - {type: instance-of, target: classical-substitution}
facts: {}                      # 只能使用 facts.json 中已登錄的事實鍵
---
```
必要段落：`## 定義`、`## 重點`（每點標註 `[Sxx p.N]`）、`## 關聯`（使用 `[[id]]`）、`## 來源引文`。
選用段落：`## 範例`、`## 常見誤解`（誤解只能寫在這裡，並說明為何錯誤）。

### 引文格式（Lint 會逐字比對原文）

```
- [S04 p.15 §5] "The AES algorithm takes ... "
```
- `p.N` 為 **抽取文字中的頁碼**（PDF 第 N 頁；RFC 為第 N 頁），不是書上印的頁碼。
- 引號內必須是原文逐字摘錄（允許空白、斷行連字號、標點差異）；不得改寫。
- 章節號（§）為選填，方便人工查閱。

## 關聯型別

`prerequisite`（先備）、`instance-of`（是…的一種）、`part-of`（是…的一部分）、
`limitation-motivates`（其限制促成…）、`contrasts-with`（對比）、`used-by`（被…使用）、
`builds-on`（建立在…之上）、`related`（一般相關）。

## 撰寫原則

1. 只寫來源中有依據的內容；來源沒有的，不寫或標示為「本 Wiki 的教學補充」並說明理由。
2. 舊來源（1976–1996）中的參數建議若已過時，必須以 NIST 現行文件（S12 等）為準並註明。
3. 名詞採台灣用語：加密／解密、明文／密文、金鑰、對稱式加密、公開金鑰、區塊加密、串流加密、操作模式、初始向量（IV）、數位簽章。
