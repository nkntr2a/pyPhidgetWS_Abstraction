import logging
import time

from Phidget22.PhidgetException import *

import phidgetConfig
from ObjectHotel import ObjectHotel

log = logging.getLogger(__name__)


class LinearMotorActuator():

    def __init__(self, device_name, config=None):
        log.info("Initializing Linear Motor for " + device_name)
        self.device_name = device_name
        o_h = ObjectHotel()
        self.controller = o_h.visit(device_name)

    def move_to_position(self, position):
        device_name = self.device_name
        o_h = ObjectHotel()
        cfg = phidgetConfig.ConfigTool(None)
        voltage_monitor_device_name = cfg.get_device_config(device_name, "positionHandler")
        vm_device = o_h.visit(voltage_monitor_device_name)
        volts = vm_device.getVoltage()
        print("Volts read = " + str(volts))

        if cfg.get_device_config(device_name, "voltsDirection") == "rise":
            last_volts = -1
            if position > volts:
                try:
                    self.setPollInterval(180)
                    self.setVoltageChangeTrigger(0.001)
                    self.actuate_lm(1)
                except PhidgetException as e:
                    log.error("There was an error actuating linear motor " + device_name, exc_info=True)
                    raise e
                except Exception as e:
                    log.error("There was an unexpected error actuating linear motor " + device_name, exc_info=True)
                    raise e
                while position > volts and last_volts < volts:
                    time.sleep(.3)
                    last_volts = volts
                    volts = vm_device.getVoltage()
                    print("Current Volts: " + str(volts) + ", previous volts: " + str(last_volts) + ", position: " + str(position))
                    gripperHoldObj = o_h.visit("HoldGripper")
                    print("Gripper Hold Object: " + str(gripperHoldObj.get_hold_state()))
                while gripperHoldObj.get_hold_state():
                    self.actuate_lm(0)
                    time.sleep(cfg.get_device_config(device_name, "GripperReleaseCycleTime"))
                    self.actuate_lm(1)
                    time.sleep(cfg.get_device_config(device_name, "GripperHoldCycleTime"))
                    gripperHoldObj = o_h.visit("HoldGripper")
                    print("Gripper Hold Object: " + str(gripperHoldObj.get_hold_state()))
        elif cfg.get_device_config(device_name, "voltsDirection") == "fall":
            last_volts = 1000
            if position < volts:
                try:
                    self.setPollInterval(180)
                    self.setVoltageChangeTrigger(0.001)
                    self.actuate_lm(1)
                except PhidgetException as e:
                    log.error("There was an error actuating linear motor " + device_name, exc_info=True)
                    raise e
                except Exception as e:
                    log.error("There was an unexpected error actuating linear motor " + device_name, exc_info=True)
                    raise e
                while position < volts and last_volts > volts:
                    time.sleep(.3)
                    last_volts = volts
                    volts = vm_device.getVoltage()
                    print("Current Volts: " + str(volts) + ", previous volts: " + str(last_volts) + ", position: " + str(position))
                    gripperHoldObj = o_h.visit("HoldGripper")
                    print("Gripper Hold Object: " + str(gripperHoldObj.get_hold_state()))
                while gripperHoldObj.get_hold_state():
                    self.actuate_lm(0)
                    time.sleep(cfg.get_device_config(device_name, "GripperReleaseCycleTime"))
                    self.actuate_lm(1)
                    time.sleep(cfg.get_device_config(device_name, "GripperHoldCycleTime"))
                    gripperHoldObj = o_h.visit("HoldGripper")
                    print("Gripper Hold Object: " + str(gripperHoldObj.get_hold_state()))
        else:
            log.error("Cannot move linear motor to a position voltsDirection being set in the config for device " + device_name)
            raise RuntimeError

        self.setVoltageChangeTrigger(0.1)
        self.setPollInterval(1000)
        self.actuate_lm(0)
        volts = vm_device.getVoltage()
        print("Volts read = " + str(volts))
        return volts

    def actuate_lm(self, state):
        device_name = self.device_name
        cfg = phidgetConfig.ConfigTool(None)
        controller = self.controller
        o_h = ObjectHotel()
        opposite_controller = cfg.get_opposite_linear_motor_relay(device_name)
        opposite_controller_handler = o_h.visit(opposite_controller)
        opposite_controller_relay_state = opposite_controller_handler.getState()

        try:
            assert state == 0 or opposite_controller_relay_state == 0
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
        controller = self.controller
        return controller.getState()

    def getVoltageChangeTrigger(self):
        o_h = ObjectHotel()
        cfg = phidgetConfig.ConfigTool(None)
        device_name = cfg.get_device_config(self.device_name, "positionHandler")
        controller = o_h.visit(device_name)
        return controller.getVoltageChangeTrigger()

    def setVoltageChangeTrigger(self, val):
        o_h = ObjectHotel()
        cfg = phidgetConfig.ConfigTool(None)
        device_name = cfg.get_device_config(self.device_name, "positionHandler")
        controller = o_h.visit(device_name)
        controller.setVoltageChangeTrigger(val)

    def getPollInterval(self):
        o_h = ObjectHotel()
        cfg = phidgetConfig.ConfigTool(None)
        device_name = cfg.get_device_config(self.device_name, "positionHandler")
        controller = o_h.visit(device_name)
        return controller.getDataInterval()

    def setPollInterval(self, val):
        o_h = ObjectHotel()
        cfg = phidgetConfig.ConfigTool(None)
        device_name = cfg.get_device_config(self.device_name, "positionHandler")
        controller = o_h.visit(device_name)
        controller.setDataInterval(val)


class IllegalLinearMotorOperation(Exception):
    def __init__(self, dErrorArguments):
        Exception.__init__(self, "Cannot simultaneously extend and retract linear motor {}".format(dErrorArguments))
        self.dErrorArguments = dErrorArguments
