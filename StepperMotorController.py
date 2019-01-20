import logging
import time

from Phidget22.PhidgetException import *

import phidgetConfig
from ObjectHotel import ObjectHotel

log = logging.getLogger(__name__)


class StepperController():
    def __init__(self, device_name, config=None):
        log.info("Initializing Stepper Motor Controller for " + device_name)
        self.device_name = device_name
        o_h = ObjectHotel()
        self.controller = o_h.visit(device_name)
        self.stepProfile = None

    def reposition_stepper(self, val, synchronous=False):
        controller = self.controller
        device_name = self.device_name
        try:
            self.engage_if_not_engaged()
            position = controller.getPosition()
            log.debug("Stepper Motor " + device_name + " current position is " + str(position))
            controller.setTargetPosition(val)
        except PhidgetException as e:
            log.error("There was an error repositioning stepper " + device_name, exc_info=True)
            raise e
        except Exception as e:
            log.error("There was an unexpected error repositioning stepper " + device_name, exc_info=True)
            raise e
        if synchronous:
            self.wait_for_stepper_to_stop()
        return

    def engage_if_not_engaged(self):
        ctrlr = self.controller
        engaged = ctrlr.getEngaged()
        if engaged == 0 or engaged is False:
            ctrlr.setEngaged(True)
            log.warning("Engaging the stepper motor for device " + self.device_name)

    def normalize_stepper(self):
        self.set_stepper_profile("default")
        return

    def set_stepper_profile(self, profile):
        ctrlr = self.controller
        self.stepProfile = profile
        cfg = phidgetConfig.ConfigTool(None)
        stepper_settings = cfg.get_stepper_profile(self.device_name, profile)
        self._apply_stepper_profile(stepper_settings)
        return

    def _apply_stepper_profile(self, profileData):
        ctrlr = self.controller
        cfg = phidgetConfig.ConfigTool(None)
        try:
            ctrlr.setRescaleFactor(cfg.get_base_rescale_factor())
            max_velocity = self.get_max_velocity()
            max_acceleration = self.get_max_acceleration()
            print("maxAcceleration = " + str(max_acceleration) + " and maxVelocity = " + str(max_velocity))
            # v_limit = max_velocity * profileData["VelocityLimit"] / 100  # VelocityLimit is in percent of max_velocity
            # acc_limit = max_acceleration * profileData["Acceleration"] / 100  # Acceleration is a percent of max_acceleration
            v_limit = profileData["VelocityLimit"]
            acc_limit = profileData["Acceleration"]
            rescale_factor = cfg.get_device_config(self.device_name, "RescaleFactor")
            log_msg = "Setting limits for stepper " + self.device_name + " according to profile "
            log_msg += self.stepProfile + " with a max acceleration percent of " + str(profileData["Acceleration"])
            log_msg += ", a max velocity percent of " + str(profileData["VelocityLimit"])
            log_msg += ", and a max current of " + str(profileData["CurrentLimit"]) + " amps"
            log.debug(log_msg)
            ctrlr.setVelocityLimit(v_limit)
            ctrlr.setAcceleration(acc_limit)
            ctrlr.setCurrentLimit(profileData["CurrentLimit"])
            ctrlr.setRescaleFactor(rescale_factor)
        except PhidgetException as e:
            log.error("There was an error repositioning stepper " + self.device_name, exc_info=True)
            raise e
        except Exception as e:
            log.error("There was an error repositioning stepper " + self.device_name, exc_info=True)
            raise e
        return

    def wait_for_stepper_to_stop(self):
        ctrlr = self.controller
        while self.get_is_moving() == 1:
            time.sleep(1)
        return

    def get_position(self):
        ctrlr = self.controller
        return ctrlr.getPosition()

    def get_is_moving(self):
        ctrlr = self.controller
        return ctrlr.getIsMoving()

    def get_max_velocity(self):
        ctrlr = self.controller
        return ctrlr.getMaxVelocityLimit()

    def get_max_acceleration(self):
        ctrlr = self.controller
        return ctrlr.getMaxAcceleration()