from Phidget22.PhidgetException import *
from Phidget22.ErrorCode import *
from Phidget22.Phidget import *
from Phidget22.Net import *
import phidgetConfig

import logging
import traceback

log = logging.getLogger(__name__)

'''f_handler = logging.FileHandler('output.log')
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
log.addHandler(f_handler)'''

_config = None


class NetInfo:
    def __init__(self):
        self.isRemote = None
        self.serverDiscovery = None
        self.hostname = None
        self.port = None
        self.password = None


class ChannelInfo:
    def __init__(self):
        self.serialNumber = -1
        self.hubPort = -1
        self.isHubPortDevice = 0
        self.channel = -1
        self.isVINT = None
        self.isRemote = 0
        self.ipAddress = None


class EndProgramSignal(Exception):
    def __init__(self, value):
        self.value = str(value)


class ConnectServer:
    def __init__(self, device=None, cfg=None):
        if device is not None:
            self.device = device
        else:
            self.device = None
            log.warning(
                "A device label was not passed in as part of the connection logic. No single device can be connected to")

        if cfg is not None:
            self.cfg = self.init_config(cfg)

            self.net_info_obj = NetInfo()
            self.net_info_obj.isRemote = cfg.get_is_remote_host()
            self.net_info_obj.serverDiscovery = cfg.get_network_discovery()
            self.net_info_obj.hostname = cfg.get_ip_address()
            self.net_info_obj.port = cfg.get_host_port()
            self.net_info_obj.password = cfg.get_password()
        else:
            self.cfg = self.init_config()

        if (self.device is not None) and (self.cfg is not None):
            self.channel_info_object = ChannelInfo()
            try:
                config = phidgetConfig.ConfigTool.get_config_struct(None)
                config["deviceList"][device]
            except Exception as err:
                log.error(
                    "The configuration item " + device +
                    " is not found in the config file deviceList. This must be remedied to continue\n")
                raise err
            self.channel_info_object.serialNumber = config["deviceList"][device]["SerialNumber"]
            self.channel_info_object.channel = config["deviceList"][device]["Channel"]
            self.channel_info_object.hubPort = config["deviceList"][device]["VINTPort"]
            self.channel_info_object.isRemote = config["deviceList"][device]["isRemote"]
            self.channel_info_object.ipAddress = config["deviceList"][device]["ipAddress"]

    def connect(self, ch, device):
        ch.deviceName = device
        ch.setDeviceSerialNumber(self.channel_info_object.serialNumber)
        ch.setHubPort(self.channel_info_object.hubPort)
        ch.setIsRemote(self.channel_info_object.isRemote)
        ch.setChannel(self.channel_info_object.channel)
        msg = "Connecting to device " + device
        msg += " having Serial Number of " + str(self.channel_info_object.serialNumber)
        msg += " Channel ID of " + str(self.channel_info_object.channel)
        msg += " and hub port of " + str(self.channel_info_object.hubPort)
        print(msg)
        log.debug(msg)
        try:
            Net.addServer(
                self.cfg.get_device_config(device, "serverName"),
                self.cfg.get_device_config(device, "ipAddress"),
                self.cfg.get_device_config(device, "port"),
                self.cfg.get_device_config(device, "password"),
                0
            )
        except PhidgetException as e:
            if e.details == 'Duplicate':
                print("connection handle already exists, not creating another")
                log.warning("Duplicate Connection to Phidgets Network Server -> Creating TemperatureSensor: " + e.details)
            else:
                raise e

        log.info("Added Server " + self.cfg.get_device_config(device, "password") + " having name of " +
                 self.cfg.get_device_config(device, "serverName") + " with intent to control device " +
                 device + " to the Phidget channel registry")
        ch.openWaitForAttachment(self.cfg.get_timeout_wait_attach())
        return ch

    def init_config(self, cfg=None):
        return phidgetConfig.ConfigTool(cfg)

    def get_config(self, cfg=None):
        return phidgetConfig.ConfigTool(cfg)

    def set_config(self, cfg):
        self.cfg = cfg

    def on_attach_handler(self):
        ph = self
        try:
            # If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            # www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nAttach Event:")
            log.debug("\nAttach Event:")

            """
            * Get device information and display it.
            """
            channelClassName = ph.getChannelClassName()
            serialNumber = ph.getDeviceSerialNumber()
            channel = ph.getChannel()
            if (ph.getDeviceClass() == DeviceClass.PHIDCLASS_VINT):
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
                log.debug("Device Attached!\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
            else:
                print("\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel:  " + str(channel) + "\n")
                log.debug("Device Attached!\n\t-> Channel Class: " + channelClassName + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel:  " + str(channel) + "\n")

            """
                * Set the DataInterval inside of the attach handler to initialize the device with this value.
                * DataInterval defines the minimum time between DeviceChange events.
                * DataInterval can be set to any value from MinDataInterval to MaxDataInterval.
                """
            pollInterval = phidgetConfig.ConfigTool.__config__.get_device_config(ph.deviceName, "PollInterval")
            ph.setDataInterval(pollInterval)
            print("\n\tSetting DataInterval to " + str(pollInterval) + "ms")
            log.debug("Setting DataInterval to " + str(pollInterval) + "ms")

        except PhidgetException as e:
            print("\nError in Attach Event:")
            ConnectServer.DisplayError(e)
            traceback.print_exc()
            return

    def on_detach_handler(self):

        ph = self
        try:
            # If you are unsure how to use more than one Phidget channel with this event, we recommend going to
            # www.phidgets.com/docs/Using_Multiple_Phidgets for information

            print("\nDetach Event:")

            """
            * Get device information and display it.
            """
            serialNumber = ph.getDeviceSerialNumber()
            channelClass = ph.getChannelClassName()
            channel = ph.getChannel()

            deviceClass = ph.getDeviceClass()
            if (deviceClass != DeviceClass.PHIDCLASS_VINT):
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel:  " + str(channel) + "\n")
                log.debug("Device Detached!\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Channel:  " + str(channel) + "\n")
            else:
                hubPort = ph.getHubPort()
                print("\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")
                log.debug("Device Detached!\n\t-> Channel Class: " + channelClass + "\n\t-> Serial Number: " + str(serialNumber) +
                      "\n\t-> Hub Port: " + str(hubPort) + "\n\t-> Channel:  " + str(channel) + "\n")

        except PhidgetException as e:
            print("\nError in Detach Event:")
            log.error("There was an error in a Detach Event")
            ConnectServer.DisplayError(e)
            traceback.print_exc()

    def on_error_handler(self, errorCode, errorString):
        log.error("[Phidget Event Error] --> " + errorString + " (" + str(errorCode) + ")")
        sys.stderr.write("[Phidget Error Event] -> " + errorString + " (" + str(errorCode) + ")\n")

    def send_data_to_ws(self, service_name, json_string):
        cfg = phidgetConfig.ConfigTool.__config__


    def DisplayError(e):
        sys.stderr.write("Desc: " + e.details + "\n")
        log.error("There was an error: " + e.details)

        if (e.code == ErrorCode.EPHIDGET_WRONGDEVICE):
            sys.stderr.write(
                "\tThis error commonly occurs when the Phidget function you are calling does not match the class of the channel that called it.\n"
                "\tFor example, you would get this error if you called a PhidgetVoltageInput_* function with a PhidgetDigitalOutput channel.")
            log.error(
                "\tThis error commonly occurs when the Phidget function you are calling does not match the class of the channel that called it.\n"
                "\tFor example, you would get this error if you called a PhidgetVoltageInput_* function with a PhidgetDigitalOutput channel.")
        elif (e.code == ErrorCode.EPHIDGET_NOTATTACHED):
            sys.stderr.write(
                "\tThis error occurs when you call Phidget functions before a Phidget channel has been opened and attached.\n"
                "\tTo prevent this error, ensure you are calling the function after the Phidget has been opened and the program has verified it is attached.")
            log.error(
                "\tThis error occurs when you call Phidget functions before a Phidget channel has been opened and attached.\n"
                "\tTo prevent this error, ensure you are calling the function after the Phidget has been opened and the program has verified it is attached."
            )
        elif (e.code == ErrorCode.EPHIDGET_NOTCONFIGURED):
            sys.stderr.write(
                "\tThis error code commonly occurs when you call an Enable-type function before all Must-Set Parameters have been set for the channel.\n"
                "\tCheck the API page for your device to see which parameters are labled \"Must be Set\" on the right-hand side of the list.")
            log.error(
                "\tThis error code commonly occurs when you call an Enable-type function before all Must-Set Parameters have been set for the channel.\n"
                "\tCheck the API page for your device to see which parameters are labled \"Must be Set\" on the right-hand side of the list."
            )