"""
Denver type license
"""

from getmac import get_mac_address
from . import crypt
from hashlib import sha256
from base64 import urlsafe_b64encode as encodebytes


def generate_license(name, date_of_expiry=None, device_binding=None, encryption_key=None):
    if device_binding is not None:
        device_binding = [hex() for x in device_binding]
    licence_file = {
        "name": name,
        "device_binding": device_binding,
        "date_of_expiry": date_of_expiry
    }


def generate_date_of_expiry(year, month=1, date=1, /):
    return ''.join(year, month, date, )


def generate_device_binding(device_information=None):
    if device_information is None:
        device_information = get_mac_address().encode()
    return crypt.encrypt(device_information, sha256(device_information).digest())


def decrypt_device_binding(bindings, device_information=None):
    if device_information is None:
        device_information = get_mac_address().encode()
    return crypt.decrypt(bindings, sha256(device_information).digest())
