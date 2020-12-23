from homeassistant.core import HomeAssistant
from .const import DOMAIN, _LOGGER
from .discovery import TuyaDiscovery
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.config_entries import ConfigEntry


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the LocalTuya integration component."""

    hass.data[DOMAIN] = {}
    hass.data[DOMAIN]["discovery"] = TuyaDiscovery()

    def handleShutdown(event):
        """Clean up resources when shutting down."""
        hass.data[DOMAIN]["discovery"].close()

    try:
        await hass.data[DOMAIN]["discovery"].start()
        hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, handleShutdown)
    except Exception:
        _LOGGER.exception("failed to set up discovery")

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "climate")
    )
    return True
