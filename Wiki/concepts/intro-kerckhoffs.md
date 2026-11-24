---
id: intro-kerckhoffs
title: Kerckhoffs 原則、金鑰空間與暴力破解
topic: T1
aliases: [Kerckhoffs' principle, Kerckhoffs, exhaustive search, brute force, security by obscurity, 暴力破解, 窮舉搜尋]
sources: [S01, S02]
prerequisites: [intro-terminology]
relations:
  - {type: related, target: classical-limitations}
  - {type: related, target: sym-aes}
facts:
  kerckhoffs.year: 1883
---

# Kerckhoffs 原則、金鑰空間與暴力破解

## 定義

**Kerckhoffs 原則**：密碼系統的設計（演算法）可以公開，**安全性只應建立在金鑰的保密上** [S02 p.15]。
這是 Kerckhoffs 在 1883 年提出的六項要求中的第 2 點 [S02 p.15]。

## 重點

- 密碼學的基本前提：演算法、明文／密文空間等都是公開的，通訊雙方**唯一要保密的是所用的金鑰** [S02 p.15]。
- 歷史證明，想把演算法本身保密非常困難 [S02 p.15]；RFC 4949 也指出「靠隱藏設計來求安全（security by obscurity）」在密碼學界早已不被接受 [S01 p.268]。
- 只靠公開、經過長期同儕審查的演算法；例如 NIST 以**公開程序**選出 AES 取代 DES [S01 p.268]。
- **暴力破解／窮舉搜尋（exhaustive search, brute force）**：把每一把可能的金鑰都試一遍 [S02 p.15][S01 p.41]。
- 因此**金鑰空間必須夠大**，讓窮舉在計算上不可行 [S02 p.15]。
- 「破解」的時間尺度取決於資料要保密多久：股票交易指令可能只需保密幾分鐘，國家機密可能要永久保密 [S02 p.15]。

## 範例

- 鎖匠都知道門鎖的構造（演算法公開），但沒有你的鑰匙（金鑰）仍打不開——本 Wiki 的教學比喻，對應 Kerckhoffs 第 2 點 [S02 p.15]。
- 金鑰空間對比：Caesar 密碼只有 25 種有意義的位移（[[classical-caesar]]），AES-128 有 2^128 種金鑰（[[sym-aes]]）。

## 關聯

- 金鑰空間太小是古典密碼的致命傷：[[classical-limitations]]
- 現代密碼（AES）是公開徵選的：[[sym-aes]]

## 來源引文

- [S02 p.15 §1.4] "When two parties wish to communicate securely using an encryption scheme, the only thing that they keep secret is the particular key pair (e, d) which they are using"
- [S02 p.15 §1.4] "History has shown that maintaining the secrecy of the transformations is very difficult indeed."
- [S02 p.15 §1.4] "This is called an exhaustive search of the key space."
- [S02 p.15 §1.4] "the number of keys (i.e., the size of the key space) should be large enough to make this approach computationally infeasible."
- [S02 p.15 §1.4] "compromise of the system details should not inconvenience the correspondents"
- [S02 p.15 §1.4] "This list of requirements was articulated in 1883 and, for the most part, remains useful today."
- [S02 p.15 §1.4] "Point 2 allows that the class of encryption transformations being used be publicly known and that the security of the system should reside only in the key chosen."
- [S02 p.15 §1.4] "For example, an instruction to buy a certain stock may only need to be kept secret for a few minutes whereas state secrets may need to remain confidential indefinitely."
- [S01 p.41 brute force] "A cryptanalysis technique or other kind of attack method involving an exhaustive procedure that tries a large number of possible solutions to the problem."
- [S01 p.268 security by obscurity] "This approach has long been discredited in cryptography, where the phrase refers to trying to keep an algorithm secret, rather than just concealing the keys"
- [S01 p.268 security by obscurity] "For example, NIST used a long, public process to select AES to replace DES."
