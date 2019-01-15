import sys
import datetime
import pystache
import traceback

import logging
log = logging.getLogger(__name__)

from Phidget22.Devices.TemperatureSensor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from PhidgetsBase import ConnectServer
from webClient import WebSender
import phidgetConfig


class TemperatureSensorHandler(ConnectServer):

    def __init__(self, device_name, config=None):
        super().__init__(device_name, config)

        try:
            ch = TemperatureSensor()
            ch.setOnAttachHandler(TemperatureSensorHandler.onAttachHandler)
            ch.setOnDetachHandler(TemperatureSensorHandler.onDetachHandler)
            ch.setOnErrorHandler(TemperatureSensorHandler.onErrorHandler)
            ch.setOnTemperatureChangeHandler(TemperatureSensorHandler.onTemperatureChangeHandler)
            super().connect(ch, device_name)
        except PhidgetException as e:
            sys.stderr.write("Phidgets Error -> Creating TemperatureSensor: \n\t")
            log.error("Phidgets Error -> Creating TemperatureSensor: " + e.details)
            ConnectServer.DisplayError(e)
            raise e
        except RuntimeError as e:
            sys.stderr.write("Runtime Error -> Creating TemperatureSensor: \n\t" + e)
            log.error("Runtime Error -> Creating TemperatureSensor: " + e.details)
            raise e

    def onAttachHandler(self):

        ph = self

        try:
            ConnectServer.on_attach_handler(self)

            """
            * Set the TemperatureChangeTrigger inside of the attach handler to initialize the device with this value.
            * TemperatureChangeTrigger will affect the frequency of TemperatureChange events, by limiting them to only occur when
            * the humidity changes by at least the value set.
            """
            min_delta = phidgetConfig.ConfigTool.__config__.get_device_config(ph.deviceName, "minimumDelta")
            print("\tSetting Temperature ChangeTrigger to " + str(min_delta))
            ph.setTemperatureChangeTrigger(min_delta)

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

    def onTemperatureChangeHandler(self, temperature):
        ph = self
        # conf = phidgetConfig.ConfigTool.get_config_struct(self);

        # If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        # www.phidgets.com/docs/Using_Multiple_Phidgets for information

        device_name = ph.__dict__["deviceName"]
        print("[Temperature Event] -> Temperature: " + str(temperature))
        log.debug("[Temperature Event] -> Temperature: " + str(temperature))
        units = ConnectServer.get_config(None).get_device_config(device_name, "units")
        payload = '{"temperature": "{{temperature}}", "timestamp": "{{dateTime}}", "device": "{{device}}"}'
        dateTime = datetime.datetime.now().isoformat()
        jStr = pystache.render(payload, {'temperature': temperature, 'dateTime': dateTime, 'device': device_name})
        log.debug("[Temperature Event] -> message sent: " + jStr)
        WebSender(device_name, units, jStr)

    def onErrorHandler(self, errorCode, errorString):
        ph = self
        ConnectServer.on_error_handler(ph, errorCode, errorString)


