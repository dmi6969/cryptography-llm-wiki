"""Text normalisation shared by validators.

PDF 抽取的文字常有斷行連字號、連字（ﬁ）、彎引號、多餘空白。為了讓「引文必須逐字出現在原文」
的檢查不被排版雜訊干擾，比對時把兩邊都壓成只剩字母與數字的小寫字串（squash）。
"""
from __future__ import annotations

import re
import unicodedata


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("­", "")  # soft hyphen
    # 去掉重音符號：PDF 把 Vigenère 抽成 "Vigen`ere"，兩邊都還原成 vigenere 才能比對
    s = "".join(ch for ch in unicodedata.normalize("NFKD", s) if not unicodedata.combining(ch))
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def squash(s: str, fold_fi: bool = False) -> str:
    r = re.sub(r"[\W_]+", "", norm(s))
    # 部分 PDF（例：FIPS 197 upd1）的 "fi" 連字 ToUnicode 對應錯誤，抽取後只剩 "f"
    # （specified→specifed）。對這類來源，比對時兩邊都把 fi 摺成 f。
    return r.replace("fi", "f") if fold_fi else r


# 連字遺失的「症狀字」：正常英文不會出現，出現多次代表抽取時 fi 被吃掉
_LIG_MARKERS = re.compile(
    r"\b(specifed|defned|defnes?|frst|fnite|fxed|fnal|confdential\w*|identif(?:ed|er)s?|"
    r"modifcation|coeffcients?|suffx|signifcant\w*|effcient\w*)\b", re.I)


def ligature_loss_markers(text: str) -> int:
    return len(_LIG_MARKERS.findall(text))


LIGATURE_LOSS_THRESHOLD = 5


def cjk_len(s: str) -> int:
    """顯示長度：中日韓字元算 1，英數單字也大致以字元計（粗估閱讀負擔用）。"""
    return len(re.sub(r"\s+", "", s))
