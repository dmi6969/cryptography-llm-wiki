---
id: classical-substitution
title: 替換密碼（Substitution Cipher）：單表、同音、多表（Vigenère）
topic: T2
aliases: [substitution cipher, mono-alphabetic substitution, polyalphabetic substitution, Vigenère cipher, homophonic substitution, 替換密碼, 多表替換]
sources: [S02, S03]
prerequisites: [intro-terminology]
relations:
  - {type: contrasts-with, target: classical-transposition}
  - {type: related, target: classical-limitations}
  - {type: part-of, target: sym-block-vs-stream}
facts:
  substitution.key_count_english: "26!"
---

# 替換密碼（Substitution Cipher）

## 定義

**替換密碼**：把符號（或一組符號）**換成其他符號**，字母的位置不變 [S02 p.18]。

## 重點

- **單表替換（simple / mono-alphabetic substitution）**：整篇用同一張對應表（字母表的一個排列）替換每個字母 [S02 p.18][S03 p.18]。Caesar 是其中「只能位移」的特例（[[classical-caesar]]）。
- 英文單表替換的金鑰數是 **26!**（約 4 × 10²⁶），金鑰空間非常大 [S02 p.18]——**但仍不安全**：字母頻率分布會原封不動留在密文裡，只要觀察適量密文就能推出金鑰 [S02 p.18]。
- **同音替換（homophonic）**：一個明文字母可對應多個密文符號、隨機挑選，用來把密文字母頻率「拉平」，代價是密文變長 [S02 p.19][S03 p.19]。
- **多表替換（polyalphabetic）**：不同位置使用不同的對應表，同一個明文字母會變成不同密文字母 [S03 p.20]。**Vigenère 密碼**就是輪流使用 t 個位移密碼（t 為金鑰長度）[S03 p.20]。
- 多表替換**沒有難破很多**：一旦找出金鑰長度 t，就能把密文分成 t 組，每組各自做頻率分析 [S02 p.19]；Kasiski 方法可用重複出現的密文片段推出金鑰長度 [S03 p.26–27]。

## 範例

HAC 的 Vigenère 例子（t = 3，三個位移量為 3、7、10）[S02 p.19]：

```
明文：THI SCI PHE RIS CER TAI NLY NOT SEC URE
密文：WOS VJS SOO UPC FLB WHS QSI QVD VLM XYO
```
同一個字母 E 被加密成 O 和 L 兩種結果 [S02 p.19]。

## 常見誤解

- 「金鑰空間有 26! 那麼大，一定安全」——錯。HAC 指出單表替換即使金鑰空間極大，仍可用頻率分析輕易破解 [S02 p.18]。

## 關聯

- 對比：[[classical-transposition]]（換位置，不換字母）
- 弱點：[[classical-limitations]]
- 替換與換位是區塊加密的兩個基本類別：[[sym-block-vs-stream]]

## 來源引文

- [S02 p.18 §1.5.2] "Substitution ciphers are block ciphers which replace symbols (or groups of symbols) by other symbols or groups of symbols."
- [S02 p.18 §1.5.2] "Ee is called a simple substitution cipher or a mono-alphabetic substitution cipher."
- [S02 p.18 §1.5.2] "Simple substitution ciphers over small block sizes provide inadequate security even when the key space is extremely large."
- [S02 p.18 §1.5.2] "If the alphabet is the English alphabet as in Example 1.25, then the size of the key space is 26!"
- [S02 p.18 §1.5.2] "This follows from the simple observation that the distribution of letter frequencies is preserved in the ciphertext."
- [S02 p.19 §1.5.2] "A homophonic cipher can be used to make the frequency of occurrence of ciphertext symbols more uniform, at the expense of data expansion."
- [S02 p.19 §1.5.2 Ex.1.31] "m = THI SCI PHE RIS CER TAI NLY NOT SEC URE"
- [S02 p.19 §1.5.2 Ex.1.31] "c = Ee(m) = WOS VJS SOO UPC FLB WHS QSI QVD VLM XYO"
- [S02 p.19 §1.5.2] "Polyalphabetic ciphers have the advantage over simple substitution ciphers that symbol frequencies are not preserved. In the example above, the letter E is encrypted to both O and L."
- [S02 p.19 §1.5.2] "However, polyalphabetic ciphers are not significantly more difficult to cryptanalyze, the approach being similar to the simple substitution cipher."
- [S03 p.18 §7.3.2] "A simple substitution cipher or mono-alphabetic substitution cipher employs a permutation e over A"
- [S03 p.19 §7.3.2] "Homophonic substitution results in ciphertext data expansion."
- [S03 p.20 §7.3.3] "Under different alphabets, the same plaintext character is thus encrypted to different ciphertext characters, precluding simple frequency analysis as per mono-alphabetic substitution"
- [S03 p.20 §7.3.3] "The simple Vigenère uses t shift ciphers (see Example 7.48)"
- [S03 p.26 §7.3.5] "Kasiski's method provides a general technique for cryptanalyzing polyalphabetic ciphers with repeated keywords, such as the simple Vigenère cipher"
