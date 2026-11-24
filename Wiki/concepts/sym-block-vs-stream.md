---
id: sym-block-vs-stream
title: 區塊加密（Block Cipher）與串流加密（Stream Cipher）
topic: T3
aliases: [block cipher, stream cipher, keystream, 區塊加密, 串流加密, 金鑰串流, product cipher]
sources: [S02, S06]
prerequisites: [sym-concept]
relations:
  - {type: related, target: sym-aes}
  - {type: related, target: mode-overview}
facts: {}
---

# 區塊加密與串流加密

## 定義

- **區塊加密（block cipher）**：把明文切成**固定長度的區塊**，一次加密一個區塊 [S02 p.17]。
- **串流加密（stream cipher）**：可以看成區塊長度為 1 的簡單區塊加密，但**每個符號的加密方式都可以不同**，由一串**金鑰串流（keystream）** 決定 [S02 p.21]。

## 重點

- 大多數知名的對稱式加密技術都是區塊加密 [S02 p.17]。替換密碼與換位密碼是區塊加密的兩個重要類別，**product cipher** 則把兩者組合起來 [S02 p.17]。
- 單獨使用替換或換位的安全性都不高 [S02 p.20]；現代區塊加密（例如 AES）就是反覆組合「替換」與「排列/混合」步驟（見 [[sym-aes]]）。
- 串流加密的優點：傳輸錯誤多時**不會擴散錯誤**；也適合一次只能處理一個符號的設備 [S02 p.21]。
- 金鑰串流可以隨機產生，或由一個小的種子（seed）經演算法產生（keystream generator）[S02 p.22]。
- NIST：區塊加密演算法要搭配**經核准的操作模式（mode of operation）** 使用 [S06 p.32]（見 [[mode-overview]]）。

## 範例

```
區塊加密： [HELLOWOR][LD______] → 每塊固定長度，各自送進加密函數
串流加密： H⊕k1  E⊕k2  L⊕k3  L⊕k4 …  → 每個符號配一個金鑰串流符號
```
（示意圖，⊕ 表示與金鑰串流組合；依 [S02 p.17][S02 p.21] 的定義繪製）

## 關聯

- 代表演算法：[[sym-aes]]（區塊加密）
- 區塊加密需要操作模式：[[mode-overview]]；CTR 模式能把區塊加密當成串流加密使用：[[mode-ctr]]

## 來源引文

- [S02 p.17 §1.5.1 Def.1.26] "A block cipher is an encryption scheme which breaks up the plaintext messages to be transmitted into strings (called blocks) of a fixed length t over an alphabet A, and encrypts one block at a time."
- [S02 p.17 §1.5.1] "Most well-known symmetric-key encryption techniques are block ciphers."
- [S02 p.17 §1.5.1] "Two important classes of block ciphers are substitution ciphers and transposition ciphers"
- [S02 p.20 §1.5.3] "Simple substitution and transposition ciphers individually do not provide a very high level"
- [S02 p.21 §1.5.4] "Stream ciphers form an important class of symmetric-key encryption schemes. They are, in one sense, very simple block ciphers having block length equal to one."
- [S02 p.21 §1.5.4] "What makes them useful is the fact that the encryption transformation can change for each symbol of plaintext being encrypted."
- [S02 p.21 §1.5.4] "In situations where transmission errors are highly probable, stream ciphers are advantageous because they have no error propagation."
- [S02 p.22 §1.5.4] "The keystream could be generated at random, or by an algorithm which generates the keystream from an initial small keystream (called a seed)"
- [S06 p.32 §3.2.1] "A block cipher algorithm is used with a single key in an approved mode of operation to both apply cryptographic protection (e.g., encrypt) and to subsequently process the protected information (e.g., decrypt)."
