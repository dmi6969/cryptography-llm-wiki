---
id: basics-bits-xor-mod
title: 基礎工具：位元、位元組、十六進位、XOR 與 mod
topic: T6
aliases: [bit, byte, hexadecimal, XOR, exclusive-or, mod, modular arithmetic, remainder, 位元, 位元組, 十六進位, 互斥或, 取餘數, 模運算]
sources: [S04, S08, S13, S14]
prerequisites: [intro-terminology]
relations:
  - {type: used-by, target: classical-caesar}
  - {type: used-by, target: sym-aes}
  - {type: used-by, target: mode-cbc}
  - {type: used-by, target: asym-rsa}
facts: {}
---

# 基礎工具：位元、位元組、十六進位、XOR 與 mod

## 定義

| 名詞 | 意思 | 例子 | 來源 |
|---|---|---|---|
| **位元（bit）** | 一個二進位數字，只能是 0 或 1 | `1` | [S04 p.10][S04 p.13] |
| **位元組（byte）** | 8 個位元排在一起 | `10100011` | [S04 p.10][S04 p.13] |
| **十六進位（hexadecimal）** | 用 0–9、a–f 共 16 個字元，每個字元代表 4 個位元；一個位元組剛好寫成 2 個字元 | `10100011` 寫成 `a3` | [S04 p.13] |
| **XOR（互斥或，符號 ⊕）** | 兩個位元**不同**得 1、**相同**得 0；兩串等長的位元就逐位做 | `0011 ⊕ 0101 = 0110` | [S14 p.17][S13 p.15] |
| **mod（取餘數）** | `a mod n` = a 除以 n 的**餘數** | `20 mod 7 = 6` | [S13 p.13][S08 p.1] |

## 重點

- AES 處理資料的基本單位是**位元組**；AES 的一個區塊是 128 個位元 = 16 個位元組 [S04 p.13]。
- FIPS 197 用十六進位寫位元組，例如 `{10100011}` 寫成 `{a3}` [S04 p.13]。這就是 AES 實例中 `32 43 f6 a8…` 這種寫法的意思（見 [[sym-aes]]）。
- **XOR 的兩個性質**讓它很適合加密 [S13 p.15]：
  - 自己和自己 XOR 會變成 0：x ⊕ x = 0
  - 和 0 XOR 不會改變：x ⊕ 0 = x
  - 所以「明文 ⊕ 金鑰 = 密文」之後，「密文 ⊕ 同一把金鑰 = 明文」——**同一個動作就能加密也能解密**（本 Wiki 由上面兩個性質推得）。
- **mod** 讓數字「繞一圈回來」，像時鐘：Caesar 密碼用 mod 26 讓 Z 之後回到 A（[[classical-caesar]]）；RSA 的加密就是「算次方後除以 n 取餘數」[S08 p.1]（[[asym-rsa]]）。
- a mod n 的結果一定介於 0 到 n−1 之間 [S13 p.13]。

## 範例

```
XOR（逐位：相同→0，不同→1）        mod（取餘數）
  0011                               20 mod 7 = 6   （20 = 2×7 + 6）
⊕ 0101                               27 mod 26 = 1  （Caesar：Y(24) + 3 = 27 → 1 = B）
= 0110
```
（左：[S13 p.15] 的例子；右上：[S13 p.13] 的例子；右下為本 Wiki 依 Caesar 公式計算的教學例）

## 關聯

- 用到 mod：[[classical-caesar]]、[[asym-rsa]]、[[asym-key-exchange]]
- 用到 XOR、位元組、十六進位：[[sym-aes]]、[[mode-cbc]]、[[mode-ctr]]

## 來源引文

- [S04 p.10 §2.1] "Byte A sequence of eight bits."
- [S04 p.13 §3.2] "The basic processing unit in the AES algorithms is the byte — a sequence of eight bits."
- [S04 p.13 §3.1] "A bit is a binary digit — 0 or 1. A block is a sequence of 128 bits"
- [S04 p.13 §3.2] "It is also convenient to denote byte values using hexadecimal notation. The 16 hexadecimal characters represent sequences of four bits"
- [S04 p.13 §3.2] "For example, the hexadecimal form of the byte {10100011} is {a3}."
- [S14 p.17 §5.1] "is true when either the first input or the second input, but not both, are true."
- [S14 p.17 §5.1] "In mathematics and cryptography papers, exclusive or is generally represented by a cross in a circle"
- [S13 p.15 Def.0.5] "to denote the bitwise exclusive-or"
- [S13 p.15 Def.0.5] "For example, 0011 ⊕ 0101 = 0110."
- [S13 p.15 Def.0.5] "ing a string with itself results in zeroes."
- [S13 p.13 Def.0.2] "The expression a % n (usually read as “a mod n”) represents the remainder after dividing a by n."
- [S13 p.13 Def.0.2] "Example 21 % 7 = 0 because 21 = 3 · 7 + 0. 20 % 7 = 6 because 20 = 2 · 7 + 6."
- [S08 p.1 Abstract] "and then taking the remainder when the result is divided by the publicly specified product, n"
