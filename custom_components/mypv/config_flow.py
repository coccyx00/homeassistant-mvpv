"""Config flow for Kostal piko integration."""

import json

import requests
from requests.exceptions import ConnectTimeout, HTTPError
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_DEVICE, CONF_HOST, CONF_MONITORED_CONDITIONS
from homeassistant.core import HomeAssistant, callback
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.selector import TextSelector, TextSelectorConfig

from .const import DOMAIN, MYPV_DEVICES, SENSOR_TYPES  # pylint:disable=unused-import

SUPPORTED_SENSOR_TYPES = list(SENSOR_TYPES)

DEFAULT_HOST = "192.168.178.0"
DEFAULT_DEVICE = "Unknown"
DEFAULT_MONITORED_CONDITIONS = ["device"]


@callback
def mypv_entries(hass: HomeAssistant):
    """Return the hosts for the domain."""
    return {
        entry.data[CONF_HOST] for entry in hass.config_entries.async_entries(DOMAIN)
    }


class MypvConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Mypv config flow."""

    VERSION = 1

    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._errors = {}
        self._info = {}

    def _host_in_configuration_exists(self, host) -> bool:
        """Return True if site_id exists in configuration."""
        if host in mypv_entries(self.hass):
            return True
        return False

    def _check_host(self, host) -> bool:
        """Check if we can connect to the mypv."""
        try:
            response = requests.get(f"http://{host}/mypv_dev.jsn", timeout=10)
            self._info = json.loads(response.text)
        except (ConnectTimeout, HTTPError):
            self._errors[CONF_HOST] = "could_not_connect"
            return False

        return True

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        if user_input is not None:
            if self._host_in_configuration_exists(user_input[CONF_HOST]):
                self._errors[CONF_HOST] = "host_exists"
            else:
                device = user_input[CONF_DEVICE]
                host = user_input[CONF_HOST]
                conditions = user_input[CONF_MONITORED_CONDITIONS]
                can_connect = await self.hass.async_add_executor_job(
                    self._check_host, host
                )
                if can_connect and device == DEFAULT_DEVICE:
                    user_input[CONF_DEVICE] = self._info["device"]
                    # getting the known sensors for this device
                    device_short = MYPV_DEVICES[user_input[CONF_DEVICE]]
                    user_input[CONF_MONITORED_CONDITIONS] = []
                    for k, e in SENSOR_TYPES.items():
                        if device_short in e.device.split(" "):
                            user_input[CONF_MONITORED_CONDITIONS].append(k)
                if can_connect and device != DEFAULT_DEVICE:
                    return self.async_create_entry(
                        title=f"{self._info['device']} {self._info['number']}",
                        data={
                            CONF_HOST: host,
                            CONF_MONITORED_CONDITIONS: conditions,
                        },
                    )
        else:
            user_input = {}
            user_input[CONF_HOST] = DEFAULT_HOST
            user_input[CONF_DEVICE] = DEFAULT_DEVICE
            user_input[CONF_MONITORED_CONDITIONS] = DEFAULT_MONITORED_CONDITIONS

        setup_schema = vol.Schema(
            {
                vol.Required(CONF_HOST, default=user_input[CONF_HOST]): str,
                vol.Required(
                    CONF_DEVICE, default=user_input[CONF_DEVICE]
                ): TextSelector(TextSelectorConfig(read_only=True)),
                vol.Required(
                    CONF_MONITORED_CONDITIONS,
                    default=user_input[CONF_MONITORED_CONDITIONS],
                ): cv.multi_select(SUPPORTED_SENSOR_TYPES),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=setup_schema, errors=self._errors
        )

    async def async_step_import(self, user_input=None):
        """Import a config entry."""
        if self._host_in_configuration_exists(user_input[CONF_HOST]):
            return self.async_abort(reason="host_exists")
        return await self.async_step_user(user_input)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler for the config entry."""
        return MypvOptionsFlowHandler(config_entry)


class MypvOptionsFlowHandler(config_entries.OptionsFlow):
    """Handles options flow."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        # self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(
                title="",
                data={
                    CONF_MONITORED_CONDITIONS: user_input[CONF_MONITORED_CONDITIONS],
                    "use_all_sensors": user_input["use_all_sensors"],
                    "polling_interval": user_input["polling_interval"],
                },
            )

        options_schema = vol.Schema(
            {
                vol.Required(
                    "polling_interval",
                    default=self.config_entry.options.get("polling_interval", 10),
                ): int,
                vol.Optional(
                    "use_all_sensors",
                    default=self.config_entry.options.get("use_all_sensors", False),
                ): bool,
                vol.Required(
                    CONF_MONITORED_CONDITIONS,
                    default=self.config_entry.options.get(
                        CONF_MONITORED_CONDITIONS, DEFAULT_MONITORED_CONDITIONS
                    ),
                ): cv.multi_select(SUPPORTED_SENSOR_TYPES),
            }
        )

        return self.async_show_form(step_id="init", data_schema=options_schema)
