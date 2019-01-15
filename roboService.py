from flask import Flask, json
import EventDriven_Humidity
import time

import logging

import EventDriven_Stepper
import EventDriven_Temperature
import EventDriven_VoltageInput
import phidgetConfig

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


@app.route('/config')
def w_config():
    config = phidgetConfig.ConfigTool.get_config_struct(None)
    j_config = json.dumps(config);
    return j_config


if __name__ == '__main__':
    logging.debug("Application Started")
    # humidityObj = Buildout_Humidity.StepperControllerHandler("HumiditySensor")
    # time.sleep(1)
    # temperatureObj = Buildout_Temperature.TemperatureSensorHandler("TemperatureSensor")
    # time.sleep(1)
    # extenderObj = Buildout_VoltageInput.VoltageInputSensorHandler("ArmExtenderWiper")
    # time.sleep(1)
    grabberObj = EventDriven_VoltageInput.VoltageInputSensorHandler("GrabberWiper")
    # time.sleep(1)
    # armUpDownObj = EventDriven_Stepper.StepperControllerHandler("ArmUpDownStepper")


    app.run(debug=True)
