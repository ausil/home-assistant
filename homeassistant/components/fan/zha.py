"""
Fans on Zigbee Home Automation networks.

For more details on this platform, please refer to the documentation
at https://home-assistant.io/components/fan.zha/
"""
import asyncio
import logging

from homeassistant.components.fan import DOMAIN, FanEntity, SPEED_OFF, 
    SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH, SUPPORT_SET_SPEED)

from homeassistant.components import zha

_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['zha']

SPEED_LIST = [SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up Zigbee Home Automation fans."""
    discovery_info = zha.get_discovery_info(hass, discovery_info)
    if discovery_info is None:
        return

    add_devices([Fan(**discovery_info)])


class Fan(zha.Entity, FanEntity):
    """ZHA fan."""

    _domain = DOMAIN

    @property
    def is_on(self) -> bool:
        """Return if the fan is on based on the statemachine."""
        if self._state == 'unknown':
            return False
        return bool(self._state)

    @asyncio.coroutine
    def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        yield from self._endpoint.on_off.on()
        self._state = 1

    @asyncio.coroutine
    def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        yield from self._endpoint.on_off.off()
        self._state = 0

    @asyncio.coroutine
    def async_set_speed(self, speed: str) -> None:


    @property
    def speed_list(self):
        """Get the list of available speeds."""
        return SPEED_LIST

