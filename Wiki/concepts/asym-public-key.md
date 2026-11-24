---
id: asym-public-key
title: 公開金鑰密碼學（Asymmetric / Public-Key Cryptography）
topic: T5
aliases: [asymmetric cryptography, public-key cryptography, public key, private key, key pair, 非對稱式加密, 公開金鑰, 公鑰, 私鑰, 金鑰對]
sources: [S02, S06, S07]
prerequisites: [sym-concept]
relations:
  - {type: contrasts-with, target: sym-concept}
  - {type: related, target: asym-key-exchange}
  - {type: related, target: asym-rsa}
  - {type: related, target: asym-signature}
facts: {}
---

# 公開金鑰密碼學（非對稱式加密）

## 定義

**非對稱式（公開金鑰）演算法**使用**一對金鑰**：**公鑰（public key）** 與 **私鑰（private key）**，兩者在數學上相關 [S06 p.34]。
- 公鑰可以公開，不會降低安全性；私鑰必須保密 [S06 p.34]。
- 雖然兩把金鑰相關，但**無法從公鑰有效率地推出私鑰** [S06 p.34]。

## 重點

- **起源**：1976 年 Diffie 與 Hellman 發表《New Directions in Cryptography》，提出公開金鑰密碼學的革命性概念 [S02 p.2]。
- 他們的想法：加密金鑰 E 與解密金鑰 D 不同，而且**從 E 算出 D 在計算上不可行**，所以 E 可以公開 [S07 p.1]。
- 每個人把自己的公開加密金鑰放進「公開目錄」，任何人都能用它加密訊息，**只有持有對應私鑰的接收者能解密** [S07 p.1]——就算兩人從沒見過面，也能祕密通訊 [S07 p.1]。
- **為什麼需要**：對稱式加密必須先透過安全通道分配金鑰；Diffie–Hellman 指出，這個**金鑰分配問題**的成本與延遲，是商業通訊走向大型網路的主要障礙 [S07 p.1]（見 [[sym-concept]]）。
- **加密 vs. 簽章**的金鑰用法 [S06 p.34]：
  - 加密：**用公鑰加密、用私鑰解密**；
  - 數位簽章：**用私鑰簽章、用公鑰驗證**（見 [[asym-signature]]）。
- **缺點：慢**。非對稱演算法比對稱式慢很多，所以不拿來處理大量資料 [S06 p.34]——實務上兩者混合使用（見 [[app-hybrid-tls]]）。

## 範例

**信箱比喻**（本 Wiki 的教學比喻）：公鑰像是**投信口**，任何人都能把信投進去；私鑰像是**信箱鑰匙**，只有主人能打開取信。對應「公鑰加密、私鑰解密」[S06 p.34]。

```
Bob 的公鑰（公開）  ──▶  Alice 用它加密  ──▶  密文  ──▶  只有 Bob 的私鑰能解開
```

## 關聯

- 對比：[[sym-concept]]（同一把金鑰）
- 金鑰交換：[[asym-key-exchange]]；代表演算法：[[asym-rsa]]；簽章：[[asym-signature]]

## 來源引文

- [S06 p.34 §3.3] "Asymmetric-key algorithms (often called public-key algorithms) use a pair of keys (i.e., a key pair): a public key and a private key that are mathematically related to each other."
- [S06 p.34 §3.3] "The public key may be made public without reducing the security of the process, but the private key must remain secret if the cryptographic protection is to remain effective."
- [S06 p.34 §3.3] "the private key cannot efficiently be determined based on knowledge of the public key."
- [S06 p.34 §3.3] "a digital signature is computed using a private key, and the signature is verified using the public key"
- [S06 p.34 §3.3] "the encryption is performed using the public key, and the decryption is performed using the private key"
- [S06 p.34 §3.3] "These algorithms tend to be much slower than symmetric-key algorithms so are not used to process large amounts of data."
- [S02 p.2 §1.1] "The most striking development in the history of cryptography came in 1976 when Diffie and Hellman published New Directions in Cryptography. This paper introduced the revolutionary concept of public-key cryptography"
- [S07 p.1 §I] "In a public key cryptosystem enciphering and deciphering are governed by distinct keys, E and D, such that computing D from E is computationally infeasible"
- [S07 p.1 §I] "The enciphering key E can thus be publicly disclosed without compromising the deciphering key D."
- [S07 p.1 §I] "Each user of the network can, therefore, place his enciphering key in a public directory."
- [S07 p.1 §I] "A private conversation can therefore be held between any two individuals regardless of whether they have ever communicated before."
- [S07 p.1 §I] "The cost and delay imposed by this key distribution problem is a major barrier to the transfer of business communications to large teleprocessing networks."
