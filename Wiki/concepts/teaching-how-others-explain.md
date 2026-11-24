---
id: teaching-how-others-explain
title: 別人怎麼介紹加密演算法？（教學設計參考）
topic: T6
aliases: [teaching approach, pedagogy, 教學設計, 教學順序, how others teach]
sources: [S13, S14, S15]
prerequisites: []
relations:
  - {type: related, target: intro-what-is-crypto}
  - {type: related, target: basics-bits-xor-mod}
facts: {}
---

# 別人怎麼介紹加密演算法？（教學設計參考）

## 定義

本頁比較三種不同對象的教材如何介紹加密：**大學教科書**（The Joy of Cryptography，Oregon State University）[S13 p.9]、**入門書**（Crypto 101）[S14 p.4]、**科技公司給大眾的說明**（Cloudflare Learning Center）[S15 p.1]，並歸納出本簡報採用的教學原則。

## 重點

- **大學教科書：先複習工具，再從最簡單的密碼開始。** 第 0 章先複習符號與模運算（mod）、字串與 XOR，第 1 章才是第一個密碼（one-time pad）與 Kerckhoffs 原則 [S13 p.9]；之後依序是區塊加密、操作模式、認證加密、RSA、Diffie–Hellman [S13 p.9]。
- **教科書會先交代每個符號**：例如「Alice 要傳的訊息叫 m，稱為明文」「轉換後的值叫 c，稱為密文」[S13 p.21]。
- **入門書：第一個「積木」就是 XOR**，然後才是區塊加密（其中介紹 AES）、串流加密、金鑰交換、公開金鑰加密 [S14 p.4]；連公式中的下標都會解釋（「i 只是編號」）[S14 p.18]。
- **給大眾的說明：定義 → 最簡單的例子 → 比喻 → 分類 → 為什麼重要 → 怎麼被攻擊 → 生活中的應用** [S15 p.1]：
  - 例子：Alice 把「Hello」每個字母換成字母表後面第 2 個字母 [S15 p.1]
  - 比喻：金鑰就像實體鑰匙，鎖上（加密）後只有對的鑰匙能打開（解密）[S15 p.1]
  - 分類：對稱式只有一把金鑰，雙方共用 [S15 p.1]
  - 攻擊：暴力破解＝猜幾百萬、幾十億次金鑰 [S15 p.1]
  - 應用：HTTPS 使用 TLS 加密 [S15 p.1]
- **本簡報採用的教學原則**（本 Wiki 歸納自以上三者）：
  1. 先介紹之後會用到的名詞與工具（位元、XOR、mod），再用到它們（[[basics-bits-xor-mod]]）。
  2. 每個主題依序講「基本原理 → 為什麼需要／好處與限制 → 現實中怎麼做」，一個主題分幾頁講完，不擠在一頁。
  3. 公式出現時，每個符號都說明代表什麼。
  4. 從最簡單的例子（位移密碼）開始，再進到現代演算法。
  5. 用生活比喻（鑰匙、信箱）幫助理解，再接回正式名詞。

## 範例

| 教材 | 對象 | 開場方式 | 主題順序 |
|---|---|---|---|
| The Joy of Cryptography | 大學生 | 複習 mod、XOR 等工具 | 工具 → 簡單密碼 → 區塊加密 → 模式 → 認證加密 → RSA → DH |
| Crypto 101 | 入門工程師 | XOR | XOR → 區塊加密（AES）→ 串流加密 → 金鑰交換 → 公開金鑰 |
| Cloudflare | 一般大眾 | 定義＋位移 2 的小例子 | 定義 → 例子 → 鑰匙比喻 → 對稱／非對稱 → 重要性 → 暴力破解 → HTTPS |

## 關聯

- 這些原則套用到：[[intro-what-is-crypto]]、[[basics-bits-xor-mod]]

## 來源引文

- [S13 p.9 Contents] "0 Review of Concepts & Notation 1 0.1 Logs & Exponents 1 0.2 Modular Arithmetic 1 0.3 Strings"
- [S13 p.21 §1] "Alice has a message m that she wants to send (privately) to Bob. We call m the plaintext."
- [S13 p.21 §1] "will somehow transform that plaintext into a value c (called the ciphertext)"
- [S14 p.4 Contents] "II Buildingblocks 16 5 Exclusiveor 17 5.1 Description"
- [S14 p.4 Contents] "6 Blockciphers 28 6.1 Description"
- [S14 p.18 §5.1] "On the left, we have the plaintext bit Pi. The i is just an index"
- [S15 p.1] "Encryption is a way of scrambling data so that only authorized parties can understand the information."
- [S15 p.1] "but she replaces each letter in her message with the letter that comes two places later in the alphabet."
- [S15 p.1] "Like a physical key, it locks (encrypts) data so that only someone with the right key can unlock (decrypt) it."
- [S15 p.1] "In symmetric encryption, there is only one key, and all communicating parties use the same (secret) key for both encryption and decryption."
- [S15 p.1] "is when an attacker who does not know the decryption key attempts to determine the key by making millions or billions of guesses."
- [S15 p.1] "HTTPS uses the encryption protocol called Transport Layer Security (TLS)."
