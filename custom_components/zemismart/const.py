import logging
import voluptuous as vol
from hashlib import md5
from homeassistant.components.climate.const import (
    PRESET_ECO,
    SUPPORT_PRESET_MODE,
    SUPPORT_SWING_MODE,
    SUPPORT_TARGET_TEMPERATURE,
    HVAC_MODE_OFF,
    HVAC_MODE_HEAT,
    PRESET_AWAY,
    PRESET_HOME,
    PRESET_SLEEP,
    PRESET_NONE,
)
from homeassistant.helpers import config_validation as cv


HVAC_MODE_MANUAL = "manual"
HVAC_MODE_UNKNOWN = "unknown"

ENTITY_ID = "entity_id"
SENSOR = "sensor"

DEFAULT_DISCOVER_TIMEOUT = 6.0
DOMAIN = "zemismart"
_LOGGER = logging.getLogger(__name__)
UDP_KEY = md5(b"yGAdlopoPVldABfn").digest()

DEVICE_IP = "DEVICE_IP"
DEVICE_KEY = "DEVICE_KEY"
DEVICE_ID = "DEVICE_ID"
SUPPORTED_DEVICES = ["3uoeudsge0ooafig"]
SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_SWING_MODE | SUPPORT_PRESET_MODE
HVAC_MODES = [HVAC_MODE_OFF, HVAC_MODE_HEAT]
PRESET_MODES = [PRESET_NONE, PRESET_ECO, PRESET_AWAY, PRESET_HOME, PRESET_SLEEP]
SWING_MODES = [2, 3, 4, 5, 6, 7, 8, 9]

SERVICE_LOCK = "set_led_mode"
SCHEMA_SERVICE_LOCK = {vol.Required(ENTITY_ID): cv.string}
SERVICE_UNLOCK = "set_led_mode"
SCHEMA_SERVICE_UNLOCK = {vol.Required(ENTITY_ID): cv.string}
SERVICE_USE_SENSOR = "use_sensor"
SCHEMA_SERVICE_USE_SENSOR = {
    vol.Required(ENTITY_ID): cv.string,
    vol.Required(SENSOR): vol.In(["internal", "external", "both"]),
}
