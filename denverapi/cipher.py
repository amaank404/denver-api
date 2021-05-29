"""
This module provides cipher encrypting and decrypting of data.
This contains many cipher methods. The Best of all is the vigenere cipher (but not better than AES Encryption provided by encryption module).

The Source code is taken from the book "Cracking Codes with Python". Although
hacking methods for all the ciphers are not created, the hackers can still
break the code by using different techniques, so it is recommended you should
go for `denverapi.encryption`.
"""

__version__ = "2021.2.24"
__author__ = "Xcodz"

import math


def _crypto_math_gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def _crypto_math_find_mod_inverse(a, m):
    if _crypto_math_gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (
            (u1 - q * v1),
            (u2 - q * v2),
            (u3 - q * v3),
            v1,
            v2,
            v3,
        )
    return u1 % m


_cvig_l = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _cvig_translate_message(key, message, mode):
    key_list = _cvig_l
    t = []
    ki = 0
    for x in message:
        n = key_list.find(x.upper())
        if n != -1:
            if mode == "e":
                n += key_list.find(key[ki])
            elif mode == "d":
                n -= key_list.find(key[ki])
            n %= len(key_list)
            if x.isupper():
                t.append(key_list[n])
            elif x.islower():
                t.append(key_list[n].lower())
            ki += 1
            if ki == len(key):
                ki = 0
        else:
            t.append(x)
    return "".join(t)


_csub_l = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _csub_translate_message(key: str, message: str, mode):
    t = ""
    ca = _csub_l
    cb = key
    if mode == "d":
        ca, cb = cb, ca
    for x in message:
        if x.upper() in ca:
            si = ca.find(x.upper())
            if x.isupper():
                t += cb[si].upper()
            else:
                t += cb[si].lower()
        else:
            t += x
    return t


def _caffine_get_key_parts(key):
    a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."
    key_a = key // len(a)
    key_b = key % len(a)
    return key_a, key_b


def _caffine_check_keys(key_a, key_b):
    a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."
    if key_a < 0 or key_b < 0 or key_b > len(a) - 1:
        return False
    if _crypto_math_gcd(key_a, len(a)) != 1:
        return False
    return True


class morse:
    """
    Provides static methods for morse code.
    """

    table = (
        {  # If you find more morse code stuff to include, Please start a Pull Request
            ".-": "A",
            "-...": "B",
            "-.-.": "C",
            "-..": "D",
            ".": "E",
            "..-.": "F",
            "--.": "G",
            "....": "H",
            "..": "I",
            ".---": "J",
            "-.-": "K",
            ".-..": "L",
            "--": "M",
            "-.": "N",
            "---": "O",
            ".--.": "P",
            "--.-": "Q",
            ".-.": "R",
            "...": "S",
            "-": "T",
            "..-": "U",
            "...-": "V",
            ".--": "W",
            "-..-": "X",
            "-.--": "Y",
            "--..": "Z",
            ".----": "1",
            "..---": "2",
            "...--": "3",
            "....-": "4",
            ".....": "5",
            "-....": "6",
            "--...": "7",
            "---..": "8",
            "----.": "9",
            "-----": "0",
        }
    )

    @staticmethod
    def encode(st: str):
        """
        A Function to encode with morse code

        A ' ' means partition between letters
        A '/' means partition between words
        """
        t = ""
        tb = {v: k for k, v in morse.table.items()}
        s = list(st.upper())
        for x in s:
            if x not in tb.keys() and x != " ":
                s.remove(x)
        w = []
        for x in s:
            if x == " ":
                t += " ".join(w) + "/"
                w = []
            else:
                w.append(tb[x])
        t += " ".join(w)
        return t

    @staticmethod
    def decode(s: str):
        """
        A Function to decode data encoded in morse code.
        """
        tb = morse.table.copy()
        d = [x.split() for x in s.split("/")]
        t = ""
        for x in d:
            for y in x:
                t += tb[y]
            t += " "
        return t[0:-1]


class basic:
    @staticmethod
    def encode(b: bytes = b""):
        """Encode Bytes to Hexadecimal String"""
        d = [hex(x)[2:] for x in list(b)]
        for x in range(len(d)):
            if len(d[x]) == 1:
                d[x] = "0" + d[x]
        return "".join(d)

    @staticmethod
    def decode(s: str):
        """
        Decode Bytes from Hexadecimal String
        """
        return bytes([int("0x" + s[x] + s[x + 1], 0) for x in range(0, len(s), 2)])


class reverse_cipher:
    @staticmethod
    def crypt(s: str):
        """
        Reverses the provided string
        """
        return "".join(reversed(s))


class caesar_cipher:
    @staticmethod
    def encrypt(s: str, k: int):
        """
        Encrypts with Caesar cipher
        """
        a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."
        t = ""
        for x in s:
            if x in a:
                si = a.find(x)
                ti = si + k
                if ti >= len(a):
                    ti -= len(a)
                elif ti < 0:
                    ti += len(a)
                t += a[ti]
            else:
                t += x
        return t

    @staticmethod
    def decrypt(s: str, k: int):
        """Decrypts with caesar cipher"""
        a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."
        t = ""
        for x in s:
            if x in a:
                si = a.find(x)
                ti = si - k
                if ti >= len(a):
                    ti -= len(a)
                elif ti < 0:
                    ti += len(a)
                t += a[ti]
            else:
                t += x
        return t


class transposition_cipher:
    @staticmethod
    def encrypt(message: str, key: int):
        """
        Encrypt using transposition cipher
        """
        # Each string in ciphertext represents a column in the grid:
        ciphertext = [""] * key
        # Loop through each column in ciphertext:
        for column in range(key):
            current_index = column
            # Keep looping until current_index goes past the message length:
            while current_index < len(message):
                # Place the character at current_index in message at the
                # end of the current column in the ciphertext list:
                ciphertext[column] += message[current_index]
                # Move current_index over:
                current_index += key
        # Convert the ciphertext list into a single string value and return it:
        return "".join(ciphertext)

    @staticmethod
    def decrypt(message: str, key: int):
        """
        decrypt using transpositon cipher
        """
        num_of_columns = int(math.ceil(len(message) / float(key)))
        num_of_rows = key
        num_of_shaded_boxes = (num_of_columns * num_of_rows) - len(message)
        plaintext = [""] * num_of_columns
        column = row = 0
        for symbol in message:
            plaintext[column] += symbol
            column += 1
            if (column == num_of_columns) or (
                column == num_of_columns - 1
                and row >= num_of_rows - num_of_shaded_boxes
            ):
                column = 0
                row += 1
        return "".join(plaintext)


class affine_cipher:
    @staticmethod
    def encrypt(message: str, key: int):
        """
        Encode using affine cipher
        """
        a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."
        ka, kb = _caffine_get_key_parts(key)
        if _caffine_check_keys(ka, kb):
            ct = ""
            for x in message:
                if x in a:
                    si = a.find(x)
                    ct += a[(si * ka + kb) % len(a)]
                else:
                    ct += x
            return ct
        else:
            return message

    @staticmethod
    def decrypt(message: str, key: int):
        """
        Decrypt using affine cipher
        """
        a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."
        ka, kb = _caffine_get_key_parts(key)
        if _caffine_check_keys(ka, kb):
            pt = ""
            mioka = _crypto_math_find_mod_inverse(ka, len(a))
            for x in message:
                if x in a:
                    si = a.find(x)
                    pt += a[(si - kb) * mioka % len(a)]
                else:
                    pt += x
            return pt
        else:
            return message


class substitution_cipher:
    @staticmethod
    def encrypt(m: str, key: str):
        """
        encrypt using substitution cipher
        """
        return _csub_translate_message(key, m, "e")

    @staticmethod
    def decrypt(m: str, key: str):
        """
        decrypt using substitution cipher
        """
        return _csub_translate_message(key, m, "d")


class vigenere_cipher:
    @staticmethod
    def encrypt(m: str, k: str):
        """
        encrypt using vigenere cipher
        """
        return _cvig_translate_message(k, m, "e")

    @staticmethod
    def decrypt(m: str, k: str):
        """
        decrypt using vigenere cipher
        """
        return _cvig_translate_message(k, m, "d")
