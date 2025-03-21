import asyncio
import logging
from homeassistant.components.select import SelectEntity
from homeassistant.helpers.entity import Entity
from .my_hood import MyHoodInstance

LOGGER = logging.getLogger(__name__)

LOGGER.info("My_Hood : select.py is loading!")

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    #"""Set up HoodSuctionSelect from YAML."""
    LOGGER.info("My_Hood : select.py - setup platform")
    device_address = hass.data["my_hood"].get("device_address")
    async_add_entities([HoodSuctionSelect(device_address)])


class HoodSuctionSelect(SelectEntity):
    def __init__(self, device_address):
        #"""Initialize the select entity."""
        LOGGER.info("My_Hood : select.py - __init__")
        self._attr_name = "Hood Suction Level"
        self._attr_options = ["Off", "Low", "Medium", "High", "Max"]
        self._attr_current_option = "Off"
        self._attr_unique_id = f"hood_suction_{device_address.replace(':', '')}"  # Unik ID baseret på BLE-adresse
        self.hood = MyHoodInstance(device_address)  # Giv BLE-adressen til din klasse

    async def async_select_option(self, option):
        #"""Handle selecting an option."""
        LOGGER.info("My_Hood : select.py - async_select_option")
        option_map = {
            "Off": "0",
            "Low": "1",
            "Medium": "2",
            "High": "3",
            "Max": "4",
        }
        if option in option_map:
            await self.hood.set_hood_suction(option_map[option])
            self._attr_current_option = option
            self.async_write_ha_state()
