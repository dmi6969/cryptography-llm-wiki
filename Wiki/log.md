# Wiki Log（只追加，不修改）

格式：`## [時間] 操作 | 說明`

## [2026-11-24 19:13] fetch | 取得 12/12 篇來源

## [2026-11-24 19:13] ingest | 抽取文字 12/12 篇

## [2026-11-24 19:35] organize | batch 1 Introduction to Cryptography：Batch 1（T1 Introduction）：讀 S01 RFC 4949 條目（cryptography/encryption/key/key space/cipher/brute force/security by obscurity 等）與 S02 HAC §1.1–1.4；建立 intro-what-is-crypto、intro-terminology、intro-kerckhoffs、來源頁 S01/S02、facts.json 初版、knowledge_map 初版。決策：HAC 稱 DES 仍為標準（1996）已過時，以 RFC 4949（AES 取代 DES）為準並加時效註記；HAC 的 key pair (e,d) 與公鑰私鑰對區分說明；authentication 譯為「鑑別」、攻擊者用 Adversary（來源無 Eve）。使用者指示後續由 agent 自行完成，不再逐批確認。

## [2026-11-24 19:37] organize | batch 2 Classical Cryptography：Batch 2（T2 Classical）：讀 S02 HAC §1.5.1–1.5.3 與 S03 HAC §7.3.1–7.3.5；建立 classical-caesar、classical-substitution（含 homophonic、Vigenère、Kasiski）、classical-transposition、classical-limitations 與來源頁 S03，更新 S02 來源頁，facts.json 新增 caesar.key_count=26、caesar.julius_key=3、substitution.key_count_english=26!。發現 PDF 把 Vigenère 的重音拆成獨立符號（Vigen+重音+ere），在 textnorm 加入去重音正規化，避免引文比對誤判。

## [2026-11-24 19:40] ingest-fix | batch 3 整理時發現 S04（FIPS 197 upd1）PDF 的 fi 連字 ToUnicode 錯誤：pypdf、pdfminer.six、PyMuPDF 抽出結果都相同（specified→specifed），屬於來源檔本身問題。原 ingest 檢查只看字數與關鍵字，沒有發現。修正：textnorm 新增連字遺失偵測與 fi→f 摺疊比對；ingest 節點新增 ligature-loss 警告（檢查提前到 ingest）。

## [2026-11-24 19:43] organize | batch 3 Symmetric Encryption：Batch 3（T3 Symmetric）：讀 S02 HAC §1.5.1/1.5.4/1.5.5、S04 FIPS 197（Abstract、§1、Table 3、§5.1–5.1.4）、S06 SP 800-175B §3.2–3.2.1.4、S12 SP 800-57 Table 2；建立 sym-concept（含金鑰分配問題、1000 人需 499,500 把金鑰）、sym-block-vs-stream、sym-aes；來源頁 S04/S06/S12；facts 新增 aes.block_bits/key_bits/rounds/selected_year、des.withdrawn_year；misconceptions 新增 AES 區塊大小、DES 仍是標準。S06 指出 DES 於 2005 撤銷，進一步證實 batch 1 的時效判斷。本批發現並處理 S04 的 fi 連字遺失（詳見 log.md ingest-fix）。另將 intro-what-is-crypto 的時效註記移到『常見誤解』段落，避免與誤解規則衝突。

## [2026-11-24 19:46] organize | batch 4 Block Cipher Modes：Batch 4（T4 Modes）：讀 S05 SP 800-38A（Abstract、§5.3 IV、§6.1 ECB、§6.2 CBC、§6.5 CTR、App.A 填充、App.B.2 計數器唯一性）、S03 HAC §7.2.2（ECB／CBC 性質、Remark 7.12）、S11 SP 800-38D（§1、§5.2、§8 IV 唯一性）；建立 mode-overview、mode-ecb、mode-cbc、mode-ctr、mode-gcm-aead 與來源頁 S05/S11，更新 S03；facts 新增 modes.sp800_38a、gcm.block_bits；misconceptions 新增 ECB 安全、IV 必須保密（用否定字排除避免誤判）。自我檢查時發現 mode-gcm-aead 內文引用 S05 但 frontmatter 未列，已補上來源與引文。

## [2026-11-24 19:53] organize | batch 5 Asymmetric Cryptography & Applications：Batch 5（T5 Asymmetric & Apps）：讀 S07 Diffie–Hellman §I/§III、S08 RSA（Abstract、§IV、§V、§VII、§VIII 範例）、S09 RFC 8017 §3.1/§7/§7.1/§8、S10 RFC 8446 §1/§1.2/§2/§4.4.3/§9.1/App.E.1、S06 §3.3、S12 Table 2；建立 asym-public-key、asym-key-exchange、asym-rsa、asym-signature、app-hybrid-tls 與來源頁 S07–S10，更新 S06/S12；facts 新增 rsa.example（論文 p=47,q=59）、rsa.paper_recommended_digits=200、rsa.k_for_112bit=2048、rsa.k_for_128bit=3072、tls13.*；misconception 新增 TLS1.3 RSA 金鑰傳輸。DH 小數字範例為自行計算，不放進 facts（無原文可引），改由 Content Validation 重算。完成 knowledge_map（索引 + Mermaid + 簡報對應）。另先寫好 query.py、slide_outline.json、content_check.py（在生成內容之前訂好檢查規則）。

## [2026-11-24 19:53] lint | 第 1 次 Wiki Validation：未通過，errors=1 warnings=0 → retry

## [2026-11-24 19:53] organize | 修正（retry 1）：Wiki 修正 retry 1：W5 引文比對失敗——app-hybrid-tls 引用 S06 的一句話橫跨 p.34–35，中間夾著 NIST 的頁首（NIST SP 800-175B REV. 1 … This publication is available …），所以無法逐字比對。修正：把引文拆成 p.34 與 p.35 兩條逐字引文，內文標註改為 [S06 p.34–35]。

## [2026-11-24 19:53] lint | 第 2 次 Wiki Validation：通過，errors=0 warnings=0 → pass

## [2026-11-24 19:53] query | 為 12 張投影片查詢 Wiki；無結果：無

## [2026-11-24 20:05] fetch | 取得 12/12 篇來源

## [2026-11-24 20:05] ingest | 抽取文字 12/12 篇

## [2026-11-24 20:05] organize | incremental（retry 0）：增量模式：ingest 重新抽取文字，SHA-256 與 run-01 相同（來源未變），S04 連字遺失已由 ingest 警告並由 Lint 的 fi→f 摺疊處理；Wiki 頁面不需要更新。

## [2026-11-24 20:05] lint | 第 1 次 Wiki Validation：通過，errors=0 warnings=0 → pass

## [2026-11-24 20:05] query | 為 12 張投影片查詢 Wiki；無結果：無

## [2026-11-24 20:33] fetch | 取得 12/12 篇來源

## [2026-11-24 20:33] ingest | 抽取文字 12/12 篇

## [2026-11-24 20:33] organize | incremental（retry 0）：增量模式：Wiki 不需要更新（本次只改簡報外觀）。

## [2026-11-24 20:33] lint | 第 1 次 Wiki Validation：通過，errors=0 warnings=0 → pass

## [2026-11-24 20:33] query | 為 12 張投影片查詢 Wiki；無結果：無

## [2026-11-24 20:40] fetch | 取得 12/12 篇來源

## [2026-11-24 20:40] ingest | 抽取文字 12/12 篇

## [2026-11-24 20:42] organize | incremental（retry 0）：使用者回饋：加密／解密過程要有更多圖解，AES 四步要有具體實例。Wiki 更新：sym-aes 新增 FIPS 197 附錄 B（AES-128 第 1 輪）完整實例——初始 AddRoundKey、SubBytes、ShiftRows、MixColumns、AddRoundKey 各步的 4×4 state 與逐格說明（19→d4、列位移、04 = 02•d4 ⊕ 03•bf ⊕ 5d ⊕ 30、04 ⊕ a0 = a4），以及解密方向（反運算、倒序，§5.3）；新增 13 條原文引文、facts aes.example_input / aes.example_key。數值先以獨立 AES 參考實作（validators/aes_ref.py）重算，與附錄 B 全部一致。mode-cbc 新增解密公式與 SP 800-38A §6.2 解密原文；mode-ctr 補上解密公式與完整原文。S04 來源頁補充 §5.3 與 Appendix B。

## [2026-11-24 20:42] lint | 第 1 次 Wiki Validation：通過，errors=0 warnings=0 → pass

## [2026-11-24 20:42] query | 為 12 張投影片查詢 Wiki；無結果：無

## [2026-11-24 20:50] fetch | 取得 12/12 篇來源

## [2026-11-24 20:51] ingest | 抽取文字 12/12 篇

## [2026-11-24 20:51] organize | incremental（retry 0）：增量模式：Wiki 不需更新。

## [2026-11-24 20:51] lint | 第 1 次 Wiki Validation：通過，errors=0 warnings=0 → pass

## [2026-11-24 20:51] query | 為 12 張投影片查詢 Wiki；無結果：無

## [2026-11-24 21:05] fetch | 取得 14/15 篇來源；失敗 ['S15']

## [2026-11-24 21:06] ingest | 抽取文字 14/15 篇；失敗 ['S15']

## [2026-11-24 21:06] fetch | 取得 15/15 篇來源

## [2026-11-24 21:07] ingest | 抽取文字 15/15 篇

## [2026-11-24 21:09] organize | batch 6 教學補充：基礎工具與別人怎麼教：Batch 6（使用者回饋：名詞要先解釋、看別人怎麼介紹加密）：新增來源 S13 The Joy of Cryptography（Oregon State 大學部教科書）、S14 Crypto 101（入門書）、S15 Cloudflare What is encryption?（給大眾的說明）。新增節點 basics-bits-xor-mod（位元、位元組、十六進位、XOR、mod，含定義與例子）與 teaching-how-others-explain（比較三種教材的介紹順序，歸納本簡報的 5 條教學原則：先介紹工具與名詞、每個主題依『原理→為什麼／好處與限制→現實怎麼做』分頁講完、公式每個符號都要說明、從最簡單例子開始、用比喻再接回正式名詞）。classical-caesar、sym-aes、mode-cbc、asym-key-exchange、asym-rsa 的先備概念加入 basics-bits-xor-mod，讓 C5 會檢查『先介紹 mod／XOR 再使用』。knowledge_map 新增 T6。（batch lint：3 errors）

## [2026-11-24 21:10] organize | batch 6 教學補充：基礎工具與別人怎麼教：Batch 6 重做（batch lint 第 1 次未過）：v2 的 batch 快速檢查第一次在實際執行中攔下問題——3 條引文太短（少於 20 字元，無法有效比對）：FIPS 197 的 'Bit A binary digit: 0 or 1.'（刪除，位元定義改由 p.13 的完整句子支撐）、Joy of Cryptography 的 mod 例子（擴充為含 21 % 7 的完整例句）、目錄的 '0.2 Modular Arithmetic'（與上一條合併成連續的目錄片段）。（batch lint：通過）

## [2026-11-24 21:10] lint | 第 1 次 Wiki Validation：通過，errors=0 warnings=0 → pass

## [2026-11-24 21:10] query | 為 12 張投影片查詢 Wiki；無結果：無

## [2026-11-24 21:34] fetch | 取得 15/15 篇來源

## [2026-11-24 21:35] ingest | 抽取文字 15/15 篇

## [2026-11-24 21:35] organize | incremental（retry 0）：增量模式：使用者回饋『公式沒有用正常的數學排版』只影響簡報呈現，Wiki 不需更新。

## [2026-11-24 21:35] lint | 第 1 次 Wiki Validation：通過，errors=0 warnings=0 → pass

## [2026-11-24 21:35] query | 為 30 張投影片查詢 Wiki；無結果：無

## [2026-11-24 21:46] fetch | 取得 15/15 篇來源

## [2026-11-24 21:46] ingest | 抽取文字 15/15 篇

## [2026-11-24 21:46] organize | incremental（retry 0）：增量模式：使用者回饋『多一些起承轉合、章與章切換要提醒』屬於教學編排，Wiki 不需更新。這次先更新大綱（35 張，第 2～6 章開頭加承上啟下轉場頁）再讓 Graph 查詢，避免 run-07 的順序錯誤。

## [2026-11-24 21:46] lint | 第 1 次 Wiki Validation：通過，errors=0 warnings=0 → pass

## [2026-11-24 21:46] query | 為 35 張投影片查詢 Wiki；無結果：無
