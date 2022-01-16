import sys
sys.path.insert(1, '../../picar-x/lib')
from picarx_improved import Picarx
import time

import logging 

logging_format = "%(asctime)s : %(message)s"
logging.basicConfig ( format = logging_format , level = logging.INFO ,
datefmt ="% H :% M :% S ")

logging.getLogger().setLevel(logging.DEBUG)

def move_straight():
    px = Picarx()
    px.forward(50)
    time.sleep(0.5)
    px.stop()
    time.sleep(0.1)
    px.backward(50)
    time.sleep(0.5)

def park_left():
    px = Picarx()
    px.set_dir_servo_angle(0)
    time.sleep(0.1)
    for angle in range(0,25):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)
    px.forward(20)
    time.sleep(1)
    px.stop()
    time.sleep(1)
    # for angle in range(-15,0):
    #     px.set_dir_servo_angle(angle)
    #     time.sleep(0.01)
    px.backward(20)
    time.sleep(2)
    px.stop()
    time.sleep(1)
    px.set_dir_servo_angle(0)
    time.sleep(0.1)
    px.forward(20)
    time.sleep(1)
    px.stop()
    time.sleep(1)



if __name__ == "__main__":
    # move_straight()
    park_left()