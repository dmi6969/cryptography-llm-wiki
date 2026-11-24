"""獨立的 AES-128 參考實作（依 FIPS 197 的定義從頭計算，不使用任何密碼學套件）。

用途：Content Validation 的 C4 用它重算簡報中「AES 一輪四步」的每個矩陣，
確認簡報與 Wiki 引用的 FIPS 197 附錄 B 數值一致，也確認解密步驟真的能還原。
state 以「列」表示：rows[r][c]，位元組依 FIPS 197 §3.4 以欄為主序填入。
"""
from __future__ import annotations


def _xtime(b: int) -> int:                      # FIPS 197 §4.2：乘以 {02}
    b <<= 1
    return (b ^ 0x1B) & 0xFF if b & 0x100 else b


def _mul(a: int, b: int) -> int:                # GF(2^8) 乘法
    r = 0
    while b:
        if b & 1:
            r ^= a
        a, b = _xtime(a), b >> 1
    return r


def _inv(a: int) -> int:                        # 乘法反元素（0 → 0）
    if a == 0:
        return 0
    r = 1
    for _ in range(254):                        # a^254 = a^-1
        r = _mul(r, a)
    return r


def _sbox_entry(x: int) -> int:                 # FIPS 197 §5.1.1：反元素 + 仿射轉換
    b = _inv(x)
    out = 0
    for i in range(8):
        bit = (b >> i ^ b >> (i + 4) % 8 ^ b >> (i + 5) % 8 ^ b >> (i + 6) % 8 ^ b >> (i + 7) % 8 ^ 0x63 >> i) & 1
        out |= bit << i
    return out


SBOX = [_sbox_entry(x) for x in range(256)]
INV_SBOX = [0] * 256
for _i, _v in enumerate(SBOX):
    INV_SBOX[_v] = _i


def to_state(hex16: str) -> list[list[int]]:
    b = bytes.fromhex(hex16)
    return [[b[r + 4 * c] for c in range(4)] for r in range(4)]


def rows_hex(s: list[list[int]]) -> list[str]:
    return [" ".join(f"{v:02x}" for v in row) for row in s]


def add_round_key(s, k):
    return [[s[r][c] ^ k[r][c] for c in range(4)] for r in range(4)]


def sub_bytes(s):
    return [[SBOX[v] for v in row] for row in s]


def inv_sub_bytes(s):
    return [[INV_SBOX[v] for v in row] for row in s]


def shift_rows(s):
    return [s[r][r:] + s[r][:r] for r in range(4)]


def inv_shift_rows(s):
    return [s[r][-r:] + s[r][:-r] if r else s[r][:] for r in range(4)]


def _mix(s, m):
    return [[_mul(m[r][0], s[0][c]) ^ _mul(m[r][1], s[1][c]) ^ _mul(m[r][2], s[2][c]) ^ _mul(m[r][3], s[3][c])
             for c in range(4)] for r in range(4)]


MIX = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]          # FIPS 197 式 (5.6)(5.7)
INV_MIX = [[14, 11, 13, 9], [9, 14, 11, 13], [13, 9, 14, 11], [11, 13, 9, 14]]  # 式 (5.13)


def mix_columns(s):
    return _mix(s, MIX)


def inv_mix_columns(s):
    return _mix(s, INV_MIX)


def round_key_1(key_hex: str) -> list[list[int]]:
    """AES-128 金鑰擴展的第 1 把 round key（FIPS 197 §5.2）。"""
    k = bytes.fromhex(key_hex)
    w = [list(k[4 * i:4 * i + 4]) for i in range(4)]
    t = w[3][1:] + w[3][:1]                     # ROTWORD
    t = [SBOX[x] for x in t]                    # SUBWORD
    t[0] ^= 0x01                                # Rcon[1]
    nw = []
    prev = t
    for i in range(4):
        prev = [a ^ b for a, b in zip(w[i], prev)] if i == 0 else [a ^ b for a, b in zip(w[i], nw[-1])]
        nw.append(prev)
    return [[nw[c][r] for c in range(4)] for r in range(4)]


def round1_frames(input_hex: str, key_hex: str) -> dict[str, list[list[int]]]:
    k0, k1 = to_state(key_hex), round_key_1(key_hex)
    start = add_round_key(to_state(input_hex), k0)
    sub = sub_bytes(start)
    sh = shift_rows(sub)
    mix = mix_columns(sh)
    end = add_round_key(mix, k1)
    return {"input": to_state(input_hex), "key": k0, "start": start, "sub": sub, "shift": sh,
            "mix": mix, "roundkey": k1, "end": end,
            # 解密方向：反運算、倒序執行（FIPS 197 §5.3）
            "dec_addkey": add_round_key(end, k1), "dec_invmix": inv_mix_columns(add_round_key(end, k1)),
            "dec_invshift": inv_shift_rows(inv_mix_columns(add_round_key(end, k1))),
            "dec_invsub": inv_sub_bytes(inv_shift_rows(inv_mix_columns(add_round_key(end, k1))))}


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    f = round1_frames("3243f6a8885a308d313198a2e0370734", "2b7e151628aed2a6abf7158809cf4f3c")
    for k, v in f.items():
        print(f"{k:12s}", " | ".join(rows_hex(v)))
