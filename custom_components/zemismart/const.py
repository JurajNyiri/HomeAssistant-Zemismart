import logging
import voluptuous as vol
from hashlib import md5
from homeassistant.components.climate.const import (
    PRESET_ECO,
    ClimateEntityFeature,
    HVACMode,
    PRESET_AWAY,
    PRESET_HOME,
    PRESET_SLEEP,
    PRESET_NONE,
)
from homeassistant.helpers import config_validation as cv


MAX_GET_DATA_RETRIES = 3
HVAC_MODE_MANUAL = "manual"
HVAC_MODE_UNKNOWN = "unknown"

STATE = "state"
ENTITY_ID = "entity_id"
SENSOR = "sensor"
DIFFERENCE = "difference"

DEFAULT_DISCOVER_TIMEOUT = 6.0
DOMAIN = "zemismart"
_LOGGER = logging.getLogger(__name__)
UDP_KEY = md5(b"yGAdlopoPVldABfn").digest()

DEVICE_IP = "DEVICE_IP"
DEVICE_KEY = "DEVICE_KEY"
DEVICE_ID = "DEVICE_ID"
SUPPORTED_DEVICES = ["3uoeudsge0ooafig"]
SUPPORT_FLAGS = ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.SWING_MODE | ClimateEntityFeature.PRESET_MODE
HVAC_MODES = [HVACMode.OFF, HVACMode.HEAT]
PRESET_MODES = [PRESET_NONE, PRESET_ECO, PRESET_AWAY, PRESET_HOME, PRESET_SLEEP]
SWING_MODES = [2, 3, 4, 5, 6, 7, 8, 9]

SERVICE_LOCK = "lock"
SCHEMA_SERVICE_LOCK = {vol.Required(ENTITY_ID): cv.string}
SERVICE_UNLOCK = "unlock"
SCHEMA_SERVICE_UNLOCK = {vol.Required(ENTITY_ID): cv.string}
SERVICE_USE_SENSOR = "use_sensor"
SCHEMA_SERVICE_USE_SENSOR = {
    vol.Required(ENTITY_ID): cv.string,
    vol.Required(SENSOR): vol.In(["internal", "external", "both"]),
}
SERVICE_CALIBRATE = "calibrate"
SCHEMA_SERVICE_CALIBRATE = {
    vol.Required(ENTITY_ID): cv.string,
    vol.Required(DIFFERENCE): vol.In(
        [-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    ),
}
SERVICE_WINDOW_MODE = "window_mode"
SCHEMA_SERVICE_WINDOW_MODE = {
    vol.Required(ENTITY_ID): cv.string,
    vol.Required(STATE): vol.In(["on", "off"]),
}
SERVICE_OPTIMAL_START_MODE = "optimal_start"
SCHEMA_SERVICE_OPTIMAL_START_MODE = {
    vol.Required(ENTITY_ID): cv.string,
    vol.Required(STATE): vol.In(["on", "off"]),
}
ADD_MANUALLY = "Add manually"

SUPPORTED_PRODUCT_KEYS = ["3uoeudsge0ooafig"]
SUPPORTED_VERSIONS = ["3.3"]

DEFAULT_DPS = {
    "1": True,
    "2": 0,
    "3": 0,
    "4": "0",
    "6": False,
    "12": 0,
    "101": 0,
    "102": "0",
    "103": 0,
    "104": 0,
    "105": False,
    "107": False,
    "108": False,
    "110": 5,
}
