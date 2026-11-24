---
id: asym-signature
title: 數位簽章（Digital Signature）
topic: T5
aliases: [digital signature, signature, RSASSA-PSS, PSS, 數位簽章, 簽章驗證]
sources: [S02, S06, S08, S09, S10]
prerequisites: [asym-public-key]
relations:
  - {type: part-of, target: asym-public-key}
  - {type: used-by, target: app-hybrid-tls}
  - {type: related, target: intro-what-is-crypto}
facts: {}
---

# 數位簽章（Digital Signature）

## 定義

**數位簽章**：用**私鑰**對訊息產生簽章，任何人都能用對應的**公鑰**驗證 [S06 p.34][S08 p.1]。
RSA 論文指出：簽章**無法偽造**，簽署者事後也**不能否認**簽過 [S08 p.1]。

## 重點

- 數位簽章是公開金鑰密碼學最重要的貢獻之一 [S02 p.3]。
- 金鑰方向與加密**相反**：加密是「公鑰加密、私鑰解密」；簽章是「**私鑰簽、公鑰驗**」[S06 p.34]。
- 提供的服務：**身分、完整性、來源鑑別** [S06 p.34]，以及**不可否認性**（簽署者無法否認）[S08 p.1]——呼應密碼學四大目標（[[intro-what-is-crypto]]）。
- 電子簽章必須**同時依賴訊息與簽署者**，否則接收者可以改訊息、或把簽章貼到別的訊息上 [S08 p.4]。
- 現行標準：RFC 8017 規定新應用必須使用 **RSASSA-PSS** [S09 p.31]；TLS 1.3 的 RSA 簽章也必須使用 RSASSA-PSS [S10 p.70]。

## 範例

```
Bob：  訊息 M ──[Bob 的私鑰 簽章]──▶ (M, 簽章 S)
Alice：(M, S) ──[Bob 的公鑰 驗證]──▶ ✔ 確實是 Bob 簽的，而且 M 沒被改過
```
（依 [S06 p.34] 的金鑰用法與 [S08 p.1] 的說明繪製）

## 關聯

- 屬於：[[asym-public-key]]
- 在 TLS 1.3 中用於伺服器憑證／身分鑑別：[[app-hybrid-tls]]

## 來源引文

- [S08 p.1 Abstract] "A message can be 'signed' using a privately held decryption key. Anyone can verify this signature using the corresponding publicly revealed encryption key. Signatures cannot be forged, and a signer cannot later deny the validity of his signature."
- [S08 p.4 §IV] "An electronic signature must be message-dependent, as well as signer-dependent."
- [S06 p.34 §3.3] "a digital signature is computed using a private key, and the signature is verified using the public key"
- [S06 p.34 §3.3] "To provide identity, integrity, and source authentication services in the form of digital signatures"
- [S02 p.3 §1.1] "One of the most significant contributions provided by public-key cryptography is the digital signature."
- [S09 p.31 §8] "RSASSA-PSS is REQUIRED in new applications."
- [S10 p.70 §4.4.3] "RSA signatures MUST use an RSASSA-PSS algorithm"
