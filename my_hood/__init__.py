"""My Hood BLE Integration"""
import logging
import asyncio
from homeassistant.helpers import discovery

DOMAIN = "my_hood"
LOGGER = logging.getLogger(__name__)

async def async_setup(hass, config):
    #"""Set up My Hood from configuration.yaml."""
    if DOMAIN not in config:
        return True

    hass.data[DOMAIN] = config[DOMAIN]

    # Start enheden (eller hvad din integration gør)
    LOGGER.info("My_Hood : integration loaded with configuration: %s", config[DOMAIN])

    # Valgfrit: Opret en entitet baseret på YAML-konfiguration
    hass.async_create_task(discovery.async_load_platform(hass, "select", DOMAIN, {}, config))

    return True