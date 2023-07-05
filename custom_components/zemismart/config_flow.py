import voluptuous as vol

from homeassistant import config_entries
from .const import DOMAIN, DEVICE_IP, DEVICE_KEY, _LOGGER, DEVICE_ID
from .utils import getData


@config_entries.HANDLERS.register(DOMAIN)
class FlowHandler(config_entries.ConfigFlow):
    """Handle a config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        return await self.async_step_device_select()

    async def async_step_device_select(self, user_input=None):
        return await self.async_step_device_manual()

    async def async_step_device_data(self, user_input=None):
        errors = {}
        self.deviceKey = ""

        if user_input is not None:
            try:
                self.deviceKey = user_input[DEVICE_KEY]

                data = await getData(
                    self.hass, self.deviceID, self.deviceKey, self.deviceIP
                )

                if data:
                    return self.async_create_entry(
                        title=self.deviceIP,
                        data={
                            DEVICE_IP: self.deviceIP,
                            DEVICE_KEY: self.deviceKey,
                            DEVICE_ID: self.deviceID,
                        },
                    )
                else:
                    errors["base"] = "auth_error"

            except Exception as e:
                errors["base"] = "unknown"
                _LOGGER.error(e)

        return self.async_show_form(
            step_id="device_data",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        DEVICE_KEY, description={"suggested_value": self.deviceKey}
                    ): str,
                }
            ),
            errors=errors,
        )

    async def async_step_device_manual(self, user_input=None):
        errors = {}
        self.deviceIP = ""
        self.deviceID = ""
        self.deviceKey = ""

        if user_input is not None:
            try:
                self.deviceIP = user_input[DEVICE_IP]
                self.deviceID = user_input[DEVICE_ID]
                self.deviceKey = user_input[DEVICE_KEY]

                data = await getData(
                    self.hass, self.deviceID, self.deviceKey, self.deviceIP
                )
                if data:
                    return self.async_create_entry(
                        title=self.deviceIP,
                        data={
                            DEVICE_IP: self.deviceIP,
                            DEVICE_KEY: self.deviceKey,
                            DEVICE_ID: self.deviceID,
                        },
                    )
                else:
                    errors["base"] = "auth_error"

            except Exception as e:
                errors["base"] = "unknown"
                _LOGGER.error(e)

        return self.async_show_form(
            step_id="device_manual",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        DEVICE_IP, description={"suggested_value": self.deviceIP}
                    ): str,
                    vol.Required(
                        DEVICE_ID, description={"suggested_value": self.deviceID}
                    ): str,
                    vol.Required(
                        DEVICE_KEY, description={"suggested_value": self.deviceKey}
                    ): str,
                }
            ),
            errors=errors,
        )
