---
id: mode-ctr
title: CTR（Counter）模式
topic: T4
aliases: [CTR, Counter mode, 計數器模式, counter block, nonce]
sources: [S05]
prerequisites: [mode-overview, sym-block-vs-stream]
relations:
  - {type: part-of, target: mode-overview}
  - {type: contrasts-with, target: mode-cbc}
  - {type: builds-on, target: sym-block-vs-stream}
facts: {}
---

# CTR（Counter）模式

## 定義

**CTR**：不直接加密明文，而是用區塊加密去加密一連串的**計數器區塊（counter）** T₁, T₂, …，產生的輸出再和明文做 XOR，得到密文；解密時做同樣的事 [S05 p.22]。

- Oⱼ = E_K(Tⱼ)
- 加密：Cⱼ = Pⱼ ⊕ Oⱼ；解密：Pⱼ = Cⱼ ⊕ Oⱼ  [S05 p.22]

解密時一樣是「加密計數器」產生同一串 Oⱼ，再和密文 XOR，就把明文還原——**解密不需要區塊加密的反函數** [S05 p.22]。

等於把區塊加密變成「產生金鑰串流」的工具，用法很像串流加密（見 [[sym-block-vs-stream]]）。

## 重點

- **計數器絕對不可重複**：同一把金鑰下，**所有訊息**用過的計數器區塊都必須彼此不同 [S05 p.22]；每則訊息的初始計數器要選得能確保這種唯一性 [S05 p.26]。
- **加密與解密都可以平行**；任何一個區塊都能獨立解密 [S05 p.22]。
- **不需要填充**：最後一個區塊可以不滿，只取輸出區塊最前面需要的位元數做 XOR，其餘丟棄 [S05 p.22]。
- 解密也只用到區塊加密的「正向」函數 [S05 p.22]。
- TLS 1.3 使用的 **AES-GCM** 就是建立在 CTR 的變形之上（[[mode-gcm-aead]]）。

## 範例

```
 計數器： T1        T2        T3
          │         │         │
         E_K       E_K       E_K      ← 三個區塊可以同時算（平行）
          │         │         │
 P1 ──▶ (⊕)  P2 ──▶ (⊕)  P3 ──▶ (⊕)
          ▼         ▼         ▼
          C1        C2        C3
```
（依 SP 800-38A §6.5 公式繪製 [S05 p.22]）

## 常見誤解

- 「CTR 的計數器跟 IV 一樣，偶爾重複沒關係」——錯。SP 800-38A 要求同一金鑰下所有計數器都必須互不相同 [S05 p.22]。

## 關聯

- 對比：[[mode-cbc]]（需填充、加密不可平行）
- 延伸：[[mode-gcm-aead]]

## 來源引文

- [S05 p.22 §6.5] "The Counter (CTR) mode is a confidentiality mode that features the application of the forward cipher to a set of input blocks, called counters, to produce a sequence of output blocks that are exclusive-ORed with the plaintext to produce the ciphertext, and vice versa."
- [S05 p.22 §6.5] "The sequence of counters must have the property that each block in the sequence is different from every other block. This condition is not restricted to a single message: across all of the messages that are encrypted under the given key, all of the counters must be distinct."
- [S05 p.22 §6.5] "In CTR decryption, the forward cipher function is invoked on each counter block, and the resulting output blocks are exclusive-ORed with the corresponding ciphertext blocks to recover the plaintext blocks."
- [S05 p.22 §6.5] "For the last block, which may be a partial block of u bits, the most significant u bits of the last output block are used for the exclusive-OR operation; the remaining b-u bits of the last output block are discarded."
- [S05 p.22 §6.5] "In both CTR encryption and CTR decryption, the forward cipher functions can be performed in parallel"
- [S05 p.26 App.B.2] "The initial counter blocks, T1, for each message that is encrypted under the given key must be chosen in a manner than ensures the uniqueness of all the counter blocks across all the messages."
