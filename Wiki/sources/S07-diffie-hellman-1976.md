---
id: S07
type: source
title: "New Directions in Cryptography"
url: https://ee.stanford.edu/~hellman/publications/24.pdf
publisher: IEEE Transactions on Information Theory, IT-22(6)（W. Diffie, M. E. Hellman）；Stanford 提供
year: 1976
nodes: [asym-public-key, asym-key-exchange]
---

# S07 — Diffie & Hellman (1976), New Directions in Cryptography

## 摘要

開創公開金鑰密碼學的論文。指出對稱式系統的「金鑰分配問題」是商業網路通訊的主要障礙，
提出 **public key cryptosystem**（加密金鑰可公開、解密金鑰保密）與 **public key distribution system**（在公開通道上協議共享金鑰）兩種方向，
並給出以「有限體上取對數很困難」為基礎的金鑰交換方法（今日稱 Diffie–Hellman 金鑰交換）。

## 本 Wiki 使用的章節

| 章節 | 抽取頁碼 | 用於節點 |
|---|---|---|
| §I Introduction（公開金鑰系統、金鑰分配問題） | p.1 | [[asym-public-key]]、[[asym-key-exchange]] |
| §III Public Key Cryptography（金鑰交換方法） | p.6 | [[asym-key-exchange]] |

## 備註

- 此 PDF 為掃描檔的 OCR 文字，**數學式嚴重失真**（例如 α 被辨識成 01、cr），只引用文字敘述；公式依論文描述以標準寫法重述。
