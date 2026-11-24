---
id: asym-key-exchange
title: Diffie–Hellman 金鑰交換（Key Exchange）
topic: T5
aliases: [Diffie-Hellman, DH, key exchange, key agreement, public key distribution, ECDHE, (EC)DHE, 金鑰交換, 金鑰協商]
sources: [S02, S07, S08, S10]
prerequisites: [asym-public-key, basics-bits-xor-mod]
relations:
  - {type: part-of, target: asym-public-key}
  - {type: used-by, target: app-hybrid-tls}
  - {type: contrasts-with, target: asym-rsa}
facts: {}
---

# Diffie–Hellman 金鑰交換

## 定義

**公開金鑰分配（public key distribution）／金鑰交換**：兩個人在**公開、可被竊聽的通道**上來回交換資訊，最後得到**同一把共享金鑰**；竊聽者即使看到全部交換內容，也無法在可行的計算量內算出這把金鑰 [S07 p.1]。
Diffie 與 Hellman 在 1976 年提出了這種方法，其安全性建立在**離散對數問題**的困難度上 [S02 p.3][S07 p.6]。

## 重點

- 目的：**不需要事先的安全通道**就能建立對稱式金鑰，解決金鑰分配問題 [S07 p.1]（見 [[sym-concept]]）。
- 做法（概念）[S07 p.6]：
  1. 公開一個質數 q 與一個基底 α；
  2. 每個人各自挑一個**祕密的隨機數** X，只公開 Y = α^X mod q；
  3. 雙方用「對方公開的 Y」與「自己的祕密 X」，各自算出相同的 K。
- 由 X 算 Y 很容易，**由 Y 反推 X（取對數）很難**——系統的安全性正取決於這個困難度 [S07 p.6]。
- 它和 RSA 不同：DH 是讓兩人**協議出一把金鑰**，再拿去給一般的（對稱式）密碼系統使用 [S08 p.7]。
- **現代應用**：TLS 1.3 的金鑰交換模式之一就是 **(EC)DHE**——建立在有限體或橢圓曲線上的 Diffie–Hellman [S10 p.10]（見 [[app-hybrid-tls]]）。

## 範例

小數字教學範例（本 Wiki 依 [S07 p.6] 的公式自行計算，簡報驗證節點會用程式重算；實務上 q 要非常大）：

```
公開：q = 23，α = 5
Alice 祕密 X_A = 4 → 公開 Y_A = 5^4 mod 23 = 4
Bob   祕密 X_B = 3 → 公開 Y_B = 5^3 mod 23 = 10
Alice 算：K = Y_B^X_A mod 23 = 10^4 mod 23 = 18
Bob   算：K = Y_A^X_B mod 23 = 4^3  mod 23 = 18   ← 兩人得到同一把金鑰
竊聽者只看到 23、5、4、10，要算出 18 必須先解離散對數
```

## 關聯

- 屬於：[[asym-public-key]]
- 被 TLS 1.3 使用：[[app-hybrid-tls]]
- 與 RSA 的差別：[[asym-rsa]]

## 來源引文

- [S07 p.1 §I] "Public key distribution systems offer a different approach to eliminating the need for a secure key distribution channel. In such a system, two users who wish to exchange a key communicate back and forth until they arrive at a key in common."
- [S07 p.1 §I] "A third party eavesdropping on this exchange must find it computationally infeasible to compute the key from the information overheard"
- [S07 p.6 §III] "The new technique makes use of the apparent difficulty of computing logarithms over a finite field GF(q) with a prime number q of elements."
- [S07 p.6 §III] "The security of our technique depends crucially on the difficulty of computing logarithms mod q"
- [S07 p.6 §III] "Each user generates an independent random number"
- [S07 p.6 §III] "Each keeps Xi secret, but places"
- [S02 p.3 §1.1] "for key exchange, the security of which is based on the intractability of the discrete logarithm problem."
- [S08 p.7 §V] "Their technique permits two users to determine a key in common to be used in a normal cryptographic system."
- [S10 p.10 §2] "TLS supports three basic key exchange modes"
- [S10 p.10 §2] "(EC)DHE (Diffie-Hellman over either finite fields or elliptic curves)"
