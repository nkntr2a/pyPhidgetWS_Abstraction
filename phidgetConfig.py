import json
import logging
import copy
log = logging.getLogger(__name__)

'''f_handler = logging.FileHandler('output.log')
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
log.addHandler(f_handler)'''


class ConfigTool:

    __config__ = None

    def __init__(self, file_name=None):
        if ConfigTool.__config__ is None:
            __configDict = None
            if file_name is None:
                file_name = "./phidgetConfig.json"

            with open(file_name, 'r') as f:
                try:
                    config_dict = json.load(f)
                except Exception as err:
                    log.error("Could not load config file: ", file_name)
                    log.error("Error was: ", err)
                    raise err
                try:
                    assert type(config_dict) is dict
                except Exception as err:
                    log.error("Config file should have returned a dictionary of configuration key value pairs. It did not")
                    log.error("Config Object returned was: ", config_dict)
                    raise err

                self.set_config_tool(config_dict)
        else:
            newObj = copy.deepcopy(ConfigTool.__config__)
            self.__dict__.update(newObj.__dict__)
        log.debug("Config instance prepared")

    def get_config_tool(self):
        if ConfigTool.__config__ is None:
            self = ConfigTool.__init__()
        return self

    def get_config_struct(self):
        if ConfigTool.__config__ is None:
            self = ConfigTool.__init__()
        else:
            self = ConfigTool.__config__
        return self.__configDict

    def set_config_tool(self, val):
        self.__configDict = val
        ConfigTool.__config__ = self

    def get_network_discovery(self):
        return self.__configDict["NetworkDiscovery"]

    def get_is_sbc(self):
        return self.__configDict["isSBC"]

    def get_ip_address(self):
        return self.__configDict["ipAddress"]

    def get_password(self):
        return self.__configDict["passwd"]

    def get_use_www_connect(self):
        return self.__configDict["useWWWConnect"]

    def get_is_remote_host(self):
        return self.__configDict["isRemoteHost"]

    def get_host_port(self):
        return self.__configDict["port"]

    def get_timeout_wait_attach(self):
        return self.__configDict["timeoutWaitingForAttach"]

    def get_base_rescale_factor(self):
        return self.__configDict["baseRescaleFactor"]

    def get_device_config(self, device, key):
        returnable = self.__configDict["deviceList"][device][key]
        if key == 'password' and self.__configDict["deviceList"][device][key] is None:
            returnable = ""
        return returnable

    def get_stepper_profile(self, device, profile):
        return self.__configDict["StepperProfiles"]["Device"][device][profile]

    def get_web_client_template(self, device):
        return self.__configDict['webClient'][self.__configDict["deviceList"][device]["webClientTemplate"]]

    def get_opposite_linear_motor_relay(self, device):
        return self.__configDict["deviceList"][device]["oppositeHandler"]

def main():
    cfg = ConfigTool('./phidgetConfig.json')
    print("Config is: ", cfg.get_config_tool())
    print("IP Address is: ", cfg.get_use_www_connect())


main()