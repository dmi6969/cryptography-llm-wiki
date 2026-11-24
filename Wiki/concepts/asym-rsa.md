---
id: asym-rsa
title: RSA：基本運作原理
topic: T5
aliases: [RSA, Rivest-Shamir-Adleman, RSA modulus, public exponent, private exponent, OAEP, RSAES-OAEP, 模數, 質數分解]
sources: [S02, S08, S09, S12]
prerequisites: [asym-public-key, basics-bits-xor-mod]
relations:
  - {type: instance-of, target: asym-public-key}
  - {type: used-by, target: asym-signature}
  - {type: used-by, target: app-hybrid-tls}
facts:
  rsa.example: {p: 47, q: 59, n: 2773, phi: 2668, d: 157, e: 17, m: 920, c: 948}
  rsa.paper_recommended_digits: 200
  rsa.k_for_112bit: 2048
  rsa.k_for_128bit: 3072
---

# RSA：基本運作原理

## 定義

**RSA**（Rivest、Shamir、Adleman，1978）是第一個實用的公開金鑰加密與簽章方案 [S02 p.3]。
它的特性是：**公開加密金鑰，並不會因此洩漏對應的解密金鑰** [S08 p.1]。

## 重點

- **金鑰產生** [S08 p.6–7]：
  1. 選兩個**很大的隨機質數** p、q，計算 **n = p·q**；
  2. 選一個與 (p−1)(q−1) 互質的 d；
  3. 算出 e，使 e·d ≡ 1 (mod (p−1)(q−1))。
  - **公鑰** = (e, n)，**私鑰** = (d, n)；每個人公開加密金鑰、保留解密金鑰 [S08 p.6]。RFC 8017 也定義 RSA 公鑰由 **模數 n（modulus）** 與 **公開指數 e** 組成 [S09 p.8]。
- **加密／解密** [S08 p.6]：
  - 加密：C = M^e mod n
  - 解密：M = C^d mod n
- **安全性**：n 公開，但 p、q 因為**大數分解非常困難**而保持隱藏，d 也因此無法從 e 推出 [S08 p.6][S08 p.1]。
- **金鑰長度要跟上時代**：1978 年論文建議 n 約 200 位十進位數字 [S08 p.9]；NIST 現行對照表：RSA 模數 k = **2048** 位元約等於 112 位元安全強度、**3072** 位元約等於 128 位元（相當 AES-128）[S12 p.67][S12 p.68]。
- **實務上不直接用 M^e mod n**：RFC 8017 規定新應用必須支援 **RSAES-OAEP**（把訊息先經 OAEP 編碼再做 RSA 運算），舊的 PKCS1-v1_5 只為相容而保留 [S09 p.18][S09 p.19]。
- 量子電腦實用化後，RSA 等演算法的強度估計會大幅改變 [S12 p.68]。

## 範例

RSA 原始論文的小例子 [S08 p.10]（簡報驗證節點會用程式重算）：

```
p = 47，q = 59 → n = 47 × 59 = 2773
(p−1)(q−1) = 46 × 58 = 2668
私鑰 d = 157 → 公鑰 e = 17（17 × 157 = 2669 ≡ 1 mod 2668）
加密 M = 920： C = 920^17 mod 2773 = 948
解密：         M = 948^157 mod 2773 = 920
```

## 常見誤解

- 「RSA 就是直接算 C = M^e mod n 就好」——教科書公式只說明原理；RFC 8017 要求新應用使用 RSAES-OAEP 編碼 [S09 p.18]。
- 「200 位數的 n 就夠安全」——那是 1978 年的建議 [S08 p.9]；現行建議至少 2048 位元 [S12 p.67]。

## 關聯

- 屬於：[[asym-public-key]]
- 也能做數位簽章：[[asym-signature]]
- 在 TLS 1.3 中用於憑證簽章，而非金鑰傳輸：[[app-hybrid-tls]]

## 來源引文

- [S02 p.3 §1.1] "In 1978 Rivest, Shamir, and Adleman discovered the first practical public-key encryption and signature scheme, now referred to as RSA."
- [S08 p.1 Abstract] "An encryption method is presented with the novel property that publicly revealing an encryption key does not thereby reveal the corresponding decryption key."
- [S08 p.1 Abstract] "A message is encrypted by representing it as a number M, raising M to a publicly specified power e, and then taking the remainder when the result is divided by the publicly specified product, n, of two large secret prime numbers p and q."
- [S08 p.1 Abstract] "The security of the system rests in part on the difficulty of factoring the published divisor, n."
- [S08 p.6 §V] "The encryption key is thus the pair of positive integers (e,n). Similarly, the decryption key is the pair of positive integers (d,n). Each user makes his encryption key public, and keeps the corresponding decryption key private."
- [S08 p.6 §V] "These primes are very large, 'random' primes."
- [S08 p.6 §V] "the factors p and q will be effectively hidden from everyone else due to the enormous difficulty of factoring n."
- [S08 p.6 §V] "You then pick the integer d to be a large, random integer which is relatively prime to (p− 1) · (q− 1)."
- [S08 p.7 §V] "The integer e is finally computed from p,q, and d to be the 'multiplicative inverse' of d, modulo (p− 1) · (q− 1)."
- [S08 p.9 §VII] "We recommend using 100-digit (decimal) prime numbers p and q, so that n has 200 digits."
- [S08 p.10 §VIII] "Consider the case p = 47,q = 59,n = p·q = 47 · 59 = 2773, and d = 157."
- [S08 p.10 §VIII] "Therefore e = 17, the multiplicative inverse (mod 2668) of d = 157."
- [S08 p.10 §VIII] "the first block (M = 920) is enciphered"
- [S08 p.10 §VIII] "M 17 = (((((1)2 ·M)2)2)2)2 ·M = 948 (mod 2773)"
- [S09 p.8 §3.1] "an RSA public key consists of two components: n the RSA modulus, a positive integer e the RSA public exponent, a positive integer"
- [S09 p.18 §7] "RSAES-OAEP is REQUIRED to be supported for new applications; RSAES-PKCS1-v1_5 is included only for compatibility with existing applications."
- [S09 p.19 §7.1] "RSAES-OAEP combines the RSAEP and RSADP primitives (Sections 5.1.1 and 5.1.2) with the EME-OAEP encoding method"
- [S12 p.67 §5.6.1.1 Table 2] "112 3TDEA68 L = 2048 N = 224 k = 2048"
- [S12 p.67 §5.6.1.1] "The predominant algorithm of this type is the RSA algorithm."
- [S12 p.68 §5.6.1.1 Table 2] "128 AES-128 L = 3072 N = 256 k = 3072"
- [S12 p.68 §5.6.1.1] "The security-strength estimates will be significantly affected when quantum computing becomes a practical consideration."
