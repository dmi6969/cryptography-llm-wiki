---
id: intro-terminology
title: 基本術語：明文、密文、金鑰、加密與解密
topic: T1
aliases: [plaintext, ciphertext, key, encryption, decryption, cipher, 明文, 密文, 金鑰, 加密, 解密]
sources: [S01, S02]
prerequisites: [intro-what-is-crypto]
relations:
  - {type: related, target: intro-kerckhoffs}
  - {type: related, target: sym-concept}
  - {type: related, target: asym-public-key}
facts: {}
---

# 基本術語：明文、密文、金鑰、加密與解密

## 定義

| 術語 | 意思 | 來源 |
|---|---|---|
| **明文（plaintext）** | 要被加密的原始資料 | [S01 p.225][S02 p.12] |
| **密文（ciphertext）** | 加密後、意義已無法直接理解的資料 | [S01 p.62][S02 p.12] |
| **加密（encryption）** | 把明文轉換成密文，藏住原本的意義 | [S01 p.119] |
| **解密（decryption）** | 加密的反向過程，把密文還原成明文 | [S01 p.119][S02 p.12] |
| **金鑰（key）** | 控制加密演算法「怎麼轉換」的輸入參數 | [S01 p.171][S02 p.12] |
| **金鑰空間（key space）** | 所有可能金鑰的集合（範圍） | [S01 p.177][S02 p.12] |
| **密碼／加密法（cipher）** | 用來加密與解密的演算法；HAC 稱「加密方案」 | [S01 p.61][S02 p.13] |

## 重點

- **兩方通訊模型**：Alice（傳送者）加密後透過**不安全的通道**送給 Bob（接收者），中間的**攻擊者（adversary）**想破壞這個安全服務 [S02 p.14]。
- 不安全的通道上，旁人可以**讀取、插入、刪除、重排**訊息 [S02 p.14]。
- 加密要能還原：每一把加密金鑰都必須對應到一把解密金鑰，使解密後得到原本的明文 [S02 p.13]。
- HAC 把加密金鑰 e 和解密金鑰 d 合稱「key pair」，並註明 **e 和 d 可以相同** [S02 p.13]——相同時就是**對稱式加密**（[[sym-concept]]）；「公鑰／私鑰對」是另一回事，屬於非對稱式加密（[[asym-public-key]]）。
- **密碼分析（cryptanalysis）**：研究如何破解密碼技術；**cryptology** 是密碼學與密碼分析的合稱 [S02 p.16]。
- 密碼技術一般分成兩大類：**對稱式金鑰（symmetric-key）** 與 **公開金鑰（public-key）** [S02 p.16]。

## 範例

```
明文  HELLO  ──加密(金鑰 k)──▶  密文  KHOOR  ──解密(金鑰 k)──▶  HELLO
```
（以位移 3 的 Caesar 密碼示意，詳見 [[classical-caesar]]。）

## 關聯

- 為什麼「只有金鑰需要保密」：[[intro-kerckhoffs]]
- e = d 的情況：[[sym-concept]]；公鑰與私鑰：[[asym-public-key]]

## 來源引文

- [S02 p.12 §1.4] "An element of M is called a plaintext message or simply a plaintext."
- [S02 p.12 §1.4] "alphabet of definition for M. An element of C is called a ciphertext."
- [S02 p.12 §1.4] "denotes a set called the key space. An element of K is called a key."
- [S02 p.12 §1.4] "The process of applying the transformation Dd to a ciphertext c is usually referred to as decrypting c or the decryption of c."
- [S02 p.13 §1.4] "An encryption scheme is sometimes referred to as a cipher."
- [S02 p.13 §1.4] "Note that e and d could be the same."
- [S02 p.14 §1.4] "An adversary is an entity in a two-party communication which is neither the sender nor receiver, and which tries to defeat the information security service being provided between the sender and receiver."
- [S02 p.14 §1.4] "An unsecured channel is one from which parties other than those for which the information is intended can reorder, delete, insert, or read."
- [S02 p.16 §1.4] "Cryptanalysis is the study of mathematical techniques for attempting to defeat cryptographic techniques"
- [S02 p.16 §1.4] "Cryptology is the study of cryptography (Definition 1.1) and cryptanalysis."
- [S02 p.16 §1.4] "Cryptographic techniques are typically divided into two generic types: symmetric-key and public-key."
- [S01 p.225 plain text] "Data that is input to an encryption process."
- [S01 p.62 cipher text] "Data that has been transformed by encryption so that its semantic information content (i.e., its meaning) is no longer intelligible or directly available."
- [S01 p.119 encryption] "Cryptographic transformation of data (called 'plain text') into a different form (called 'cipher text') that conceals the data's original meaning and prevents the original form from being used."
- [S01 p.119 encryption] "The corresponding reverse process is 'decryption', a transformation that restores encrypted data to its original form."
- [S01 p.171 key] "An input parameter used to vary a transformation function performed by a cryptographic algorithm."
- [S01 p.177 key space] "The range of possible values of a cryptographic key; or the number of distinct transformations supported by a particular cryptographic algorithm."
- [S01 p.61 cipher] "A cryptographic algorithm for encryption and decryption."
