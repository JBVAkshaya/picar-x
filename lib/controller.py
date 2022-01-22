import logging
from sensor import Sensor
from interpreter import Interpreter
from picarx_improved import Picarx

logging.basicConfig(level=logging.DEBUG)

class Controller(object):
    def __init__(self, car, offset, turn_angle):
        self.car = car
        self.car.set_dir_servo_angle(offset*turn_angle)

    def control (self, offset, steer_angle):
        '''
        The main control method should call the steering-servo method from your car class so that 
        it turns the car toward the line. It should also return the commanded steering angle.
        '''
        steer_angle = int(-offset*steer_angle)
        self.car.set_dir_servo_angle(steer_angle)
        logging.debug(f"Steering Angle: {steer_angle}")
        return steer_angle

if __name__=="__main__":
    sensor = Sensor()
    polarity, sensitivity = sensor.calibrate()
    interpret = Interpreter(polarity, sensitivity)
    car = Picarx()
    controller = Controller(car, interpret.output(sensor.sensor_reading()),20)
    while(1):
        sensor_vals = sensor.sensor_reading()
        controller.control(interpret.output(sensor_vals), 20)
