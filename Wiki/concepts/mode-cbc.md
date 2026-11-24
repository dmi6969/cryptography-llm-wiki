---
id: mode-cbc
title: CBC（Cipher Block Chaining）模式
topic: T4
aliases: [CBC, Cipher Block Chaining, 密文區塊鏈結]
sources: [S01, S03, S05]
prerequisites: [mode-overview, mode-ecb, basics-bits-xor-mod]
relations:
  - {type: part-of, target: mode-overview}
  - {type: contrasts-with, target: mode-ecb}
  - {type: contrasts-with, target: mode-ctr}
facts: {}
---

# CBC（Cipher Block Chaining）模式

## 定義

**CBC**：每個明文區塊在加密前，先和**前一個密文區塊**做 XOR（⊕），把區塊「鏈結」起來；第一個區塊則和 **IV** 做 XOR [S05 p.17]。

- C₁ = E_K(P₁ ⊕ IV)
- Cⱼ = E_K(Pⱼ ⊕ Cⱼ₋₁)，j = 2…n  [S05 p.17]

**解密**反過來：先用區塊加密的**反函數**解開密文區塊，再和前一個密文區塊（第一塊用 IV）做 XOR [S05 p.18]。

- P₁ = D_K(C₁) ⊕ IV
- Pⱼ = D_K(Cⱼ) ⊕ Cⱼ₋₁，j = 2…n  [S05 p.18]

RFC 4949 也說 CBC 是「以鏈結密文區塊來改進 ECB」的模式 [S01 p.61]。

## 重點

- **打破重複**：因為鏈結，每個密文區塊都和它之前的所有明文區塊有關 [S03 p.9]；只要改變 IV，同樣的明文就會產生不同的密文 [S03 p.9]。
- **IV 不需要保密，但必須無法預測**，而且 IV 的完整性應受到保護 [S05 p.17]。
- **加密無法平行**：每個區塊的輸入要等前一個區塊的加密結果 [S05 p.18]；**解密可以平行**，因為所有密文區塊都已經拿到了 [S05 p.18]。
- 需要填充，讓明文成為完整區塊 [S05 p.24]。
- 錯誤傳播：密文區塊 cⱼ 有一個位元出錯，會影響 cⱼ 與 cⱼ₊₁ 兩個區塊的解密 [S03 p.9]。

## 範例

```
         IV        C1         C2
          │         │          │
 P1 ──▶ (⊕) ──▶ E_K ─┤  P2 ──▶ (⊕) ──▶ E_K ─┤  P3 ──▶ (⊕) ──▶ E_K ──▶ C3
                    C1                    C2
```
（依 SP 800-38A §6.2 公式繪製 [S05 p.17]）

## 關聯

- 改進自：[[mode-ecb]]；另一種做法：[[mode-ctr]]

## 來源引文

- [S05 p.17 §6.2] "The Cipher Block Chaining (CBC) mode is a confidentiality mode whose encryption process features the combining ('chaining') of the plaintext blocks with the previous ciphertext blocks."
- [S05 p.17 §6.2] "The CBC mode requires an IV to combine with the first plaintext block. The IV need not be secret, but it must be unpredictable"
- [S05 p.17 §6.2] "Also, the integrity of the IV should be protected"
- [S05 p.17 §6.2] "In CBC encryption, the first input block is formed by exclusive-ORing the first block of the plaintext with the IV."
- [S05 p.18 §6.2] "In CBC decryption, the inverse cipher function is applied to the first ciphertext block, and the resulting output block is exclusive-ORed with the initialization vector to recover the first plaintext block."
- [S05 p.18 §6.2] "The inverse cipher function is also applied to the second ciphertext block, and the resulting output block is exclusive-ORed with the first ciphertext block to recover the second plaintext block."
- [S05 p.18 §6.2] "In CBC encryption, the input block to each forward cipher operation (except the first) depends on the result of the previous forward cipher operation, so the forward cipher operations cannot be performed in parallel."
- [S05 p.18 §6.2] "In CBC decryption, however, the input blocks for the inverse cipher function, i.e., the ciphertext blocks, are immediately available, so that multiple inverse cipher operations can be performed in parallel."
- [S05 p.24 App.A] "For the ECB, CBC, and CFB modes, the plaintext must be a sequence of one or more complete data blocks"
- [S03 p.9 §7.2.2] "Changing the IV, key, or first plaintext block (e.g., using a counter or random field) results in different ciphertext."
- [S03 p.9 §7.2.2] "the chaining mechanism causes ciphertext cj to depend on xj and all preceding plaintext blocks"
- [S03 p.9 §7.2.2] "a single bit error in ciphertext block cj affects decipherment of blocks cj and cj+1"
- [S01 p.61 cipher block chaining] "A block cipher mode that enhances ECB mode by chaining together blocks of cipher text it produces."
