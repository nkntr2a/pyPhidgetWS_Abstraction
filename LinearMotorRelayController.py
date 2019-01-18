import EventDriven_DigitalOutput
import logging
from Phidget22 import PhidgetException

import phidgetConfig
from ObjectHotel import ObjectHotel

log = logging.getLogger(__name__)


class LinearMotorActuator():

    def __init__(self, device_name, config=None):
        log.info("Initializing Linear Motor for " + device_name)
        self.device_name = device_name

    def actuate_lm(self, state):
        device_name = self.device_name
        o_h = ObjectHotel()
        cfg = phidgetConfig.ConfigTool(None)
        controller = o_h.visit(device_name)
        opposite_controller = cfg.get_opposite_linear_motor_relay(device_name)
        opposite_controller_handler = o_h.visit(opposite_controller)
        opposite_controller_relay_state = opposite_controller_handler.getState()

        try:
            assert opposite_controller_relay_state == 0
        except AssertionError:
            log.error(
                "Cannot engage relay on a linear motor if the opposite relay" +
                "engaging the reversing actino is also set to true")
            raise IllegalLinearMotorOperation(device_name)

        current_state = controller.getState()
        if current_state == state:
            stateText = "On" if current_state else "Off"
            log.warning(device_name + " is already " + stateText)
        else:
            try:
                controller.setState(state)
            except PhidgetException as e:
                log.error("Cannot toggle relay for device " + device_name, exc_info=True)
        return

    def get_state(self):
        device_name = self.device_name
        o_h = ObjectHotel()
        controller = o_h.visit(device_name)
        return controller.getState()

    def getVoltageChangeTrigger(self):
        o_h = ObjectHotel()
        cfg = phidgetConfig.ConfigTool(None)
        device_name = cfg.get_device_config(self.device_name, "positionHandler")
        controller = o_h.visit(device_name)
        return controller.getVoltageChangeTrigger

    def setVoltageChangeTrigger(self, val):
        o_h = ObjectHotel()
        cfg = phidgetConfig.ConfigTool(None)
        device_name = cfg.get_device_config(self.device_name, "positionHandler")
        controller = o_h.visit(device_name)
        controller.setVoltageChangeTrigger(val)

class IllegalLinearMotorOperation(Exception):
    def __init__(self, dErrorArguments):
        Exception.__init__(self, "Cannot simultaneously extend and retract linear motor {}".format(dErrorArguments))
        self.dErrorArguments = dErrorArguments
