---
id: S02
type: source
title: "Handbook of Applied Cryptography, Chapter 1: Overview of Cryptography"
url: https://cacr.uwaterloo.ca/hac/about/chap1.pdf
publisher: CRC Press（A. Menezes, P. van Oorschot, S. Vanstone）；University of Waterloo CACR 提供下載
year: 1996
nodes: [intro-what-is-crypto, intro-terminology, intro-kerckhoffs, classical-caesar, classical-substitution, classical-transposition, classical-limitations]
---

# S02 — Handbook of Applied Cryptography, Ch.1 Overview of Cryptography

## 摘要

應用密碼學經典教科書的第 1 章，是全書的導論：密碼學的定義與四大目標、基本術語與兩方通訊模型、
Kerckhoffs 原則、對稱式加密（含替換與換位密碼）、數位簽章、公開金鑰密碼學。
本 Wiki 以它作為 **大學教材層級的概念主幹**。

## 本 Wiki 使用的章節

| 章節 | 抽取頁碼（= 書頁 + 1） | 用於節點 |
|---|---|---|
| §1.1 Introduction | p.2–3 | [[intro-what-is-crypto]] |
| §1.2 Information security and cryptography（Def. 1.1、四大目標） | p.5 | [[intro-what-is-crypto]] |
| §1.4 Basic terminology and concepts | p.12–16 | [[intro-terminology]]、[[intro-kerckhoffs]] |
| §1.5.1 Ex.1.25（位移 3 的範例） | p.16 | [[classical-caesar]] |
| §1.5.2 Substitution / transposition ciphers | p.18–19 | [[classical-substitution]]、[[classical-transposition]]、[[classical-limitations]] |
| §1.5.3 Composition of ciphers | p.20 | [[classical-transposition]] |

## 備註

- 出版於 1996 年（PDF 標示 ©1997），部分「現況」描述已過時，例如 DES 的地位；使用時以 NIST 現行文件校正。
- PDF 以 TeX 字型排版，抽取後數學符號會失真（例如集合括號），**只引用文字敘述**。
- 授權僅允許個人保存一份，因此原始 PDF 只留在本機 `Wiki/raw/`。
