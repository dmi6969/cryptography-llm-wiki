---
id: intro-what-is-crypto
title: 密碼學是什麼？為什麼需要它？
topic: T1
aliases: [Cryptography, 密碼學, information security, 資訊安全]
sources: [S01, S02]
prerequisites: []
relations:
  - {type: related, target: intro-terminology}
  - {type: related, target: asym-signature}
facts: {}
---

# 密碼學是什麼？為什麼需要它？

## 定義

**密碼學（cryptography）** 是研究「與資訊安全相關的數學技術」的學問，目標包括機密性、資料完整性、實體鑑別與資料來源鑑別 [S02 p.5]。
RFC 4949 的白話說法：把資料轉換成**看不懂的形式**、**防止資料被偷偷竄改**、**防止未經授權的使用**；如果轉換可逆，也負責把資料還原 [S01 p.90]。

## 重點

- **為什麼需要**：密碼學原本主要服務軍事、外交與政府；1960 年代電腦與通訊普及後，民間也開始需要保護數位資訊 [S02 p.2]。
- **密碼學的四大目標**（HAC 的框架）[S02 p.5]：
  1. **機密性（confidentiality）**：只有被授權的人能看到內容 [S02 p.5][S01 p.94]
  2. **資料完整性（data integrity）**：能偵測資料是否被未授權地修改 [S02 p.5][S01 p.95]
  3. **鑑別（authentication，確認身分或來源）**：確認通訊對象是誰、資料從哪裡來 [S02 p.5][S01 p.26]
  4. **不可否認性（non-repudiation）**：讓人無法否認自己做過的承諾或動作 [S02 p.5][S01 p.200]
- 密碼學的本質是「預防與偵測作弊及其他惡意行為」[S02 p.5]。
- 密碼學不是保護資訊的唯一方法，而是其中一組技術 [S02 p.5]。
- 不同目標由不同工具達成：加密主要負責機密性；完整性、不可否認性需要雜湊函數、數位簽章等其他工具 [S02 p.5]（見 [[asym-signature]]）。

## 範例

- 網路購物時：信用卡號不能被看到（機密性）、訂單金額不能被改（完整性）、要確定連到的是真正的商店（鑑別）、商店不能事後否認收到訂單（不可否認性）。——本 Wiki 的教學補充例子，對應四大目標的定義 [S02 p.5]。

## 常見誤解

- **時效註記**：HAC 寫於 1996 年，書中提到 DES「仍是許多金融機構的標準」[S02 p.2]；較新的 RFC 4949（2007）則記載 NIST 以公開程序選出 AES 來取代 DES [S01 p.268]。本 Wiki 以較新的來源為準，不把 DES 當成現行標準（見 [[sym-aes]]）。

## 關聯

- 下一步先認識基本術語：[[intro-terminology]]
- 「不可否認性」靠數位簽章達成：[[asym-signature]]

## 來源引文

- [S02 p.5 §1.2 Def.1.1] "Cryptography is the study of mathematical techniques related to aspects of information security such as confidentiality, data integrity, entity authentication, and data origin authentication."
- [S02 p.5 §1.2] "Cryptography is not the only means of providing information security, but rather one set of techniques."
- [S02 p.5 §1.2] "Confidentiality is a service used to keep the content of information from all but those authorized to have it."
- [S02 p.5 §1.2] "Data integrity is a service which addresses the unauthorized alteration of data."
- [S02 p.5 §1.2] "Authentication is a service related to identification."
- [S02 p.5 §1.2] "Non-repudiation is a service which prevents an entity from denying previous commitments or actions."
- [S02 p.5 §1.2] "Cryptography is about the prevention and detection of cheating and other malicious activities."
- [S02 p.5 §1.2] "Examples of primitives include encryption schemes"
- [S02 p.2 §1.1] "The proliferation of computers and communications systems in the 1960s brought with it a demand from the private sector for means to protect information in digital form and to provide security services."
- [S02 p.2 §1.1] "It remains the standard means for securing electronic commerce for many financial institutions around the world."
- [S01 p.90 cryptography] "The mathematical science that deals with transforming data to render its meaning unintelligible (i.e., to hide its semantic content), prevent its undetected alteration, or prevent its unauthorized use."
- [S01 p.94 data confidentiality] "The property that data is not disclosed to system entities unless they have been authorized to know the data."
- [S01 p.95 data integrity] "The property that data has not been changed, destroyed, or lost in an unauthorized or accidental manner."
- [S01 p.26 authentication] "The process of verifying a claim that a system entity or system resource has a certain attribute value."
- [S01 p.200 non-repudiation service] "A security service that provide protection against false denial of involvement in an association"
- [S01 p.268 security by obscurity] "For example, NIST used a long, public process to select AES to replace DES."
