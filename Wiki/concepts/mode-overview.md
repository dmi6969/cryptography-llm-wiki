---
id: mode-overview
title: 操作模式（Mode of Operation）：為什麼需要？IV 與填充
topic: T4
aliases: [mode of operation, modes of operation, 操作模式, 加密模式, initialization vector, IV, 初始向量, padding, 填充]
sources: [S03, S05]
prerequisites: [sym-block-vs-stream, sym-aes]
relations:
  - {type: related, target: mode-ecb}
  - {type: related, target: mode-cbc}
  - {type: related, target: mode-ctr}
facts:
  modes.sp800_38a: [ECB, CBC, CFB, OFB, CTR]
---

# 操作模式（Mode of Operation）

## 定義

區塊加密（如 AES）一次只能加密**一個固定大小的區塊**。訊息比一個區塊長時，就需要一套規則決定「區塊之間怎麼處理」——這就是**操作模式（mode of operation）** [S03 p.7]。
NIST SP 800-38A 定義了五種提供機密性的操作模式：**ECB、CBC、CFB、OFB、CTR** [S05 p.5]。

## 重點

- 最簡單的做法是把訊息切塊、各自加密，也就是 ECB；但它在多數應用中有缺點，因此才發展出其他模式 [S03 p.7]（見 [[mode-ecb]]）。
- **初始向量（IV, initialization vector）**：CBC、CFB、OFB 在加密時除了明文，還要輸入一個資料區塊 IV [S05 p.15]。
  - IV **不需要保密** [S05 p.15]；
  - 但 CBC／CFB 的 IV **必須無法預測**，OFB 每次都要用**不同的** IV [S05 p.15]。
- **填充（padding）**：ECB、CBC、CFB 要求明文長度是區塊大小的整數倍，不足時要在尾端補位元 [S05 p.24]。CTR 不需要（見 [[mode-ctr]]）。
- 本 Wiki 聚焦 ECB、CBC、CTR 三種，並補充以 CTR 為基礎、TLS 1.3 實際使用的 **GCM**（[[mode-gcm-aead]]）。

## 範例

| 模式 | 需要 IV／計數器？ | 需要填充？ | 加密可平行？ | 同樣明文區塊 → 同樣密文區塊？ |
|---|---|---|---|---|
| ECB | 否 | 是 | 是 | **是（洩漏圖樣）** |
| CBC | IV（不可預測） | 是 | 否（解密可以） | 否 |
| CTR | 計數器（不可重複） | 否 | 是 | 否 |

（整理自 [S05 p.15–24]、[S03 p.7–9]，各格依據見各模式頁。）

## 關聯

- [[mode-ecb]]、[[mode-cbc]]、[[mode-ctr]]、[[mode-gcm-aead]]
- 底層區塊加密：[[sym-aes]]

## 來源引文

- [S03 p.7 §7.2.2] "For messages exceeding n bits, the simplest approach is to partition the message into n-bit blocks and encrypt each separately."
- [S03 p.7 §7.2.2] "This electronic-codebook (ECB) mode has disadvantages in most applications, motivating other methods of employing block ciphers (modes of operation) on larger messages."
- [S05 p.5 Abstract] "This recommendation defines five confidentiality modes of operation for use with an underlying symmetric key block cipher algorithm: Electronic Codebook (ECB), Cipher Block Chaining (CBC), Cipher Feedback (CFB), Output Feedback (OFB), and Counter (CTR)."
- [S05 p.15 §5.3] "The input to the encryption processes of the CBC, CFB, and OFB modes includes, in addition to the plaintext, a data block called the initialization vector (IV), denoted IV."
- [S05 p.15 §5.3] "The IV need not be secret; however, for the CBC and CFB modes, the IV for any particular execution of the encryption process must be unpredictable, and, for the OFB mode, unique IVs must be used for each execution of the encryption process."
- [S05 p.24 App.A] "For the ECB, CBC, and CFB modes, the plaintext must be a sequence of one or more complete data blocks"
- [S05 p.24 App.A] "A common way to achieve the necessary increase is to append some extra bits, called padding, to the trailing end of the data string"
