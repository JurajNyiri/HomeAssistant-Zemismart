from .const import (
    UDP_KEY,
    _LOGGER,
    MAX_GET_DATA_RETRIES,
    DOMAIN,
    DEVICE_IP,
    SUPPORTED_PRODUCT_KEYS,
    SUPPORTED_VERSIONS,
)
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import tinytuya
import asyncio


async def getData(hass, deviceID, deviceKey, deviceIP, retry=True, retries=0):
    if retries >= MAX_GET_DATA_RETRIES:
        return False
    else:
        try:
            client = tinytuya.Device(deviceID, deviceIP, deviceKey)
            client.set_version(3.3)
            data = await hass.async_add_executor_job(
                client.status,
            )
            return data
        except Exception:
            await asyncio.sleep(1)
            return await getData(
                hass, deviceID, deviceKey, deviceIP, retry, retries + 1
            )


def getDiscoveredDevices(hass):
    discoveredDevices = list()
    devices = hass.data[DOMAIN]["discovery"].devices
    if len(devices) > 0:
        existingEntries = hass.config_entries.async_entries(DOMAIN)
        savedIPs = list()
        for entry in existingEntries:
            savedIPs.append(entry.data.get(DEVICE_IP))
        for ip in devices:
            device = devices[ip]
            if ip not in savedIPs:
                if (
                    device["productKey"] in SUPPORTED_PRODUCT_KEYS
                    and device["version"] in SUPPORTED_VERSIONS
                ):
                    discoveredDevices.append(ip)
                else:
                    _LOGGER.warn(
                        "Discovered device "
                        + device["productKey"]
                        + " ("
                        + ip
                        + ") with version "
                        + device["version"]
                        + " not currently supported."
                    )
    return discoveredDevices


async def setState(
    hass, deviceID, deviceKey, deviceIP, dpsValue, dpsIndex: int, retry=True, retries=0
):
    if retries >= MAX_GET_DATA_RETRIES:
        return False
    else:
        try:
            client = tinytuya.Device(deviceID, deviceIP, deviceKey)
            client.set_version(3.3)
            data = await hass.async_add_executor_job(
                client.set_value, dpsIndex, dpsValue
            )
            return data
        except Exception:
            await asyncio.sleep(1)
            return setState(
                deviceID, deviceKey, deviceIP, dpsValue, dpsIndex, retry, retries + 1
            )


def decrypt_udp(message):
    """Decrypt encrypted UDP broadcasts."""

    def _unpad(data):
        return data[: -ord(data[len(data) - 1 :])]

    cipher = Cipher(algorithms.AES(UDP_KEY), modes.ECB(), default_backend())
    decryptor = cipher.decryptor()
    return _unpad(decryptor.update(message) + decryptor.finalize()).decode()
