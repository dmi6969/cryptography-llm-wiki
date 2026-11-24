---
id: sym-concept
title: 對稱式加密（Symmetric Encryption）與金鑰分配問題
topic: T3
aliases: [symmetric-key encryption, symmetric encryption, secret key, secret-key algorithm, 對稱式加密, 祕密金鑰, key distribution problem, 金鑰分配問題]
sources: [S02, S06]
prerequisites: [intro-terminology, intro-kerckhoffs]
relations:
  - {type: related, target: sym-block-vs-stream}
  - {type: limitation-motivates, target: asym-public-key}
  - {type: contrasts-with, target: asym-public-key}
facts: {}
---

# 對稱式加密（Symmetric Encryption）

## 定義

**對稱式金鑰演算法**（又稱 secret-key algorithm）用**同一把金鑰**加上保護、也解除保護：加密用的金鑰，同時也是解密用的金鑰 [S06 p.30–31]。
這把金鑰稱為 **secret key（祕密金鑰）**，又稱 symmetric key [S06 p.18]。
HAC 的定義：知道加密金鑰 e 就能輕易算出解密金鑰 d（反之亦然），而實務上大多 **e = d** [S02 p.16]。

## 重點

- **金鑰必須保密**，資料才會受到保護 [S06 p.31]；因為 d 能從 e 推出，加密金鑰 e 也必須保密 [S02 p.17]。
- 用途：加密以提供**機密性**、訊息鑑別以確保**完整性與來源**、金鑰衍生、金鑰包裝、亂數產生 [S06 p.31]。
- **金鑰分配問題（key distribution problem）**：雙方要先用**安全的方式**協議並交換金鑰，這是對稱式系統的主要難題之一 [S02 p.17]。
- **金鑰數量爆炸**：每一對通訊者都要一把不同的金鑰。4 個人需要 6 把；**1,000 個人需要 499,500 把** [S06 p.31]。
- 對稱式加密分成兩大類：**區塊加密（block cipher）** 與 **串流加密（stream cipher）** [S02 p.17]（見 [[sym-block-vs-stream]]）。
- 古典密碼（Caesar、替換、換位）都屬於對稱式加密 [S02 p.16][S02 p.19]。

## 範例

```
Alice ──[同一把金鑰 K 加密]──▶ 密文 ──(不安全通道)──▶ Bob [同一把金鑰 K 解密]
          ▲                                                    ▲
          └────────── K 必須事先經由「安全通道」交給 Bob ──────────┘
```
（依 HAC 圖 1.7「加上一條安全通道來交換金鑰」改繪 [S02 p.17]）

n 個人兩兩通訊所需金鑰數 = n(n−1)/2：4 → 6、1,000 → 499,500 [S06 p.31]。

## 關聯

- 兩大類型：[[sym-block-vs-stream]]；代表演算法：[[sym-aes]]
- 金鑰分配問題促成了公開金鑰密碼學：[[asym-public-key]]、[[asym-key-exchange]]

## 來源引文

- [S02 p.16 §1.5.1 Def.1.24] "The encryption scheme is said to be symmetric-key if for each associated encryption/decryption key pair (e, d), it is computationally 'easy' to determine d knowing only e, and to determine e from d."
- [S02 p.16 §1.5.1] "Since e = d in most practical symmetric-key encryption schemes, the term symmetric-key becomes appropriate."
- [S02 p.17 §1.5.1] "One of the major issues with symmetric-key systems is to find an efficient method to agree upon and exchange keys securely. This problem is referred to as the key distribution problem"
- [S02 p.17 §1.5.1] "However, in symmetric-key encryption, this means that the key e must also be kept secret, as d can be deduced from e."
- [S02 p.17 §1.5.1] "There are two classes of symmetric-key encryption schemes which are commonly distinguished: block ciphers and stream ciphers."
- [S02 p.16 §1.5.1] "Example 1.25 illustrates the idea of symmetric-key encryption."
- [S02 p.19 §1.5.2] "Another class of symmetric-key ciphers is the simple transposition cipher"
- [S06 p.30 §3.2] "Symmetric-key algorithms (sometimes called secret-key algorithms) use a single key to both apply cryptographic protection and to remove or check the protection"
- [S06 p.31 §3.2] "encrypt data (i.e., apply protection) is also used to decrypt the encrypted data (i.e., remove the protection)."
- [S06 p.31 §3.2] "The key must be kept secret if the data is to remain protected."
- [S06 p.31 §3.2] "Encryption to provide data confidentiality (see Section 4.1)"
- [S06 p.31 §3.2] "If, instead, there are 1,000 entities that wish to communicate with each other, there are 499,500 possible pair-wise relationships"
- [S06 p.31 §3.2] "There are six possible pair-wise relationships (A-B, A-C, A-D, B-C, B-D, and C-D), so at least six keys are required."
- [S06 p.18 §2.1] "A single cryptographic key that is used with a symmetric (secret key) algorithm"
