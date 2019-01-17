from flask import Flask, json
import EventDriven_Humidity
import time
import ObjectHotel
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
    j_config = json.dumps(config)
    return j_config


@app.before_first_request
def do_something_only_once():
    print("Doing The Thing")
    logging.debug("Application Started")
    o_h = ObjectHotel.ObjectHotel()
    humidity_obj = EventDriven_Humidity.HumiditySensorHandler("HumiditySensor")
    o_h.checkIn("HumiditySensorObj", humidity_obj)
    temperature_obj = EventDriven_Temperature.TemperatureSensorHandler("TemperatureSensor")
    o_h.checkIn("TemperatureSensorObj", temperature_obj)
    extender_obj = EventDriven_VoltageInput.VoltageInputSensorHandler("ArmExtenderWiper")
    o_h.checkIn("ArmExtenderWiperObj", extender_obj)
    grabber_obj = EventDriven_VoltageInput.VoltageInputSensorHandler("GrabberWiper")
    o_h.checkIn("GrabberWiperObj", grabber_obj)
    arm_up_down_obj = EventDriven_Stepper.StepperControllerHandler("ArmUpDownStepper")
    o_h.checkIn("ArmUpDownStepperObj", arm_up_down_obj)
    spin_arm_obj = EventDriven_Stepper.StepperControllerHandler("SpinArm")
    o_h.checkIn("SpinArmObj", spin_arm_obj)
    locomotion_obj = EventDriven_Stepper.StepperControllerHandler("Locomotion")
    o_h.checkIn("LocomotionObj", locomotion_obj)
    ud_stepper = o_h.visit("Locomotion")
    pos = ud_stepper.getPosition()
    time.sleep(5)
    ud_stepper.setEngaged(True)
    ud_stepper.setTargetPosition(-2)
    time.sleep(12)
    ud_stepper.setTargetPosition(2)
    time.sleep(20)
    ud_stepper.setTargetPosition(0)

    print(pos)
    print("First Position")
    time.sleep(10)
    pos = ud_stepper.getPosition()
    print("Second Position: " + str(pos))
    ud_stepper.setEngaged(False)


if __name__ == '__main__':
    app.run(debug=True)
