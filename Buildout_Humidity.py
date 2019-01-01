import sys
import datetime
import pystache
import traceback

import logging
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
            print("\tSetting Humidity ChangeTrigger to 0.0")
            ph.setHumidityChangeTrigger(0.0)

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

        print("[Humidity Event] -> Humidity: " + str(humidity))
        log.debug("[Humidity Event] -> Humidity: " + str(humidity))

        payload = '{"humidity": "{{humidity}}", "timestamp": "{{dateTime}}", "device": "{{device}}"}'
        dateTime = datetime.datetime.now().isoformat()
        jStr = pystache.render(payload, {'humidity': humidity, 'dateTime': dateTime, 'device': 'HumiditySensor'})

        WebSender("HumiditySensor", "reportHumidity", jStr)

    def onErrorHandler(self, errorCode, errorString):
        ph = self
        ConnectServer.on_error_handler(ph, errorCode, errorString)


