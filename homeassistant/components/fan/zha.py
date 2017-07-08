"""
Fan on Zigbee Home Automation networks.

For more details on this platform, please refer to the documentation
at https://home-assistant.io/components/fan.zha/
"""
import asyncio
import logging

from homeassistant.components.fan import (
    DOMAIN, FanEntity, SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH,
    SUPPORT_SET_SPEED)
from homeassistant.components import zha


_LOGGER = logging.getLogger(__name__)

DEPENDENCIES = ['zha']

SPEED_LOWEST = 'lowest'
SPEED_AUTO = 'auto'

SPEED_LIST = [SPEED_OFF, SPEED_AUTO, SPEED_LOWEST ,SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH]

SUPPORTED_FEATURES = SUPPORT_SET_SPEED

# Value will first be divided to an integer
VALUE_TO_SPEED = {
    0: SPEED_OFF,
    1: SPEED_LOW,
    2: SPEED_MEDIUM,
    3: SPEED_HIGH,
}

SPEED_TO_VALUE = {
    SPEED_OFF: 0,
    SPEED_LOW: 1,
    SPEED_MEDIUM: 50,
    SPEED_HIGH: 99,
}

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the Zigbee Home Automation Fan."""
    discovery_info = zha.get_discovery_info(hass, discovery_info)
    if discovery_info is None:
        return

    import bellows.zigbee.zcl.clusters as zcl_clusters
    if zcl_clusters.general.Fan.cluster_id in self._clusters:
        self._supported_features |= fan.SUPPORT_BRIGHTNESS
        self._brightness = 0

    async_add_devices([Fan(**discovery_info)])


class Fan(zha.Entity, FanEntity):
    """Representation of a ZHA or ZLL fan."""

    _domain = DOMAIN
    def __init__(self, **kwargs):
        """Initialize the ZHA Fan."""
        super().__init__(**kwargs)

    def is_on(self) -> bool:
        """Return true if entity is on."""
        if self._state == 'unknown':
            return False
        return bool(self._state)


    def update_properties(self):
        """Handle data changes for node values."""
        value = math.ceil(self.values.primary.data * 3 / 100)
        self._state = VALUE_TO_SPEED[value]

    def set_speed(self, speed):
        """Set the speed of the fan."""
        self.node.set_dimmer(
            self.values.primary.value_id, SPEED_TO_VALUE[speed])

    def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        duration = 5  # tenths of s
        yield from self._endpoint.on_off.on()
        self._state = 0


    @asyncio.coroutine
    def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        yield from self._endpoint.on_off.off()
        self._state = 0

    @property
    def speed(self):
        """Return the current speed."""
        return self._state

    @property
    def speed_list(self):
        """Get the list of available speeds."""
        return SPEED_LIST

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORTED_FEATURES

