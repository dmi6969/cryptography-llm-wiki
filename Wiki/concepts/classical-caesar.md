---
id: classical-caesar
title: Caesar Cipher（凱撒密碼／位移密碼）
topic: T2
aliases: [Caesar cipher, shift cipher, 凱撒密碼, 位移密碼]
sources: [S02, S03]
prerequisites: [intro-terminology, basics-bits-xor-mod]
relations:
  - {type: instance-of, target: classical-substitution}
  - {type: related, target: classical-limitations}
facts:
  caesar.key_count: 26
  caesar.julius_key: 3
---

# Caesar Cipher（凱撒密碼／位移密碼）

## 定義

**位移密碼（shift cipher）／Caesar 密碼**：把字母表中的每個字母**往後移動固定的 k 位**，是一種限定成「字母位移」的簡單替換密碼 [S03 p.18]。
用數字表示（A=0、B=1、…、Z=25）：

- 加密：c = (m + k) mod 26
- 解密：m = (c − k) mod 26  [S03 p.18]

金鑰就是位移量 k。傳說凱撒（Julius Caesar）使用 k = 3 [S03 p.18]。

## 重點

- 它是 **simple substitution（單表替換）** 的特例：整篇訊息都用同一套對應表 [S03 p.18]（見 [[classical-substitution]]）。
- 例：k = 1 時，HAL 加密成 IBM [S03 p.18]。
- HAC 第 1 章用「每個字母往右移 3 位」當作對稱式加密的入門範例，加密與解密用的是同一個祕密（位移量）[S02 p.16]。
- **致命弱點**：英文只有 26 種位移（s = 26），攻擊者把所有金鑰試一遍就能破解 [S03 p.18]（見 [[classical-limitations]]、[[intro-kerckhoffs]]）。

## 範例

```
k = 3
明文：H  E  L  L  O
      ↓+3 ↓+3 ↓+3 ↓+3 ↓+3
密文：K  H  O  O  R
```
（HELLO → KHOOR 由本 Wiki 以公式 c = (m + 3) mod 26 計算，簡報驗證節點會用程式重算。）

## 常見誤解

- 「Caesar 密碼有 25 或 26 把金鑰，所以算安全」——錯。金鑰空間只有 26，用手就能窮舉 [S03 p.18]。

## 關聯

- 是 [[classical-substitution]] 的一種
- 弱點分析：[[classical-limitations]]

## 來源引文

- [S03 p.18 §7.3.2 Ex.7.48] "A shift cipher is a simple substitution cipher with the permutation e constrained to an alphabetic shift through k characters for some fixed k."
- [S03 p.18 §7.3.2 Ex.7.48] "For English text, s = 26, and characters A through Z are associated with integers 0 through 25."
- [S03 p.18 §7.3.2 Ex.7.48] "For k = 1, the message m = HAL is encrypted to c = IBM. According to folklore, Julius Caesar used the key k = 3."
- [S03 p.18 §7.3.2] "The shift cipher can be trivially broken because there are only s"
- [S03 p.18 §7.3.2] "keys (e.g., s = 26) to exhaustively search."
- [S02 p.16 §1.5 Ex.1.25] "suppose that the key e is chosen to be the permutation which maps each letter to the one which is three positions to its right"
