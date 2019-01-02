from flask import Flask, jsonify
import Buildout_Humidity
import time

import logging

import Buildout_Temperature
import Buildout_VoltageInput

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt = '%m/%d/%Y %I:%M:%S %p',
                    filename = 'output.log',
                    level=logging.DEBUG)

'''log = logging.getLogger(__name__)

f_handler = logging.FileHandler('./output.log')
f_handler.setLevel(logging.DEBUG)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
log.addHandler(f_handler)
'''

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World!"


if __name__ == '__main__':
    logging.debug("Application Started")
    humidityObj = Buildout_Humidity.HumiditySensorHandler("HumiditySensor")
    time.sleep(10)
    temperatureObj = Buildout_Temperature.TemperatureSensorHandler("TemperatureSensor")
    time.sleep(10)
    extenderObj = Buildout_VoltageInput.VoltageInputSensorHandler("ArmExtenderWiper")
    time.sleep(10)
    grabberObj = Buildout_VoltageInput.VoltageInputSensorHandler("GrabberWiper")
    time.sleep(300)

    #app.run(debug=True)
