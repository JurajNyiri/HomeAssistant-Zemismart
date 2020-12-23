"""Discovery module for Tuya devices.

Entirely based on discovery.py from localtuya:

https://github.com/rospogrigio/localtuya/blob/master/custom_components/localtuya/discovery.py
"""
import asyncio
import json
from .const import _LOGGER, DEFAULT_DISCOVER_TIMEOUT, SUPPORTED_DEVICES
from .utils import decrypt_udp


class TuyaDiscovery(asyncio.DatagramProtocol):
    """Datagram handler listening for Tuya broadcast messages."""

    def __init__(self, callback=None):
        """Initialize a new BaseDiscovery."""
        self.devices = {}
        self._listeners = []
        self._callback = callback

    async def start(self):
        """Start discovery by listening to broadcasts."""
        loop = asyncio.get_running_loop()
        listener = loop.create_datagram_endpoint(
            lambda: self, local_addr=("0.0.0.0", 6666)
        )
        encrypted_listener = loop.create_datagram_endpoint(
            lambda: self, local_addr=("0.0.0.0", 6667)
        )

        self.listeners = await asyncio.gather(listener, encrypted_listener)
        _LOGGER.debug("Listening to broadcasts on UDP port 6666 and 6667")

    def close(self):
        """Stop discovery."""
        self.callback = None
        for transport, _ in self.listeners:
            transport.close()

    def datagram_received(self, data, addr):
        """Handle received broadcast message."""
        data = data[20:-8]
        try:
            data = decrypt_udp(data)
        except Exception:
            data = data.decode()

        decoded = json.loads(data)
        self.device_found(decoded)

    def device_found(self, device):
        """Discover a new device."""
        if device.get("ip") not in self.devices:
            if (
                device.get("productKey") in SUPPORTED_DEVICES
                and device.get("version") == "3.3"
            ):
                self.devices[device.get("ip")] = device
                _LOGGER.debug("Added device: %s", device)
            _LOGGER.debug("Discovered device: %s", device)

        if self._callback:
            self._callback(device)


async def discover():
    """Discover and return devices on local network."""
    discover = TuyaDiscovery()
    try:
        await discover.start()
        await asyncio.sleep(DEFAULT_DISCOVER_TIMEOUT)
    except Exception:
        _LOGGER.exception("failed to discover devices")
    finally:
        discover.close()
    return discover