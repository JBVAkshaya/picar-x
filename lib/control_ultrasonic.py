import logging
from interpret_ultrasonic import InterpretUltrasonic
from ultrasonic import Ultrasonic
from picarx_improved import Picarx

class ControlUltrasonic(object):
    def __init__(self, car, speed=30):
        try:
            self.car = car
            self.speed = speed
        # self.car.set_dir_servo_angle(int(-offset*turn_angle))
        except:
            logging.info("not on pi!!")
            self.car = car
            self.speed = speed

    def control (self, status):
        '''
        The main control method should call the steering-servo method from your car class so that 
        it turns the car toward the line. It should also return the commanded steering angle.
        '''
        try:
            if status==0:
                print('status 0')
                self.car.stop()
            else:
                print('status 1')
                self.car.forward(self.speed)
        except:
            logging.info(f"not on pi move status: {status}")

if __name__=="__main__":
    sense = Ultrasonic()
    car = Picarx()
    interp = InterpretUltrasonic()
    control1 = ControlUltrasonic(car)
    while True:
        print(sense.read())
        print(interp.output(sense.read()))
        print(control1.control(interp.output(sense.read())))