"""
This is very useful module in-case of cipher encrypting and decrypting of data.
This contains many cipher methods. The Best of all is the vigenere cipher which
is also used in these modern times.

The Source code is taken from the book "Cracking Codes with Python". Although
hacking methods for all the ciphers are not created, the hackers can still
break the code by using different techniques.
"""

__version__ = "2020.6.4"
__author__ = "Xcodz"

import math
import cryptography.fernet
import base64


class crypto_math:
    def gcd(a, b):
        while a != 0:
            a, b = b % a, a
        return b

    def findModInverse(a, m):
        if crypto_math.gcd(a, m) != 1:
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


class cVig:
    l = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def translateMessage(key, message, mode):
        l = cVig.l
        t = []
        ki = 0
        k = key.upper()
        for x in message:
            n = l.find(x.upper())
            if n != -1:
                if mode == "e":
                    n += l.find(key[ki])
                elif mode == "d":
                    n -= l.find(key[ki])
                n %= len(l)
                if x.isupper():
                    t.append(l[n])
                elif x.islower():
                    t.append(l[n].lower())
                ki += 1
                if ki == len(key):
                    ki = 0
            else:
                t.append(x)
        return "".join(t)


class cSub:
    l = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def keyIsValid(key):
        keyList = list(key)
        lettersList = list(cSub.l)
        keyList.sort()
        return keyList == lettersList

    def translateMessage(key: str, message: str, mode):
        t = ""
        ca = cSub.l
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


class cAffine:
    def getKeyParts(key):
        a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."
        keyA = key // len(a)
        keyB = key % len(a)
        return keyA, keyB

    def checkKeys(keyA, keyB):
        a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."
        if keyA < 0 or keyB < 0 or keyB > len(a) - 1:
            return False
        if crypto_math.gcd(keyA, len(a)) != 1:
            return False
        return True


class crypt:
    class morse:
        table = {
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

        def encode(st: str):
            """MORSE CODE ENCODER

            A ' ' MEANS PARTITION BETWEEN LETTERS
            A '/' MEANS PARTITION BETWEEN WORDS"""
            t = ""
            tb = {v: k for k, v in crypt.morse.table.items()}
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

        def decode(s: str):
            tb = crypt.morse.table.copy()
            d = [x.split() for x in s.split("/")]
            t = ""
            for x in d:
                for y in x:
                    t += tb[y]
                t += " "
            return t[0:-1]

    class basic:
        def encode(b: bytes = b""):
            """Encode Bytes to String"""
            d = [hex(x)[2:] for x in list(b)]
            for x in range(len(d)):
                if len(d[x]) == 1:
                    d[x] = "0" + d[x]
            return "".join(d)

        def decode(s: str):
            return bytes([int("0x" + s[x] + s[x + 1], 0) for x in range(0, len(s), 2)])

    class cipher:
        class reverse:
            def crypt(s: str):
                """ENCODING AND DECODING FUNCTIONS ARE SAME"""
                t = ""
                i = len(s) - 1
                while i >= 0:
                    t += s[i]
                    i -= 1
                return t

        class caesar:
            def encrypt(s: str, k: int):
                """Encrypts with Caesar cipher"""
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

        class transposition:
            def encrypt(message: str, key: int):
                # Each string in ciphertext represents a column in the grid:
                ciphertext = [""] * key
                # Loop through each column in ciphertext:
                for column in range(key):
                    currentIndex = column
                    # Keep looping until currentIndex goes past the message length:
                    while currentIndex < len(message):
                        # Place the character at currentIndex in message at the
                        # end of the current column in the ciphertext list:
                        ciphertext[column] += message[currentIndex]
                        # Move currentIndex over:
                        currentIndex += key
                # Convert the ciphertext list into a single string value and return it:
                return "".join(ciphertext)

            def decrypt(message: str, key: int):
                numOfColumns = int(math.ceil(len(message) / float(key)))
                numOfRows = key
                numOfShadedBoxes = (numOfColumns * numOfRows) - len(message)
                plaintext = [""] * numOfColumns
                column = row = 0
                for symbol in message:
                    plaintext[column] += symbol
                    column += 1
                    if (column == numOfColumns) or (
                        column == numOfColumns - 1
                        and row >= numOfRows - numOfShadedBoxes
                    ):
                        column = 0
                        row += 1
                return "".join(plaintext)

        class affine:
            def encrypt(message: str, key: int):
                a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."
                ka, kb = cAffine.getKeyParts(key)
                if cAffine.checkKeys(ka, kb):
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

            def decrypt(message: str, key: int):
                a = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 !?."
                ka, kb = cAffine.getKeyParts(key)
                if cAffine.checkKeys(ka, kb):
                    pt = ""
                    mioka = crypto_math.findModInverse(ka, len(a))
                    for x in message:
                        if x in a:
                            si = a.find(x)
                            pt += a[(si - kb) * mioka % len(a)]
                        else:
                            pt += x
                    return pt
                else:
                    return message

        class substitution:
            def encrypt(m: str, key: str):
                return cSub.translateMessage(key, m, "e")

            def decrypt(m: str, key: str):
                return cSub.translateMessage(key, m, "d")

        class vigenere:
            def encrypt(m: str, k: str):
                return cVig.translateMessage(k, m, "e")

            def decrypt(m: str, k: str):
                return cVig.translateMessage(k, m, "d")


def encrypt(data: bytes, key: bytes) -> bytes:
    machine = cryptography.fernet.Fernet(base64.urlsafe_b64encode(key))
    return machine.encrypt(data)


def decrypt(data: bytes, key: bytes) -> bytes:
    machine = cryptography.fernet.Fernet(base64.urlsafe_b64encode(key))
    try:
        return machine.decrypt(data)
    except cryptography.fernet.InvalidToken:
        return b""
