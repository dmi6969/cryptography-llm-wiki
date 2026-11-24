---
id: app-hybrid-tls
title: 密碼學在現代網路的應用：混合加密與 HTTPS／TLS 1.3
topic: T5
aliases: [TLS 1.3, TLS, HTTPS, hybrid encryption, 混合加密, handshake, record protocol, forward secrecy, 前向保密, certificate, 憑證]
sources: [S06, S10]
prerequisites: [sym-aes, mode-gcm-aead, asym-key-exchange, asym-signature]
relations:
  - {type: builds-on, target: asym-key-exchange}
  - {type: builds-on, target: asym-signature}
  - {type: builds-on, target: mode-gcm-aead}
  - {type: related, target: intro-what-is-crypto}
facts:
  tls13.static_rsa_removed: true
  tls13.mandatory_suite: TLS_AES_128_GCM_SHA256
---

# 密碼學在現代網路的應用：混合加密與 TLS 1.3

## 定義

**TLS** 的主要目標是在兩個通訊端點之間提供一條**安全通道** [S10 p.6]，具備三種性質 [S10 p.6]：
- **鑑別（authentication）**：伺服器端一定會被鑑別，可使用 RSA、ECDSA 等非對稱密碼學或預先共享金鑰；
- **機密性（confidentiality）**：建立連線後的資料只有兩端看得到；
- **完整性（integrity）**：資料被攻擊者修改一定會被偵測出來。

我們瀏覽 HTTPS 網站時，背後就是 TLS 在保護資料（HTTPS 與 TLS 的關係為本 Wiki 的教學補充）。

## 重點

- **混合加密（hybrid）**：非對稱演算法太慢、不適合處理大量資料；NIST 指出可以**結合對稱與非對稱演算法**，兼顧效率並減少所需金鑰數量 [S06 p.34–35]。
- TLS 由兩部分組成 [S10 p.6]：
  1. **Handshake（交握）協定**：鑑別雙方、協商演算法，並**建立共享金鑰** → 用到 **(EC)DHE 金鑰交換**（[[asym-key-exchange]]）與**憑證簽章**（[[asym-signature]]）；
  2. **Record（記錄）協定**：用交握得到的金鑰保護之後的所有流量 → 用到**對稱式 AEAD 加密**（如 AES-GCM，[[mode-gcm-aead]]）。
- **TLS 1.3 的重要改變** [S10 p.8]：
  - **移除了靜態 RSA 與靜態 Diffie–Hellman 的金鑰交換**，所有公鑰式金鑰交換都提供**前向保密（forward secrecy）**；
  - 對稱式演算法只保留 **AEAD**。
- **前向保密**：即使長期金鑰（例如憑證的簽章私鑰）在交握完成後外洩，也不會危及這次連線的 session key [S10 p.143]。
- 每個 TLS 1.3 實作都必須支援 **TLS_AES_128_GCM_SHA256** [S10 p.102]——也就是 AES-128 + GCM。
- RSA 在 TLS 1.3 的角色是**簽章**（且必須用 RSASSA-PSS）[S10 p.70]，不是用來「加密並傳送 session key」。

## 範例

```
瀏覽器（Client）                                  網站（Server）
   │  ① ClientHello + (EC)DHE 公開值  ────────────▶ │
   │  ◀──────────── ② ServerHello + (EC)DHE 公開值   │   → 雙方各自算出相同的共享金鑰
   │  ◀──────────── ③ 憑證 + 簽章（RSA-PSS／ECDSA）  │   → 確認「真的是這個網站」
   │  ④ 之後的網頁資料：AES-GCM 加密 + 認證  ◀══════▶ │   → 機密性 + 完整性
```
（依 RFC 8446 §1、§2 的描述簡化繪製 [S10 p.6][S10 p.10]）

## 常見誤解

- 「HTTPS 是用 RSA 加密 session key 再傳給伺服器」——這是舊版 TLS 的靜態 RSA 金鑰傳輸；**TLS 1.3 已移除** [S10 p.8]，改用 (EC)DHE 金鑰交換，RSA 只用於簽章 [S10 p.70]。

## 關聯

- 組成元件：[[asym-key-exchange]]、[[asym-signature]]、[[mode-gcm-aead]]、[[sym-aes]]
- 對應四大目標：[[intro-what-is-crypto]]

## 來源引文

- [S10 p.6 §1] "The primary goal of TLS is to provide a secure channel between two communicating peers"
- [S10 p.6 §1] "Authentication: The server side of the channel is always authenticated; the client side is optionally authenticated."
- [S10 p.6 §1] "Authentication can happen via asymmetric cryptography (e.g., RSA [RSA], the Elliptic Curve Digital Signature Algorithm (ECDSA) [ECDSA], or the Edwards-Curve Digital Signature Algorithm (EdDSA) [RFC8032]) or a symmetric pre-shared key (PSK)."
- [S10 p.6 §1] "Confidentiality: Data sent over the channel after establishment is only visible to the endpoints."
- [S10 p.6 §1] "Integrity: Data sent over the channel after establishment cannot be modified by attackers without detection."
- [S10 p.6 §1] "A handshake protocol (Section 4) that authenticates the communicating parties, negotiates cryptographic modes and parameters, and establishes shared keying material."
- [S10 p.6 §1] "A record protocol (Section 5) that uses the parameters established by the handshake protocol to protect traffic between the communicating peers."
- [S10 p.8 §1.2] "Static RSA and Diffie-Hellman cipher suites have been removed; all public-key based key exchange mechanisms now provide forward secrecy."
- [S10 p.8 §1.2] "Those that remain are all Authenticated Encryption with Associated Data (AEAD) algorithms."
- [S10 p.10 §2] "(EC)DHE (Diffie-Hellman over either finite fields or elliptic curves)"
- [S10 p.143 App.E.1] "If the long-term keying material (in this case the signature keys in certificate-based authentication modes or the external/resumption PSK in PSK with (EC)DHE modes) is compromised after the handshake is complete, this does not compromise the security of the session key"
- [S10 p.102 §9.1] "A TLS-compliant application MUST implement the TLS_AES_128_GCM_SHA256 [GCM] cipher suite"
- [S10 p.70 §4.4.3] "RSA signatures MUST use an RSASSA-PSS algorithm"
- [S06 p.34 §3.3] "there are methods that combine the use of symmetric and asymmetric algorithms to"
- [S06 p.35 §3.3] "achieve better efficiency than is possible when using only asymmetric algorithms, while reducing the number of keys required when using only symmetric algorithms."
