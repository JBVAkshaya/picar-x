import logging
from sensor import Sensor
from interpreter import Interpreter
from picarx_improved import Picarx
import time

logging.basicConfig(level=logging.DEBUG)

class Controller(object):
    def __init__(self, car):
        self.car = car
        # self.car.set_dir_servo_angle(int(-offset*turn_angle))

    def _control (self, offset, steer_angle):
        '''
        The main control method should call the steering-servo method from your car class so that 
        it turns the car toward the line. It should also return the commanded steering angle.
        '''
        steer_angle = int(-offset*steer_angle)
        self.car.set_dir_servo_angle(steer_angle)
        logging.debug(f"Steering Angle: {steer_angle}")
        return steer_angle

    ##### Controller read from interpreter bus and writes to controller bus: Consumer-producer
    def car_control(self, interpreter_bus, delay_time, steer_angle):
        while True:
            offset = interpreter_bus.read()
            self._control(offset, steer_angle)
            time.delay(delay_time)

# if __name__=="__main__":
#     sensor = Sensor()
#     polarity, sensitivity = sensor.calibrate()
#     interpret = Interpreter(polarity, sensitivity)
#     car = Picarx()
#     robot_position = interpret.output(sensor.sensor_reading())
#     controller = Controller(car, robot_position, 20)
    
#     while(1):
#         sensor_vals = sensor.sensor_reading()
#         robot_position = interpret.output(sensor_vals)
#         controller.control(robot_position, 20)
#         car.forward(20)
#     car.stop()