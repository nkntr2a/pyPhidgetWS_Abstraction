import http.client
import phidgetConfig
import PhidgetsBase
import json
import pystache
import datetime

import logging
log = logging.getLogger(__name__)


class WebSender:
    def __init__(self, device, measurement, json_string):
        self.cfg = phidgetConfig.ConfigTool()
        web_cfg = self.cfg.get_web_client_template(device)
        connection = http.client.HTTPConnection(web_cfg["hostName"])
        header_string = web_cfg["headers"]
        conn_type = web_cfg["type"]
        service_path = '/' + self.cfg.get_config_struct()["webClient"]["serviceName"][device][measurement]["servicePath"]
        log.debug('Web Client [Humidity] sending info: ' + header_string + ' | ' + conn_type + ' | ' + service_path + ' | ' + json_string)
        headers = json.loads(header_string)
        connection.request(conn_type, service_path, json_string, headers)
        response = connection.getresponse()
        log.debug('Web Client [humidity] sender response: ' + str(response.__dict__))
        print('response = ', response)
