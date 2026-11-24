---
id: classical-limitations
title: 古典密碼的限制：金鑰空間太小與頻率分析
topic: T2
aliases: [frequency analysis, 頻率分析, classical cipher weaknesses, redundancy, Kasiski]
sources: [S02, S03]
prerequisites: [classical-caesar, classical-substitution, classical-transposition, intro-kerckhoffs]
relations:
  - {type: limitation-motivates, target: sym-aes}
  - {type: related, target: intro-kerckhoffs}
facts:
  caesar.key_count: 26
---

# 古典密碼的限制：金鑰空間太小與頻率分析

## 定義

**古典密碼**指在二十世紀後半以前發明、流傳已久的加密技術，大多是簡單替換與簡單換位的變形 [S03 p.16]。
HAC 明確指出：這些技術**在今天只具歷史與教學價值**，無法抵抗現代密碼分析，**不適合實際使用** [S03 p.17]。

## 重點

1. **金鑰空間太小 → 暴力破解**：位移密碼只有 26 把金鑰，可以輕易窮舉 [S03 p.18]（見 [[intro-kerckhoffs]]）。
2. **頻率分析**：自然語言有冗餘，例如英文中 E 遠比 Z 常見、Q 後面幾乎都是 U [S03 p.24]。單表替換不會改變整體的字母頻率分布，所以把密文字母頻率和語言的字母頻率表比對，就能對應回明文字母 [S03 p.18]。
3. **金鑰空間大也不夠**：英文單表替換有 26! 把金鑰，仍可透過頻率被破解 [S02 p.18]；經驗上大約 **25 個密文字元**就足以讓熟練的分析者還原明文 [S03 p.25]。HAC 的結論：金鑰空間夠大是安全的**必要條件，但通常不是充分條件** [S02 p.22]。
4. **換位密碼**保留了每種字元的出現次數，一樣容易被分析 [S02 p.19][S03 p.17]。
5. **多表替換（Vigenère）**：找出金鑰長度後，可以分組做頻率分析 [S02 p.19]；Kasiski 方法利用重複的密文片段推出金鑰長度 [S03 p.26]。

**→ 現代密碼學的教訓**：需要**巨大的金鑰空間**，而且密文**不能洩漏明文的統計特徵**。這正是 AES 這類現代區塊加密的設計目標（[[sym-aes]]）。

## 範例

- Caesar 密文「KHOOR」：把 25 種位移逐一試過，就會看到唯一有意義的「HELLO」（本 Wiki 教學補充，依據 [S03 p.18] 的窮舉說法）。

## 關聯

- 被分析的對象：[[classical-caesar]]、[[classical-substitution]]、[[classical-transposition]]
- 促成現代設計：[[sym-aes]]

## 來源引文

- [S03 p.16 §7.3] "The term classical ciphers refers to encryption techniques which have become well-known over time, and generally created prior to the second half of the twentieth century"
- [S03 p.16 §7.3] "Many classical techniques are variations of simple substitution and simple transposition."
- [S03 p.17 §7.3] "However, since these techniques are neither sophisticated nor secure against current cryptanalytic capabilities, they are not generally suitable for practical use."
- [S03 p.18 §7.3.2] "The shift cipher can be trivially broken because there are only s"
- [S03 p.18 §7.3.2 Note 7.50] "Mono-alphabetic substitution alters the frequency of individual plaintext characters, but does not alter the frequency distribution of the overall character set."
- [S03 p.18 §7.3.2 Note 7.50] "comparing ciphertext character frequencies to a table of expected letter frequencies (unigram statistics) in the plaintext language allows associations between ciphertext and plaintext characters."
- [S03 p.24 §7.3.5] "All natural languages are redundant."
- [S03 p.24 §7.3.5] "in English the letter 'E' appears far more frequently than 'Z', 'Q' is almost always followed by 'U'"
- [S03 p.25 §7.3.5 Fact 7.68] "as few as 25 ciphertext characters suffices to allow a skilled cryptanalyst to recover the plaintext."
- [S03 p.26 §7.3.5] "Kasiski's method provides a general technique for cryptanalyzing polyalphabetic ciphers with repeated keywords"
- [S02 p.18 §1.5.2] "yet the key being used can be determined quite easily by examining a modest amount of ciphertext."
- [S02 p.19 §1.5.2] "a frequency analysis can be done on each group."
- [S02 p.22 §1.5.5 Fact 1.40] "A necessary, but usually not sufficient, condition for an encryption scheme to be secure is that the key space be large enough to preclude exhaustive search."
- [S02 p.19 §1.5.2] "A simple transposition cipher preserves the number of symbols of a given type within a block, and thus is easily cryptanalyzed."
