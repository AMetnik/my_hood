import logging
from homeassistant.components.switch import SwitchEntity
from .my_hood import MyHoodInstance

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    device_address = hass.data["my_hood"].get("device_address")
    async_add_entities([HoodPowerSwitch(device_address)])

class HoodPowerSwitch(SwitchEntity):
    def __init__(self, device_address):
        self._attr_name = "Hood light"
        self._attr_unique_id = f"hood_light_{device_address.replace(':', '')}"
        self._is_on = False
        self.hood = MyHoodInstance(device_address)

    async def async_turn_on(self, **kwargs):
        try:
            await self.hood.turn_on()
            self._is_on = True
        except Exception as e:
            _LOGGER.error(f"My_Hood: Failed to set light on: {e}")
        finally:
            self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        try:
            await self.hood.turn_off()
            self._is_on = False
        except Exception as e:
            _LOGGER.error(f"My_Hood: Failed to set light off: {e}")
        finally:
            self.async_write_ha_state()

    @property
    def is_on(self):
        return self._is_on
