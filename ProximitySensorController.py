import logging
import time

from Phidget22.PhidgetException import *

import phidgetConfig
from ObjectHotel import ObjectHotel

log = logging.getLogger(__name__)


class ProximitySensor:
    def __init__(self, device_name, config=None):
        log.info("Initializing Proximity Sensor for " + device_name)
        self.device_name = device_name
        o_h = ObjectHotel()
        self.controller = o_h.visit(device_name)

    def get_current_state(self):
        try:
            current_state = self.controller.getState()
        except PhidgetException as e
            log.error("Unable to get the current state from " + device_name, exc_info=True)
            raise e
        except RuntimeError as e
            log.error("For unknown reason, unable to get the current state from " + device_name, exc_info=True)
            raise e
        return current_state

    def get_last_trigger(self):
        cfg = phidgetConfig.ConfigTool()
        o_h = ObjectHotel()
        last_state_handler = o_h.visit(cfg.get_device_config(self.device_name, ProximityEventTracker))
        time_stamp_last_trigger = last_state_handler.get_last_true()
        return time_stamp_last_trigger