import asyncio
import time
from .const import UDP_KEY, _LOGGER
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from tuyaface.tuyaclient import TuyaClient


def getData(deviceID, deviceKey, deviceIP):
    device = {
        "protocol": "3.3",
        "deviceid": deviceID,
        "localkey": deviceKey,
        "ip": deviceIP,
    }

    try:
        client = TuyaClient(device)
        client.start()
        data = client.status()
        while data == None:
            data = client.status()
            _LOGGER.warn("Retrying getting data in 1 second...")
            time.sleep(1)
        client.stop_client()
        return data
    except Exception as e:
        _LOGGER.error(e)
    return False


def setState(deviceID, deviceKey, deviceIP, dpsValue, dpsIndex: int):
    device = {
        "protocol": "3.3",
        "deviceid": deviceID,
        "localkey": deviceKey,
        "ip": deviceIP,
    }

    try:
        client = TuyaClient(device)
        client.start()
        data = client.set_state(dpsValue, dpsIndex)
        while data != True:
            data = client.set_state(dpsValue, dpsIndex)
            _LOGGER.warn("Retrying setting data in 1 second...")
            time.sleep(1)
        client.stop_client()
        return data
    except Exception as e:
        _LOGGER.error(e)
    return False


def decrypt_udp(message):
    """Decrypt encrypted UDP broadcasts."""

    def _unpad(data):
        return data[: -ord(data[len(data) - 1 :])]

    cipher = Cipher(algorithms.AES(UDP_KEY), modes.ECB(), default_backend())
    decryptor = cipher.decryptor()
    return _unpad(decryptor.update(message) + decryptor.finalize()).decode()
