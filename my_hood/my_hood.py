import asyncio
import logging
from bleak import BleakClient

LOGGER = logging.getLogger(__name__)

# Define the UUID for the characteristic to write to
CHARACTERISTIC_UUID = "a0e40002-daa1-4a1f-8adc-78f736d2d474"  # Change as per your device spec
# Command to be sent (hex data)
DEVICE_INFO = bytes.fromhex("00220c02")


class MyHoodInstance:
        def __init__(self, device_address):
                LOGGER.info("My_Hood : Initialize with a BLE device address: %s", device_address)
                self.device_address = device_address

        async def is_connected(self, client):
                return client.is_connected

        async def send_command(self, command: bytearray):
                async with BleakClient(self.device_address) as client:
                        try:
                                result = await asyncio.wait_for(self.is_connected(client), timeout=20)
                                if result:
                                        LOGGER.debug("My_Hood : Connected to %s", self.device_address)
                                        await client.write_gatt_char(CHARACTERISTIC_UUID, DEVICE_INFO + command, response=True)
                                        LOGGER.info("My_Hood : Command sent successfully")
                        except asyncio.TimeoutError:
                                LOGGER.error("My_Hood : Connection check timed out")

        async def set_hood_suction(self, value):
                LOGGER.error("My_Hood : set_hood_suction - %s", value)
                await self.send_command(bytes.fromhex("070" + value + "0000"))

        async def turn_on(self):
                await self.send_command(bytes.fromhex("09640000"))

        async def turn_off(self):
                await self.send_command(bytes.fromhex("09000000"))
