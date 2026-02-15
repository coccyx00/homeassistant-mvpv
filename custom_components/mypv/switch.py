"""Switch for mypv."""

import json
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DATA_COORDINATOR, DOMAIN, MYPV_SWITCHES, SENSOR_TYPES
from .coordinator import MYPVDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up switch sensor entities when the config entry is loaded.

    This function retrieves the coordinator from hass.data,
    creates switch entities based on MYPV_SWITCHES,
    and registers them with Home Assistant.

    Args:
        hass: Home Assistant instance.
        entry: Configuration entry.
        async_add_entities: Callback to add entities.
    """

    # Retrieve the coordinator instance from hass data and add entities
    coordinator: MYPVDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id][
        DATA_COORDINATOR
    ]
    entities = [MYPVSwitch(coordinator, switch_name) for switch_name in MYPV_SWITCHES]
    async_add_entities(entities)


class MYPVSwitch(CoordinatorEntity, SwitchEntity):
    """Representation of a switch entity for MyPV.

    Sensor state is read and write asynchronously via
    the coordinator communicating with the device.
    """

    def __init__(
        self, coordinator: MYPVDataUpdateCoordinator, switch_name: str
    ) -> None:
        """Initialize the switch entity.

        Args:
            coordinator: The data update coordinator instance.
            switch_name: the identifier in SENSOR_TYPES
        """
        super().__init__(coordinator)
        if switch_name not in SENSOR_TYPES:
            raise KeyError
        self.coordinator = coordinator

        self._icon = SENSOR_TYPES[switch_name].icon
        self._sensor = SENSOR_TYPES[switch_name].name_long
        self.type = switch_name

        self.serial_number = self.coordinator.data["info"]["sn"]
        self.fwversion = self.coordinator.data["info"]["fwversion"]
        self.model = self.coordinator.data["info"]["device"]

        self.on_value = 1
        # if elwa for bstmode 1 is 2
        if self.type == "bstmode":
            self.on_value = 2

        # Store the key and definition
        self._key = switch_name
        self._name = SENSOR_TYPES[switch_name].name_long

        # Assign the entity type to the coordinator mapping
        # self.coordinator._entity_types[self._key] = self.entity_type

        # Set entity attributes from definition
        self._attr_unique_id = f"mypv_{switch_name}_sw"
        self._attr_has_entity_name = True
        self._attr_translation_key = switch_name

        # Internal state variables
        self._state = None
        # self._register = definition["register"]

        # Optional: disable entity by default if specified in the definition
        # if definition.get("enabled_by_default") is False:
        #    self._attr_entity_registry_enabled_default = False

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._sensor}"

    @property
    def entity_type(self) -> str:
        """Return the type of this entity for logging purposes.

        This allows the coordinator to show more descriptive messages.
        """
        return "switch"

    @property
    def available(self) -> bool:
        """Return True if the coordinator has successfully fetched data.

        Used by Home Assistant to determine entity availability.
        """
        return self.coordinator.last_update_success

    @property
    def is_on(self) -> bool | None:
        """Return True if switch sensor is on, False if off, None if unknown."""
        data = self.coordinator.data["setup"]
        if data is None or self._key not in data:
            return None

        current_value = data[self._key]
        return current_value == self.on_value

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the switch on via the coordinator."""

        # Write the value using the coordinator's async HTTP session
        session = async_get_clientsession(self.hass)
        async with session.get(
            f"http://{self.coordinator.host}/setup.jsn?{self.type}={self.on_value}"
        ) as resp:
            response_text = await resp.read()
            json_data = json.loads(response_text)
            self.coordinator.data["setup"][self.type] = json_data[self.type]

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the switch off via the coordinator."""

        # Write the value using the coordinator's method
        session = async_get_clientsession(self.hass)
        async with session.get(
            f"http://{self.coordinator.host}/setup.jsn?{self.type}=0"
        ) as resp:
            response_text = await resp.read()
            json_data = json.loads(response_text)
            self.coordinator.data["setup"][self.type] = json_data[self.type]

    async def async_update(self):
        """Return sensor state."""

        data = self.coordinator.data
        if data is None or self._key not in data:
            return None

        current_value = data[self._key]
        return current_value == 1

    @property
    def device_info(self):
        """Return information about the device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.serial_number)},
            manufacturer="MYPV",
            model=self.model,
            name=self._name,
            sw_version=self.fwversion,
            hw_version=None,
        )
