import sys
import datetime
import pystache
import traceback

import logging

from ObjectHotel import ObjectHotel

log = logging.getLogger(__name__)

from Phidget22.Devices.DigitalInput import *
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Net import *
from PhidgetsBase import ConnectServer
from webClient import WebSender
import phidgetConfig


class DigitalInputHandler(ConnectServer):

    def __init__(self, device_name, config=None):
        super().__init__(device_name, config)

        try:
            ch = DigitalInput()
            ch.setOnAttachHandler(DigitalInputHandler.onAttachHandler)
            ch.setOnDetachHandler(DigitalInputHandler.onDetachHandler)
            ch.setOnErrorHandler(DigitalInputHandler.onErrorHandler)
            ch.setOnStateChangeHandler(DigitalInputHandler.onStateChangeHandler)
            super().connect(ch, device_name)
        except PhidgetException as e:
            sys.stderr.write("Phidgets Error -> Creating State Change Sensor: \n\t")
            log.error("Phidgets Error -> Creating State Change Sensor: " + e.details)
            ConnectServer.DisplayError(e)
            raise e
        except RuntimeError as e:
            sys.stderr.write("Runtime Error -> Creating State Change Sensor: \n\t" + e)
            log.error("Runtime Error -> Creating State Change Sensor: " + e.details)
            raise e

    def onAttachHandler(self):

        ph = self

        try:
            ConnectServer.on_attach_handler(self)

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
        oh = ObjectHotel()
        oh.checkIn(ph.__dict__["deviceName"], ph)
        return

    def onDetachHandler(self):
        ph = self
        ConnectServer.on_detach_handler(ph)
        return

    def onStateChangeHandler(self, current_state):
        ph = self
        device_name = ph.__dict__["deviceName"]
        print("[State Change Event] -> State Change: " + str(current_state))
        log.debug("[State Change Event] -> State Change: " + str(current_state))
        units = ConnectServer.get_config(None).get_device_config(device_name, "units")
        payload = '{"currentState": "{{state}}", "timestamp": "{{dateTime}}", "device": "{{device}}"}'
        dateTime = datetime.datetime.now().isoformat()
        jStr = pystache.render(payload, {'state': current_state, 'dateTime': dateTime, 'device': device_name})
        log.debug("[State Change Event] -> message sent: " + jStr)
        WebSender(device_name, units, jStr)

    def onErrorHandler(self, errorCode, errorString):
        ph = self
        ConnectServer.on_error_handler(ph, errorCode, errorString)


