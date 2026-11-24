---
id: S03
type: source
title: "Handbook of Applied Cryptography, Chapter 7: Block Ciphers"
url: https://cacr.uwaterloo.ca/hac/about/chap7.pdf
publisher: CRC Press（A. Menezes, P. van Oorschot, S. Vanstone）；University of Waterloo CACR 提供下載
year: 1996
nodes: [classical-caesar, classical-substitution, classical-transposition, classical-limitations, mode-overview, mode-ecb, mode-cbc]
---

# S03 — Handbook of Applied Cryptography, Ch.7 Block Ciphers

## 摘要

HAC 第 7 章討論區塊加密：一般概念與操作模式（§7.2）、古典密碼與其密碼分析（§7.3）、DES 等。
本 Wiki 用 §7.3 說明 **古典密碼的運作與弱點**（位移、替換、換位、Vigenère、頻率分析、Kasiski），
用 §7.2.2 補充 **操作模式的性質**（batch 4）。

## 本 Wiki 使用的章節

| 章節 | 抽取頁碼（= 書頁 − 221） | 用於節點 |
|---|---|---|
| §7.2.2 Modes of operation（ECB／CBC 性質、Remark 7.12） | p.7–9 | [[mode-overview]]、[[mode-ecb]]、[[mode-cbc]] |
| §7.3 Classical ciphers（導言） | p.16–17 | [[classical-limitations]] |
| §7.3.1 Transposition ciphers | p.17 | [[classical-transposition]] |
| §7.3.2 Substitution ciphers（Ex.7.48 Caesar、Note 7.50） | p.18–19 | [[classical-caesar]]、[[classical-substitution]] |
| §7.3.3 Vigenère | p.20 | [[classical-substitution]] |
| §7.3.5 Cryptanalysis of classical ciphers | p.24–27 | [[classical-limitations]] |

## 備註

- HAC 明言古典密碼「僅為歷史與教學目的」介紹，不適合實際使用 [S03 p.17]。
- 抽取時 Vigenère 的重音被拆成 "Vigen`ere"，Lint 比對前會先去除重音。
