---
id: sym-aes
title: AES（Advanced Encryption Standard）
topic: T3
aliases: [AES, Advanced Encryption Standard, Rijndael, AES-128, AES-192, AES-256, 進階加密標準]
sources: [S01, S04, S06, S12]
prerequisites: [sym-concept, sym-block-vs-stream, basics-bits-xor-mod]
relations:
  - {type: instance-of, target: sym-block-vs-stream}
  - {type: used-by, target: mode-overview}
  - {type: used-by, target: app-hybrid-tls}
facts:
  aes.block_bits: 128
  aes.key_bits: [128, 192, 256]
  aes.rounds: {AES-128: 10, AES-192: 12, AES-256: 14}
  aes.selected_year: 2000
  des.withdrawn_year: 2005
  aes.example_input: 3243f6a8885a308d313198a2e0370734
  aes.example_key: 2b7e151628aed2a6abf7158809cf4f3c
---

# AES（Advanced Encryption Standard）

## 定義

**AES** 是 NIST 標準化的**對稱式區塊加密演算法**，可以加密與解密數位資料 [S04 p.4]。
它使用 **128、192 或 256 位元**的金鑰，對 **128 位元**的資料區塊做加解密 [S04 p.4]。

## 重點

- **怎麼來的**：NIST 在 1997 年公開徵求候選演算法，2000 年宣布選出 **Rijndael** 作為 AES [S04 p.9]——正是 Kerckhoffs 原則「演算法公開、經過公開審查」的實踐 [S01 p.268]（見 [[intro-kerckhoffs]]）。
- **三個版本**：AES-128、AES-192、AES-256，數字代表**金鑰長度**；**區塊大小一律 128 位元** [S04 p.9]。（Rijndael 本身支援其他區塊大小，但沒有納入標準 [S04 p.9]。）
- **輪數（rounds）**：AES-128 做 10 輪、AES-192 做 12 輪、AES-256 做 14 輪 [S04 p.19]。
- **每一輪的四個步驟**（作用在 4×4 位元組的 state 上）[S04 p.20]：
  1. **SubBytes**：用替換表（S-box）替換每個位元組——非線性的「替換」[S04 p.21]
  2. **ShiftRows**：把 state 的後三列循環位移——「換位」[S04 p.22]
  3. **MixColumns**：把每一欄的資料混合在一起 [S04 p.20]
  4. **AddRoundKey**：用 XOR 把該輪的 round key 加進 state [S04 p.24]
  其中有一輪會省略一個步驟 [S04 p.10]。
- **解密（InvCipher）**：把加密的步驟換成各自的反運算（InvSubBytes、InvShiftRows、InvMixColumns 與 AddRoundKey），並**依相反順序**執行 [S04 p.26]。
- FIPS 197 附錄 B 提供 AES-128 一步一步的完整實例，下方「實例」整理了第 1 輪 [S04 p.9][S04 p.42]。
- **取代 DES**：AES 是為了取代 DES 與 TDEA 而開發，是新產品**首選**的區塊加密演算法 [S06 p.33]；DES 因電腦運算力進步、強度不足，已在 **2005 年**被撤銷核准 [S06 p.32]。
- **安全強度**：AES-128／192／256 分別提供 128／192／256 位元的安全強度；低於 112 位元的組合已不再核准用於加密 [S12 p.68]。

## 範例

```
明文區塊（128 bits）
   │  AddRoundKey（初始）
   ▼
┌─ 第 1 ～ Nr 輪 ───────────────────┐
│ SubBytes → ShiftRows → MixColumns → AddRoundKey │ ×Nr（最後一輪省略一個步驟）
└──────────────────────────────────┘
   ▼
密文區塊（128 bits）       Nr = 10 / 12 / 14
```
（依 FIPS 197 §5.1 的步驟順序與 Table 3 的輪數繪製 [S04 p.19][S04 p.20]）

### 實例：FIPS 197 附錄 B，AES-128 第 1 輪 [S04 p.42]

- 輸入：`32 43 f6 a8 88 5a 30 8d 31 31 98 a2 e0 37 07 34`；金鑰：`2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c` [S04 p.42]
- 16 個位元組**依「欄」**填入 4×4 的 state：前 4 個位元組（32 43 f6 a8）成為第 1 欄。

| 步驟 | state（逐列，由上到下） | 看哪一格 |
|---|---|---|
| 初始 AddRoundKey（輸入 ⊕ 金鑰） | `19 a0 9a e9 / 3d f4 c6 f8 / e3 e2 8d 48 / be 2b 2a 08` | 32 ⊕ 2b = 19 |
| ① SubBytes | `d4 e0 b8 1e / 27 bf b4 41 / 11 98 5d 52 / ae f1 e5 30` | 19 查 S-box：列看前半 1、欄看後半 9 → d4（查表規則見 [S04 p.22]） |
| ② ShiftRows | `d4 e0 b8 1e / bf b4 41 27 / 5d 52 11 98 / 30 ae f1 e5` | 第 r 列往左循環移 r 格：`27 bf b4 41` → `bf b4 41 27` |
| ③ MixColumns | `04 e0 48 28 / 66 cb f8 06 / 81 19 d3 26 / e5 9a 7a 4c` | 第 1 欄 `d4 bf 5d 30` → `04 66 81 e5`；04 = 02•d4 ⊕ 03•bf ⊕ 5d ⊕ 30（式 5.8，[S04 p.23]） |
| ④ AddRoundKey（round key 1：`a0 88 23 2a / fa 54 a3 6c / fe 2c 39 76 / 17 b1 39 05`） | `a4 68 6b 02 / 9c 9f 5b 6a / 7f 35 ea 50 / f2 2b 43 49` | 04 ⊕ a0 = a4 |

**解密時**倒著走：再 XOR 同一把 round key（得回 `04 e0 48 28…`）→ InvMixColumns → InvShiftRows（每列往右移回）→ InvSubBytes（反查 S-box），最後回到 `19 a0 9a e9…` [S04 p.26]。

表中每個數值都與 FIPS 197 附錄 B 相同；Content Validation 另以獨立的 AES 參考實作（`Workflow/validators/aes_ref.py`）從輸入與金鑰重算，並確認解密方向能還原。

## 常見誤解

- 「AES-256 的區塊是 256 位元」——錯。256 指的是**金鑰長度**，三種 AES 的區塊大小都是 128 位元 [S04 p.9]。
- 「DES 仍是目前的加密標準」——錯。DES 已於 2005 年撤銷核准 [S06 p.32]。

## 關聯

- 是一種區塊加密：[[sym-block-vs-stream]]
- 實際使用時要搭配操作模式：[[mode-overview]]、[[mode-gcm-aead]]
- 在 HTTPS/TLS 1.3 中用來加密資料：[[app-hybrid-tls]]

## 來源引文

- [S04 p.4 §3] "The AES algorithm is a symmetric block cipher that can encrypt (encipher) and decrypt (decipher) digital information."
- [S04 p.4 §3] "The AES algorithm is capable of using cryptographic keys of 128, 192, and 256 bits to encrypt and decrypt data in blocks of 128 bits."
- [S04 p.3 Abstract] "In 2000, NIST announced the selection of the Rijndael block cipher family as the winner of the Advanced Encryption Standard (AES) competition."
- [S04 p.9 §1] "In 1997, NIST initiated the Advanced Encryption Standard (AES) development effort [1] and called for the public to submit candidate algorithms for block ciphers."
- [S04 p.9 §1] "This Standard specifies three instantiations of Rijndael: AES-128, AES-192, and AES-256, where the suffix indicates the bit length of the key."
- [S04 p.9 §1] "The block size (i.e., the length of the data inputs and outputs) is 128 bits in each case."
- [S04 p.9 §1] "Rijndael supports additional block sizes and key lengths that are not adopted in this Standard."
- [S04 p.19 §4/§5 Eq.5.1] "AES-128(in , key) = CIPHER(in, 10, KEYEXPANSION(key)) AES-192(in, key) = CIPHER(in, 12, KEYEXPANSION(key)) AES-256(in, key) = CIPHER(in, 14, KEYEXPANSION(key))"
- [S04 p.20 §5.1] "The rounds in the specification of CIPHER() are composed of the following four byte-oriented transformations on the state"
- [S04 p.20 §5.1] "MIXCOLUMNS() mixes the data within each column of the state array."
- [S04 p.21 §5.1.1] "SUBBYTES() is an invertible, non-linear transformation of the state in which a substitution table, called an S-box, is applied independently to each byte in the state."
- [S04 p.22 §5.1.2] "SHIFTROWS() is a transformation of the state in which the bytes in the last three rows of the state are cyclically shifted."
- [S04 p.24 §5.1.4] "ADDROUNDKEY() is a transformation of the state in which a round key is combined with the state by applying the bitwise XOR operation."
- [S04 p.10 §2.1] "The sequence consists of four transformations, except for one iteration, in which one of the transformations is omitted."
- [S06 p.33 §3.2.1.4] "The Advanced Encryption Standard (AES) was developed as a replacement for DES and TDEA and is the preferred block cipher algorithm for new products."
- [S06 p.32 §3.2.1.1] "due to advances in computer power and speeds, the strength of the DES algorithm is no longer sufficient to adequately protect Federal Government information."
- [S06 p.32 §3.2.1.1] "DES was withdrawn as an approved algorithm in 2005"
- [S12 p.68 §5.6.1.1 Table 2] "128 AES-128 L = 3072 N = 256 k = 3072"
- [S12 p.68 §5.6.1.1] "algorithm/key-size combinations that have been estimated at a maximum security strength of less than 112 bits"
- [S01 p.268 security by obscurity] "For example, NIST used a long, public process to select AES to replace DES."
- [S04 p.9 §1] "Appendix B gives a step-by-step example of an invocation of AES-128."
- [S04 p.42 App.B] "Input = 32 43 f6 a8 88 5a 30 8d 31 31 98 a2 e0 37 07 34"
- [S04 p.42 App.B] "Key = 2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c"
- [S04 p.42 App.B Start of Round 1] "19 a0 9a e9 3d f4 c6 f8 e3 e2 8d 48 be 2b 2a 08"
- [S04 p.42 App.B After SubBytes] "d4 e0 b8 1e 27 bf b4 41 11 98 5d 52 ae f1 e5 30"
- [S04 p.42 App.B After ShiftRows] "d4 e0 b8 1e bf b4 41 27 5d 52 11 98 30 ae f1 e5"
- [S04 p.42 App.B After MixColumns] "04 e0 48 28 66 cb f8 06 81 19 d3 26 e5 9a 7a 4c"
- [S04 p.42 App.B Round Key 1] "a0 88 23 2a fa 54 a3 6c fe 2c 39 76 17 b1 39 05"
- [S04 p.42 App.B Start of Round 2] "a4 68 6b 02 9c 9f 5b 6a 7f 35 ea 50 f2 2b 43 49"
- [S04 p.22 §5.1.1] "the substitution value would be determined by the intersection of the row with index ‘5’ and the column with index ‘3’ in Table 4"
- [S04 p.23 §5.1.3] "MIXCOLUMNS() is a transformation of the state that multiplies each of the four columns of the state by a single fixed matrix"
- [S04 p.23 §5.1.3 Eq.5.8] "so that the individual output bytes are defined as follows: 0s = ({02}• s0,c) ⊕ ({03}• s1,c) ⊕ s2,c ⊕ s3,c"
- [S04 p.26 §5.3] "To implement INVCIPHER(), the transformations in the specification of CIPHER() (Section 5.1) are inverted and executed in reverse order."
- [S04 p.26 §5.3] "The inverted transformations of the state — denoted by INVSHIFTROWS(), INVSUBBYTES(), INVMIXCOLUMNS(), and ADDROUNDKEY()"
