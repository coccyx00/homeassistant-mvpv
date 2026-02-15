"""Provides the MYPV DataUpdateCoordinator."""

import asyncio
from datetime import timedelta
import json
import logging

import requests

from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util.dt import utcnow

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MYPVDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching MYPV data."""

    def __init__(self, hass: HomeAssistant, *, config: dict, options: dict) -> None:
        """Initialize global NZBGet data updater."""
        self._host = config[CONF_HOST]
        self.host = config[CONF_HOST]
        self._info = None
        self._setup = None
        self._firmware = None
        self._next_update = 0
        self._next_update_firmware = 0
        self.update_interval = timedelta(seconds=10)

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=self.update_interval,
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from NZBGet."""

        def _update_data() -> dict:
            """Fetch data from NZBGet via sync functions."""
            data = self.json_update("data")
            if self._info is None:
                self._info = self.json_update("mypv_dev")

            if self._setup is None or self._next_update < utcnow().timestamp():
                self._next_update = utcnow().timestamp() + 120  # 86400
                self._setup = self.json_update("setup")

            if (
                self._firmware is None
                or self._next_update_firmware < utcnow().timestamp()
            ):
                self._next_update_firmware = utcnow().timestamp() + (7 * 86400)
                # @todo self._firmware = self.firmware_update()

            return {
                "data": data,
                "info": self._info,
                "setup": self._setup,
                "firmware": self._firmware,
            }

        try:
            async with asyncio.timeout(4):
                return await self.hass.async_add_executor_job(_update_data)
        except Exception as error:
            raise UpdateFailed(f"Invalid response from API: {error}") from error

    def set_interval(self, new_interval: int):
        """Update polling interval."""
        self.update_interval = timedelta(seconds=new_interval)

    def json_update(self, page: str):
        """Update inverter data."""
        try:
            response = requests.get(f"http://{self._host}/{page}.jsn", timeout=10)
            data = json.loads(response.text)
            _LOGGER.debug(data)
        except (requests.RequestException, json.JSONDecodeError) as error:
            _LOGGER.error("Failed to update JSON data: %s", error)
            return None
        else:
            return data

    def firmware_update(self):
        """Read the firmware info."""
        try:
            response = requests.get(
                "https://www.my-pv.com/download/currentversion.php?sn="
                + self._info.get("sn"),
                timeout=10,
            )
            info = json.loads(response.text)
            _LOGGER.debug(info)
        except requests.RequestException:
            _LOGGER.error("Failed to load firmware info")
            return json.loads("{}")
        except json.JSONDecodeError:
            _LOGGER.error("Failed to decode JSON")
            return json.loads("{}")
        else:
            return info
