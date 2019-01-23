import time

from flask import Flask, request, json, jsonify

import EventDriven_DigitalInput
import EventDriven_Humidity
from Phidget22 import PhidgetException

import LastFiveTriggers
import ObjectHotel
import logging

import EventDriven_Stepper
import EventDriven_Temperature
import EventDriven_VoltageInput
import StepperMotorController
import phidgetConfig
import EventDriven_DigitalOutput
import LinearMotorRelayController
from HoldGripper import HoldGripper

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


@app.route('/moveStepper', methods=['POST'])
def stepper_move():
    content = request.json
    print(str(content))
    stepper_motor_controller = StepperMotorController.StepperController(content["device"])
    stepper_motor_controller.set_stepper_profile(content["profile"])
    stepper_motor_controller.reposition_stepper(content["position"], content["waitForMove"])
    return jsonify({"commandSent": True})


@app.route('/getStepperPosition', methods=['POST'])
def get_stepper_position():
    content = request.json
    stepper_motor_controller = StepperMotorController.StepperController(content["device"])
    pos = stepper_motor_controller.get_position()
    return jsonify({"commandSent": True, "device_name": content["device"], "position": pos})


@app.route('/updateStepperPosition', methods=['POST'])
def update_stepper_position():
    content = request.json
    stepper_motor_controller = StepperMotorController.StepperController(content["device"])
    position = content["position"]
    stepper_motor_controller.addPositionOffset(position)
    pos = stepper_motor_controller.get_position()
    return jsonify({"commandSent": True, "device_name": content["device"], "position": pos})


@app.route('/moveLinearMotor', methods=['POST'])
def lm_move():
    content = request.json
    print(str(content))
    linear_motor_controller = LinearMotorRelayController.LinearMotorActuator(content["device"])
    volts = linear_motor_controller.move_to_position(content["position"])
    return jsonify({"endingVolts": volts, "commandSent": True})


@app.route('/holdGripper', methods=['POST'])
def hold_gripper():
    content=request.json
    o_h = ObjectHotel.ObjectHotel()
    gripper_hold_obj = o_h.visit("HoldGripper")
    gripper_hold_obj.set_hold_state(content["holdGripper"])
    return jsonify({"holdState": gripper_hold_obj.get_hold_state()})


@app.before_first_request
def do_something_only_once():
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
    arm_in_obj = EventDriven_DigitalOutput.DigitalOutputHandler("ArmIn")
    o_h.checkIn("ArmInObj", arm_in_obj)
    arm_out_obj = EventDriven_DigitalOutput.DigitalOutputHandler("ArmOut")
    o_h.checkIn("ArmOutObj", arm_out_obj)
    gripper_close_obj = EventDriven_DigitalOutput.DigitalOutputHandler("CloseGripper")
    o_h.checkIn("CloseGripperObj", gripper_close_obj)
    gripper_open_obj = EventDriven_DigitalOutput.DigitalOutputHandler("OpenGripper")
    o_h.checkIn("OpenGripperObj", gripper_open_obj)
    hg = HoldGripper()
    o_h.checkIn("HoldGripper", hg)
    are = LastFiveTriggers.LastFiveEvents()
    o_h.checkIn("ArmRotateLastFiveProximityEvents", are)
    aude = LastFiveTriggers.LastFiveEvents()
    o_h.checkIn("ArmUpDownLastFiveProximityEvents", aude)
    loce = LastFiveTriggers.LastFiveEvents()
    o_h.checkIn("LocomotionLastFiveProximityEvents", loce)
    locomotion_proximity_obj = EventDriven_DigitalInput.DigitalInputHandler("LocomotionStopSensor")
    o_h.checkIn("LocomotionProximitySensorObj", locomotion_proximity_obj)
    arm_up_down_proximity_sensor_obj = EventDriven_DigitalInput.DigitalInputHandler("ArmUpDownStopSensor")
    o_h.checkIn("ArmUpDownProximitySensorObj", arm_up_down_proximity_sensor_obj)
    arm_rotation_proximity_sensor_obj = EventDriven_DigitalInput.DigitalInputHandler("ArmRotationStopSensor")
    o_h.checkIn("ArmRotationProximitySensorObj", arm_rotation_proximity_sensor_obj)


if __name__ == '__main__':
    app.run(debug=True)


def move_stepper(device_name, position):
    logging.debug("About to move the stepper for " + device_name)
    try:
        o_h = ObjectHotel.ObjectHotel()
        device_handle = o_h.visit(device_name)
        pos = device_handle.getPosition()
        logging.debug(device_name + " started out at position " + pos + ", moving to " + position)
        device_handle.setTargetPosition(position)
    except PhidgetException as e:
        logging.error("Unable to move the stepper motor for " + device_name, exc_info=True)
    except Exception as e:
        logging.error("Unable to move the stepper motor for " + device_name + "for an unknown reason", exc_info=True)
    return


'''time.sleep(15)
    lmrc = LinearMotorRelayController.LinearMotorActuator("CloseGripper")
    lmrc.setVoltageChangeTrigger(0.01)
    lmrc.actuate_lm(True)
    time.sleep(3)
    print(lmrc.get_state())
    lmrc.actuate_lm(False)
    print(lmrc.get_state())
    lmrc.setVoltageChangeTrigger(0.1)
    time.sleep(1)
    lmrc = LinearMotorRelayController.LinearMotorActuator("OpenGripper")
    lmrc.setVoltageChangeTrigger(0.01)
    lmrc.actuate_lm(True)
    time.sleep(3)
    print(lmrc.get_state())
    lmrc.actuate_lm(False)
    print(lmrc.get_state())
    lmrc.setVoltageChangeTrigger(0.1)'''