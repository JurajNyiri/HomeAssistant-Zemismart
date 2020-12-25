import time
from .const import UDP_KEY, _LOGGER, MAX_GET_DATA_RETRIES, DOMAIN, DEVICE_IP
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from tuyaface.tuyaclient import TuyaClient


def getData(deviceID, deviceKey, deviceIP, retry=True):
    device = {
        "protocol": "3.3",
        "deviceid": deviceID,
        "localkey": deviceKey,
        "ip": deviceIP,
    }
    retries = 0

    try:
        client = TuyaClient(device)
        client.start()
        data = client.status()
        while data is None and retry and retries < MAX_GET_DATA_RETRIES:
            data = client.status()
            _LOGGER.warn("Retrying getting data in 1 second...")
            retries += 1
            time.sleep(1)

        client.stop_client()
        return data
    except Exception as e:
        _LOGGER.error(e)
    return False


def getDiscoveredDevices(hass):
    discoveredDevices = list()
    devices = hass.data[DOMAIN]["discovery"].devices
    if len(devices) > 0:
        print(devices)
        discoveredIPs = list(devices.keys())
        existingEntries = hass.config_entries.async_entries(DOMAIN)
        savedIPs = list()
        for entry in existingEntries:
            savedIPs.append(entry.data.get(DEVICE_IP))
        for ip in discoveredIPs:
            if ip not in savedIPs:
                discoveredDevices.append(ip)
    return discoveredDevices


def setState(deviceID, deviceKey, deviceIP, dpsValue, dpsIndex: int, retry=True):
    device = {
        "protocol": "3.3",
        "deviceid": deviceID,
        "localkey": deviceKey,
        "ip": deviceIP,
    }
    retries = 0

    try:
        client = TuyaClient(device)
        client.start()
        data = client.set_state(dpsValue, dpsIndex)
        while data is not True and retry and retries < MAX_GET_DATA_RETRIES:
            data = client.set_state(dpsValue, dpsIndex)
            _LOGGER.warn("Retrying setting data in 1 second...")
            retries += 1
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
