import logging
import traceback

from ObjectHotel import ObjectHotel

log = logging.getLogger(__name__)

from Phidget22.Devices.DigitalOutput import *
from Phidget22.Net import *
from PhidgetsBase import ConnectServer


class DigitalOutputHandler(ConnectServer):

    def __init__(self, device_name, config=None):
        super().__init__(device_name, config)

        try:
            ch = DigitalOutput()
            ch.setOnAttachHandler(DigitalOutputHandler.onAttachHandler)
            ch.setOnDetachHandler(DigitalOutputHandler.onDetachHandler)
            ch.setOnErrorHandler(DigitalOutputHandler.onErrorHandler)
            super().connect(ch, device_name)
        except PhidgetException as e:
            sys.stderr.write("Phidgets Error -> Creating Digital Output Controller: \n\t")
            log.error("Phidgets Error -> Creating Digital Output Controller: " + e.details)
            ConnectServer.DisplayError(e)
            raise e
        except RuntimeError as e:
            sys.stderr.write("Runtime Error -> Creating Digital Output Controller: \n\t" + e)
            log.error("Runtime Error -> Creating Digital Output Controller: " + e.details)
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

    def onErrorHandler(self, errorCode, errorString):
        ph = self
        ConnectServer.on_error_handler(ph, errorCode, errorString)


