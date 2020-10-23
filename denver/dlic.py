"""
Denver type license
"""

from getmac import get_mac_address
from .crypt import crypt
from hashlib import sha256


def generate_license(name, date_of_expiry, device_binding = None, encryption_key = None):
    pass


def generate_device_binding(device_information=None):
    if device_information is None:
        device_information = get_mac_address()
    return crypt.cipher.vigenere.encrypt(device_information, sha256(device_information.encode()).hexdigest())


def decrypt_device_binding(bindings, device_information=None):
    if device_information is None:
        device_information = get_mac_address()
    return crypt.cipher.vigenere.decrypt(bindings, sha256(device_information.encode()).hexdigest())