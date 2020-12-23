import time
from attr import attr
from homeassistant.components.climate.const import (
    PRESET_AWAY,
    PRESET_ECO,
    PRESET_HOME,
    PRESET_NONE,
    PRESET_SLEEP,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.climate import ClimateEntity
from homeassistant.util import slugify
from homeassistant.const import (
    ATTR_TEMPERATURE,
    SERVICE_LOCK,
    SERVICE_UNLOCK,
    TEMP_CELSIUS,
)
from homeassistant.helpers import entity_platform
from typing import Callable
from .const import (
    SCHEMA_SERVICE_CALIBRATE,
    SCHEMA_SERVICE_LOCK,
    SCHEMA_SERVICE_UNLOCK,
    SCHEMA_SERVICE_USE_SENSOR,
    SERVICE_CALIBRATE,
    SERVICE_USE_SENSOR,
    SUPPORT_FLAGS,
    HVAC_MODES,
    DEVICE_IP,
    DEVICE_ID,
    DEVICE_KEY,
    SWING_MODES,
    _LOGGER,
    HVAC_MODE_OFF,
    HVAC_MODE_HEAT,
    PRESET_MODES,
)
from .utils import getData, setState


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: Callable
):
    platform = entity_platform.current_platform.get()
    platform.async_register_entity_service(
        SERVICE_LOCK,
        SCHEMA_SERVICE_LOCK,
        "lock",
    )
    platform = entity_platform.current_platform.get()
    platform.async_register_entity_service(
        SERVICE_UNLOCK,
        SCHEMA_SERVICE_UNLOCK,
        "unlock",
    )
    platform = entity_platform.current_platform.get()
    platform.async_register_entity_service(
        SERVICE_USE_SENSOR,
        SCHEMA_SERVICE_USE_SENSOR,
        "use_sensor",
    )
    platform = entity_platform.current_platform.get()
    platform.async_register_entity_service(
        SERVICE_CALIBRATE,
        SCHEMA_SERVICE_CALIBRATE,
        "calibrate",
    )
    try:
        dps = getData(
            entry.data.get(DEVICE_ID),
            entry.data.get(DEVICE_KEY),
            entry.data.get(DEVICE_IP),
        )["dps"]
        return async_add_entities(
            [
                ZemismartClimateEntity(
                    hass,
                    entry,
                    dps,
                )
            ]
        )
    except Exception as e:
        _LOGGER.error(e)
    return False


class ZemismartClimateEntity(ClimateEntity):
    def __init__(self, hass: HomeAssistant, entry: dict, dps):
        super().__init__()
        self._unit = "C"
        self._icon = "mdi:alert-decagram"
        self.deviceIP = entry.data.get(DEVICE_IP)
        self.deviceID = entry.data.get(DEVICE_ID)
        self.deviceKey = entry.data.get(DEVICE_KEY)
        self.dps = dps

    def manualUpdate(self):
        self.dps = getData(self.deviceID, self.deviceKey, self.deviceIP)["dps"]
        print(self.dps)

    @property
    def should_poll(self):
        return True

    @property
    def unit_of_measurement(self):
        return self._unit

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        if self.dps["1"]:
            return HVAC_MODE_HEAT
        else:
            return HVAC_MODE_OFF

    @property
    def supported_features(self):
        return SUPPORT_FLAGS

    @property
    def name(self):
        return slugify(f"zemismart_{self.deviceIP}")

    @property
    def device_state_attributes(self):
        attributes = {}

        attributes["locked"] = self.dps["6"]
        attributes["overheat_protection"] = self.dps["12"] == "1"
        attributes["external_temperature"] = self.dps["101"]

        if self.dps["102"] == "0":
            attributes["sensor"] = "Internal"
        elif self.dps["102"] == "1":
            attributes["sensor"] = "External"
        elif self.dps["102"] == "2":
            attributes["sensor"] = "Internal & External"
        else:
            attributes["sensor"] = "Unknown"

        attributes["temperature_calibration"] = self.dps["103"]
        attributes["heating"] = self.dps["105"]
        attributes["window_mode"] = self.dps["107"]
        attributes["optimal_start"] = self.dps["108"]

        return attributes

    @property
    def temperature_unit(self):
        return TEMP_CELSIUS

    @property
    def target_temperature(self):
        return float(self.dps["2"])

    @property
    def hvac_modes(self):
        return HVAC_MODES

    @property
    def hvac_mode(self):
        return self.state()

    @property
    def swing_modes(self):
        return SWING_MODES

    @property
    def swing_mode(self):
        return self.dps["104"]

    @property
    def preset_mode(self):
        if self.dps["4"] == "1":
            return PRESET_HOME
        elif self.dps["4"] == "2":
            return PRESET_AWAY
        elif self.dps["4"] == "3":
            return PRESET_ECO
        elif self.dps["4"] == "4":
            return PRESET_SLEEP
        return PRESET_NONE

    @property
    def preset_modes(self):
        return PRESET_MODES

    @property
    def current_temperature(self):
        return float(self.dps["3"])

    @property
    def min_temp(self):
        return 18

    @property
    def max_temp(self):
        return 30

    def update(self):
        self.manualUpdate()

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        elif temperature >= 18 and temperature <= 30:  # todo
            setState(self.deviceID, self.deviceKey, self.deviceIP, int(temperature), 2)
            time.sleep(1)
        else:
            _LOGGER.warn(
                "Chosen temperature=%s is incorrect. It needs to be between 18 and 30.",  # todo
                str(temperature),
            )

    def set_preset_mode(self, preset):
        if preset == PRESET_NONE:
            setState(self.deviceID, self.deviceKey, self.deviceIP, str(0), 4)
        elif preset == PRESET_HOME:
            setState(self.deviceID, self.deviceKey, self.deviceIP, str(1), 4)
        elif preset == PRESET_AWAY:
            setState(self.deviceID, self.deviceKey, self.deviceIP, str(2), 4)
        elif preset == PRESET_ECO:
            setState(self.deviceID, self.deviceKey, self.deviceIP, str(3), 4)
        elif preset == PRESET_SLEEP:
            setState(self.deviceID, self.deviceKey, self.deviceIP, str(4), 4)
        else:
            _LOGGER.warn("Chosen preset=%s is incorrect preset.", str(preset))

        time.sleep(1)

    def set_hvac_mode(self, hvac_mode):
        if hvac_mode == HVAC_MODE_HEAT:
            setState(self.deviceID, self.deviceKey, self.deviceIP, True, 1)
        elif hvac_mode == HVAC_MODE_OFF:
            setState(self.deviceID, self.deviceKey, self.deviceIP, False, 1)
        else:
            _LOGGER.warn("Chosen hvac_mode=%s is incorrect preset.", str(hvac_mode))

        time.sleep(1)

    def set_swing_mode(self, swing_value):
        if int(swing_value) > 9 or int(swing_value) < 2:
            _LOGGER.warn("Chosen swing value %s is incorrect.", str(swing_value))
        else:
            setState(
                self.deviceID, self.deviceKey, self.deviceIP, int(swing_value), 104
            )

        time.sleep(1)

    def turn_on(self):
        setState(self.deviceID, self.deviceKey, self.deviceIP, True, 1)
        time.sleep(1)

    def turn_off(self):
        setState(self.deviceID, self.deviceKey, self.deviceIP, False, 1)
        time.sleep(1)

    def lock(self):
        setState(self.deviceID, self.deviceKey, self.deviceIP, True, 6)
        time.sleep(1)

    def unlock(self):
        setState(self.deviceID, self.deviceKey, self.deviceIP, False, 6)
        time.sleep(1)

    def use_sensor(self, sensor):
        if sensor == "both":
            setState(self.deviceID, self.deviceKey, self.deviceIP, str(2), 102)
        elif sensor == "external":
            setState(self.deviceID, self.deviceKey, self.deviceIP, str(1), 102)
        elif sensor == "internal":
            setState(self.deviceID, self.deviceKey, self.deviceIP, str(0), 102)
        time.sleep(1)

    def calibrate(self, difference):
        if int(difference) > -10 and int(difference) < 10:
            setState(self.deviceID, self.deviceKey, self.deviceIP, int(difference), 103)
        else:
            _LOGGER.warn("Chosen difference %s is incorrect.", str(difference))
        time.sleep(1)