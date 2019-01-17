import sys
import datetime
import pystache
import traceback
import logging
import ObjectHotel
import phidgetConfig
from Phidget22.Devices.Stepper import *
from Phidget22.Net import *

from ObjectHotel import ObjectHotel
from PhidgetsBase import ConnectServer
from webClient import WebSender

log = logging.getLogger(__name__)


class StepperControllerHandler(ConnectServer):

    def __init__(self, device_name, config=None):
        super().__init__(device_name, config)

        try:
            ch = Stepper()
            ch.setOnAttachHandler(StepperControllerHandler.onAttachHandler)
            ch.setOnDetachHandler(StepperControllerHandler.onDetachHandler)
            ch.setOnErrorHandler(StepperControllerHandler.onErrorHandler)
            ch.setOnPositionChangeHandler(StepperControllerHandler.onPositionChangeHandler)
            super().connect(ch, device_name)
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Creating StepperController: \n\t")
            log.error("Runtime Error -> Creating StepperController: " + e.details)
            ConnectServer.DisplayError(e)
            raise e
        except RuntimeError as e:
            sys.stderr.write("Runtime Error -> Creating StepperController: \n\t" + e)
            log.error("Runtime Error -> Creating StepperController: " + e.details)
            raise e



    def onAttachHandler(self):

        ph = self
        device_name = ph.__dict__["deviceName"]

        try:
            ConnectServer.on_attach_handler(self)
            log.debug("Setting up stepper attach parameters")
            v_limit = phidgetConfig.ConfigTool.__config__.get_device_config(device_name, "VelocityLimit")
            ph.setVelocityLimit(v_limit)
            accel = phidgetConfig.ConfigTool.__config__.get_device_config(device_name, "Acceleration")
            ph.setAcceleration(accel)
            current_limit = phidgetConfig.ConfigTool.__config__.get_device_config(device_name, "CurrentLimit")
            ph.setCurrentLimit(current_limit)
            rescale_factor = phidgetConfig.ConfigTool.__config__.get_device_config(device_name, "RescaleFactor")
            ph.setRescaleFactor(rescale_factor)



        except PhidgetException as e:
            print("\nError in Attach Event:")
            tb = traceback.format_exc()
            log.error("There was an error in an Attach Event: " + tb)
            ConnectServer.DisplayError(e)
            traceback.print_exc
        except RuntimeError as e:
            print("\nError in Attach Event:")
            tb = traceback.format_exc()
            log.error("There was an error in an Attach Event: " + tb)
            traceback.print_exc
        oh = ObjectHotel()
        oh.checkIn(device_name, ph)
        return

    def onDetachHandler(self):
        ph = self
        ConnectServer.on_detach_handler(ph)
        return

    def onPositionChangeHandler(self, position_deg):
        ph = self
        # conf = phidgetConfig.ConfigTool.get_config_struct(self);

        # If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        # www.phidgets.com/docs/Using_Multiple_Phidgets for information
        device_name = ph.__dict__["deviceName"]
        print("[Position Change Event] -> Position (Degrees/Rotations): " + str(position_deg))
        log.debug("[Position Change Event] -> Position (Degrees/Rotations): " + str(position_deg))
        units = ConnectServer.get_config(None).get_device_config(device_name, "units")
        payload = '{"position": "{{position}}", "timestamp": "{{dateTime}}", "device": "{{device}}"}'
        date_time = datetime.datetime.now().isoformat()
        j_str = pystache.render(payload, {'position': str(position_deg), 'dateTime': date_time, 'device': device_name})

        WebSender(device_name, units, j_str)

    def onErrorHandler(self, errorCode, errorString):
        ph = self
        ConnectServer.on_error_handler(ph, errorCode, errorString)


