import logging

class ControlUltrasonic(object):
    def __init__(self, car, speed=10):
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
                self.car.stop()
            else:
                self.car.forward(self.speed)
        except:
            logging.info(f"not on pi move status: {status}")