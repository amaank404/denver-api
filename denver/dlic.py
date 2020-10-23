"""
Denver type license
"""

from getmac import get_mac_address
from . import crypt
from hashlib import sha256
from base64 import urlsafe_b64encode as encodebytes


def generate_license(name, date_of_expiry, device_binding = None, encryption_key = None):
    pass


def generate_device_binding(device_information=None):
    if device_information is None:
        device_information = get_mac_address().encode()
    return crypt.encrypt(device_information, sha256(device_information).digest())


def decrypt_device_binding(bindings, device_information=None):
    if device_information is None:
        device_information = get_mac_address().encode()
    return crypt.decrypt(bindings, sha256(device_information).digest())
