---
id: mode-gcm-aead
title: GCM 與認證加密（Authenticated Encryption, AEAD）
topic: T4
aliases: [GCM, Galois/Counter Mode, AES-GCM, AEAD, authenticated encryption, 認證加密, authentication tag]
sources: [S05, S11]
prerequisites: [mode-ctr, intro-what-is-crypto]
relations:
  - {type: builds-on, target: mode-ctr}
  - {type: used-by, target: app-hybrid-tls}
facts:
  gcm.block_bits: 128
---

# GCM 與認證加密（AEAD）

## 定義

**GCM（Galois/Counter Mode）** 是一種**帶有附加資料的認證加密（authenticated encryption with associated data, AEAD）** 演算法 [S11 p.9]。
它建立在**區塊大小 128 位元**的經核准區塊加密（例如 AES）之上，所以 GCM 是 AES 的一種操作模式 [S11 p.9]。

## 重點

- **一次提供兩件事** [S11 p.9]：
  - **機密性**：使用 **CTR 模式的變形**來加密（見 [[mode-ctr]]）；
  - **真實性／完整性（authenticity）**：用一個通用雜湊函數計算**認證標籤（authentication tag）**。
- 加密時同時算出標籤；解密時**先驗證標籤，驗證通過才解密** [S11 p.15]。
- 這補上了 ECB／CBC／CTR 的缺口：前三者只提供**機密性**（SP 800-38A 稱它們為 confidentiality modes [S05 p.5]），無法偵測竄改——呼應密碼學四大目標中的「完整性」（[[intro-what-is-crypto]]）。
- **IV 不可重複**：同一把金鑰下只要有一個 IV 重複，就可能遭受偽造攻擊；NIST 說這個要求「幾乎和金鑰保密一樣重要」[S11 p.26]。
- 本頁只作為銜接 CTR 與 TLS 1.3 的橋樑（TLS 1.3 只使用 AEAD 演算法，見 [[app-hybrid-tls]]）。

## 範例

```
            ┌──────────── GCM ────────────┐
明文 ──▶   │ CTR 變形加密 → 密文          │ ──▶ 密文 + 標籤(tag)
附加資料 ─▶ │ GHASH 計算 → 認證標籤 tag     │
            └─────────────────────────────┘
接收方：先驗證 tag ✔ → 才解密；tag ✘ → 拒絕
```
（依 SP 800-38D §1、§5.2 的描述繪製 [S11 p.9][S11 p.15]）

## 關聯

- 建立在：[[mode-ctr]]
- 被 TLS 1.3 使用：[[app-hybrid-tls]]

## 來源引文

- [S11 p.9 §1] "This Recommendation specifies an algorithm called Galois/Counter Mode (GCM) for authenticated encryption with associated data."
- [S11 p.9 §1] "GCM is constructed from an approved symmetric key block cipher with a block size of 128 bits, such as the Advanced Encryption Standard (AES) algorithm"
- [S11 p.9 §1] "Thus, GCM is a mode of operation of the AES algorithm."
- [S11 p.9 §1] "GCM provides assurance of the confidentiality of data using a variation of the Counter mode of operation for encryption."
- [S11 p.9 §1] "GCM provides assurance of the authenticity of the confidential data"
- [S11 p.15 §5.2] "The authenticated encryption function encrypts the confidential data and computes an authentication tag on both the confidential data and any additional, non-confidential data."
- [S11 p.15 §5.2] "The authenticated decryption function decrypts the confidential data, contingent on the verification of the tag."
- [S11 p.26 §8] "if even one IV is ever repeated, then the implementation may be vulnerable to the forgery attacks"
- [S11 p.26 §8] "In practice, this requirement is almost as important as the secrecy of the key."
- [S05 p.5 Abstract] "This recommendation defines five confidentiality modes of operation for use with an underlying symmetric key block cipher algorithm"
