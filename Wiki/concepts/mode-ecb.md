---
id: mode-ecb
title: ECB（Electronic Codebook）模式
topic: T4
aliases: [ECB, Electronic Codebook, 電子密碼本]
sources: [S03, S05]
prerequisites: [mode-overview]
relations:
  - {type: part-of, target: mode-overview}
  - {type: contrasts-with, target: mode-cbc}
  - {type: contrasts-with, target: mode-ctr}
facts: {}
---

# ECB（Electronic Codebook）模式

## 定義

**ECB**：在同一把金鑰下，每個明文區塊都對應到一個固定的密文區塊，就像查「密碼本」一樣 [S05 p.16]。
加密時，把區塊加密函數**直接、獨立地**套用到每一個明文區塊 [S05 p.16]：Cⱼ = E_K(Pⱼ)。

## 重點

- **致命缺點：洩漏圖樣**——同一把金鑰下，相同的明文區塊**永遠**加密成相同的密文區塊 [S05 p.16–17][S03 p.7]。HAC：區塊加密本身不會隱藏資料圖樣 [S03 p.7]。
- NIST：如果這個性質在應用中不可接受，就**不應該使用 ECB** [S05 p.17]；HAC：ECB **不建議用於超過一個區塊的訊息** [S03 p.7]。
- 區塊彼此獨立：攻擊者重排或替換密文區塊，解密出的明文也會跟著被重排／替換 [S03 p.7]。
- 優點只有簡單、可平行運算 [S05 p.16]。
- ECB 要求明文是完整區塊，需要填充 [S05 p.24]。

## 範例

```
明文區塊：  [AAAA] [BBBB] [AAAA] [AAAA]
ECB 密文：  [X7#q] [p2@L] [X7#q] [X7#q]   ← 重複的明文 → 重複的密文，圖樣外洩
```
（示意。簡報中會用一張簡單圖片示範：ECB 加密後仍看得出輪廓，CBC/CTR 則看起來像雜訊。）

## 常見誤解

- 「用了 AES 就安全，模式不重要」——錯。AES 搭配 ECB 時，重複的明文區塊仍會產生重複的密文區塊 [S05 p.16–17]，攻擊者看得出資料的結構。

## 關聯

- 對比：[[mode-cbc]]（用 IV 與鏈結打破重複）、[[mode-ctr]]（用計數器）

## 來源引文

- [S05 p.16 §6.1] "The Electronic Codebook (ECB) mode is a confidentiality mode that features, for a given key, the assignment of a fixed ciphertext block to each plaintext block, analogous to the assignment of code words in a codebook."
- [S05 p.16 §6.1] "In ECB encryption, the forward cipher function is applied directly and independently to each block of the plaintext."
- [S05 p.16 §6.1] "In ECB encryption and ECB decryption, multiple forward cipher functions and inverse cipher functions can be computed in parallel."
- [S05 p.16 §6.1] "In the ECB mode, under a given key, any given plaintext block always gets encrypted to the"
- [S05 p.17 §6.1] "same ciphertext block. If this property is undesirable in a particular application, the ECB mode should not be used."
- [S05 p.24 App.A] "For the ECB, CBC, and CFB modes, the plaintext must be a sequence of one or more complete data blocks"
- [S03 p.7 §7.2.2] "Identical plaintext blocks (under the same key) result in identical ciphertext."
- [S03 p.7 §7.2.2] "Re-ordering ciphertext blocks results in correspondingly re-ordered plaintext blocks."
- [S03 p.7 §7.2.2 Remark 7.12] "Furthermore, block ciphers do not hide data patterns – identical ciphertext blocks imply identical plaintext blocks. For this reason, the ECB mode is not recommended for messages longer than one block"
