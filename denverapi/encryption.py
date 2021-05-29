"""
Provides functions for encryption of data using AES encryption.

The data returned after encryption is in this format:

`{len(salt)};{len(nonce)};{len(tag)}/{salt}{nonce}{tag}{encrypted_text}`
"""

import hashlib
from typing import Union

from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

__author__ = "xcodz-dot"
__version__ = "2021.2.24"


def _encode_entries(salt: bytes, nonce: bytes, tag: bytes, cipher_text: bytes):
    salt_len = str(len(salt)).encode("utf-8")
    nonce_len = str(len(nonce) + len(salt)).encode("utf-8")
    tag_len = str(len(tag) + len(nonce) + len(salt)).encode("utf-8")
    return (
        b";".join([salt_len, nonce_len, tag_len])
        + b"/"
        + salt
        + nonce
        + tag
        + cipher_text
    )


def _decode_entries(data: bytes):
    len_sector, data_sector = data.split(b"/", 1)
    salt_len, nonce_len, tag_len = map(int, len_sector.split(b";"))
    salt = data_sector[0:salt_len]
    nonce = data_sector[salt_len:nonce_len]
    tag = data_sector[nonce_len:tag_len]
    data = data_sector[tag_len:]
    return (salt, nonce, tag), data


def encrypt(message: Union[bytes, str], password: Union[bytes, str]) -> bytes:
    """
    Encrypts the provided `message` using `password` with randomly generated salt and returns it
    """
    if isinstance(message, str):
        message = message.encode("utf-8")
    if isinstance(password, str):
        password = password.encode("utf-8")

    salt = get_random_bytes(AES.block_size)

    private_key = hashlib.scrypt(
        password,
        salt=salt,
        n=2 ** 14,
        r=8,
        p=1,
        dklen=32,
    )

    cipher_config = AES.new(private_key, AES.MODE_GCM)
    (cipher_text, tag) = cipher_config.encrypt_and_digest(message)

    encrypted_string = _encode_entries(salt, cipher_config.nonce, tag, cipher_text)
    return encrypted_string


def decrypt(encrypted_data: bytes, password: Union[str, bytes]) -> bytes:
    """
    Decrypts the provided `encrypted_data` using `password` and returns it
    """
    (salt, nonce, tag), cipher_text = _decode_entries(encrypted_data)

    private_key = hashlib.scrypt(
        password.encode() if isinstance(password, str) else password,
        salt=salt,
        n=2 ** 14,
        r=8,
        p=1,
        dklen=32,
    )

    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)

    return decrypted
