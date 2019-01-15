import sys
import datetime
import pystache
import traceback

import logging

import phidgetConfig

log = logging.getLogger(__name__)

from Phidget22.Devices.HumiditySensor import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from PhidgetsBase import ConnectServer
from webClient import WebSender

class HumiditySensorHandler(ConnectServer):

    def __init__(self, device_name, config=None):
        super().__init__(device_name, config)

        try:
            ch = HumiditySensor()
            ch.setOnAttachHandler(HumiditySensorHandler.onAttachHandler)
            ch.setOnDetachHandler(HumiditySensorHandler.onDetachHandler)
            ch.setOnErrorHandler(HumiditySensorHandler.onErrorHandler)
            ch.setOnHumidityChangeHandler(HumiditySensorHandler.onHumidityChangeHandler)
            super().connect(ch, device_name)
        except PhidgetException as e:
            sys.stderr.write("Runtime Error -> Creating HumiditySensor: \n\t")
            log.error("Runtime Error -> Creating HumiditySensor: " + e.details)
            ConnectServer.DisplayError(e)
            raise e
        except RuntimeError as e:
            sys.stderr.write("Runtime Error -> Creating HumiditySensor: \n\t" + e)
            log.error("Runtime Error -> Creating HumiditySensor: " + e.details)
            raise e



    def onAttachHandler(self):

        ph = self

        try:
            ConnectServer.on_attach_handler(self)

            """
            * Set the HumidityChangeTrigger inside of the attach handler to initialize the device with this value.
            * HumidityChangeTrigger will affect the frequency of HumidityChange events, by limiting them to only occur when
            * the humidity changes by at least the value set.
            """
            min_delta = phidgetConfig.ConfigTool.__config__.get_device_config(ph.deviceName, "minimumDelta")
            print("\tSetting Humidity ChangeTrigger to " + str(min_delta))
            ph.setHumidityChangeTrigger(min_delta)

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

    def onHumidityChangeHandler(self, humidity):
        ph = self
        # conf = phidgetConfig.ConfigTool.get_config_struct(self);

        # If you are unsure how to use more than one Phidget channel with this event, we recommend going to
        # www.phidgets.com/docs/Using_Multiple_Phidgets for information
        device_name = ph.__dict__["deviceName"]
        print("[Humidity Event] -> Humidity: " + str(humidity))
        log.debug("[Humidity Event] -> Humidity: " + str(humidity))
        units = ConnectServer.get_config(None).get_device_config(device_name, "units")
        payload = '{"humidity": "{{humidity}}", "timestamp": "{{dateTime}}", "device": "{{device}}"}'
        date_time = datetime.datetime.now().isoformat()
        jStr = pystache.render(payload, {'humidity': humidity, 'dateTime': date_time, 'device': device_name})

        WebSender(device_name, units, jStr)

    def onErrorHandler(self, errorCode, errorString):
        ph = self
        ConnectServer.on_error_handler(ph, errorCode, errorString)


