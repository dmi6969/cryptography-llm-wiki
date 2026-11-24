---
id: classical-transposition
title: 換位密碼（Transposition Cipher）
topic: T2
aliases: [transposition cipher, permutation cipher, 換位密碼, 置換密碼]
sources: [S02, S03]
prerequisites: [intro-terminology]
relations:
  - {type: contrasts-with, target: classical-substitution}
  - {type: related, target: classical-limitations}
  - {type: part-of, target: sym-block-vs-stream}
facts: {}
---

# 換位密碼（Transposition Cipher）

## 定義

**簡單換位密碼**：不改變字母本身，只**重新排列一個區塊內字母的位置** [S02 p.19]。
把明文分成每 t 個字元一組，對每組套用同一個排列 e（1～t 的一種排列）；解密時用反向排列 [S03 p.17]。

## 重點

- 金鑰是排列 e；週期為 t 時，金鑰空間大小為 t! [S03 p.17]。
- HAC 例子：t = 6、e = (6 4 1 3 5 2)，CAESAR 加密成 RSCEAA，解密用反排列 (3 6 4 2 5 1) [S03 p.17]。
- **弱點**：換位只改位置，**每種字母出現的次數完全不變**，因此很容易被分析 [S02 p.19]；也因為保留了字元頻率分布，很容易被辨認出是換位密碼 [S03 p.17]。
- 替換與換位單獨使用的安全性都不高，但兩者組合（product cipher）是現代區塊加密設計的基礎概念之一 [S02 p.20]（見 [[sym-block-vs-stream]]）。

## 範例

```
位置： 1 2 3 4 5 6
明文： C A E S A R
e = (6 4 1 3 5 2)：依序取第 6、4、1、3、5、2 個字母
密文： R S C E A A
```
[S03 p.17]

## 關聯

- 對比：[[classical-substitution]]（換字母，不換位置）
- 弱點：[[classical-limitations]]

## 來源引文

- [S02 p.19 §1.5.2] "Another class of symmetric-key ciphers is the simple transposition cipher, which simply permutes the symbols in a block."
- [S02 p.19 §1.5.2] "A simple transposition cipher preserves the number of symbols of a given type within a block, and thus is easily cryptanalyzed."
- [S03 p.17 §7.3.1] "For a simple transposition cipher with fixed period t, encryption involves grouping the plaintext into blocks of t characters, and applying to each block a single permutation e on the numbers 1 through t."
- [S03 p.17 §7.3.1] "the key space K has cardinality t! for a given value t."
- [S03 p.17 §7.3.1 Ex.7.43] "The message m = CAESAR is encrypted to c = RSCEAA."
- [S03 p.17 §7.3.1 Note 7.47] "they are easily recognized because they preserve the frequency distribution of each character."
- [S02 p.20 §1.5.3] "Simple substitution and transposition ciphers individually do not provide a very high level"
