import sys
import datetime
import pystache
import traceback

import logging

import phidgetConfig

log = logging.getLogger(__name__)

from Phidget22.Devices.VoltageInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from PhidgetsBase import ConnectServer
from webClient import WebSender

class VoltageInputSensorHandler(ConnectServer):

    def __init__(self, device_name, config=None):
        super().__init__(device_name, config)

        try:
            ch = VoltageInput()
            ch.setOnAttachHandler(VoltageInputSensorHandler.onAttachHandler)
            ch.setOnDetachHandler(VoltageInputSensorHandler.onDetachHandler)
            ch.setOnErrorHandler(VoltageInputSensorHandler.onErrorHandler)
            ch.setOnVoltageChangeHandler(VoltageInputSensorHandler.onVoltageChangeHandler)
            super().connect(ch, device_name)
        except PhidgetException as e:
            sys.stderr.write("Phidgets Error -> Creating VoltageInputSensor: \n\t")
            log.error("Phidgets Error -> Creating VoltageInputSensor: " + e.details)
            ConnectServer.DisplayError(e)
            raise e
        except RuntimeError as e:
            sys.stderr.write("Runtime Error -> Creating VoltageInputSensor: \n\t" + e)
            log.error("Runtime Error -> Creating VoltageInputSensor: " + e.details)
            raise e



    def onAttachHandler(self):

        ph = self

        try:
            ConnectServer.on_attach_handler(self)

            """
            * Set the VoltageInputChangeTrigger inside of the attach handler to initialize the device with this value.
            * VoltageInputChangeTrigger will affect the frequency of VoltageInputChange events, by limiting them to only occur when
            * the humidity changes by at least the value set.
            """
            min_delta = phidgetConfig.ConfigTool.__config__.get_device_config(ph.deviceName, "minimumDelta")
            print("\tSetting VoltageInput ChangeTrigger to " + str(min_delta))
            ph.setVoltageChangeTrigger(min_delta)

        except PhidgetException as e:
            print("\nError in Detach Event:")
            tb = traceback.format_exc()
            log.error("There was an error in a Detach Event: " + tb)
            ConnectServer.DisplayError(e)
            traceback.print_exc
        except RuntimeError as e:
            print("\nError in Detach Event:")
            tb = traceback.format_exc()
            log.error("There was an error in a Detach Event: " + tb)
            traceback.print_exc
        return

    def onDetachHandler(self):
        ph = self
        ConnectServer.on_detach_handler(ph)
        return

    def onVoltageChangeHandler(self, voltage):
        ph = self
        # conf = phidgetConfig.ConfigTool.get_config_struct(self);

        # If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        # www.phidgets.com/docs/Using_Multiple_Phidgets for information

        print("[VoltageInput Event] -> VoltageInput: " + str(voltage))
        log.debug("[VoltageInput Event] -> VoltageInput: " + str(voltage))
        device_name = ph.__dict__["deviceName"]
        payload = '{"voltage": "{{voltage}}", "timestamp": "{{dateTime}}", "device": "{{device}}"}'
        date_time = datetime.datetime.now().isoformat()
        j_str = pystache.render(payload, {'voltage': voltage, 'dateTime': date_time, 'device': device_name})
        units = ConnectServer.get_config(None).get_device_config(device_name, "units")
        log.debug("[VoltageInput Event] -> message sent: " + j_str)
        WebSender(device_name, units, j_str)

    def onErrorHandler(self, errorCode, errorString):
        ph = self
        ConnectServer.on_error_handler(ph, errorCode, errorString)


