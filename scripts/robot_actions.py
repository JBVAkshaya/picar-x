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

    ## Turn wheels right
    for angle in range(0,35):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)
    
    ## Move Forward
    px.forward(50)
    time.sleep(0.5)
    px.stop()
    time.sleep(0.1)

    ## Straighten wheels and move back
    for angle in range(35, 0, -1):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)
    px.backward(30)
    time.sleep(1)
    px.stop()
    time.sleep(0.1)

    ## Move back while steering to right. Thish will straighten the car
    for angle in range(0,25):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)
    px.backward(30)
    time.sleep(1.1)
    px.stop()
    time.sleep(0.1)

    ## Straighten wheel and move in front.
    for angle in range(25, 0 , -1):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)
    px.forward(20)
    time.sleep(1)
    px.stop()
    time.sleep(0.1)

def park_right():
    px = Picarx()

    ## Turn wheels left
    for angle in range(0,-35, -1):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)
    
    ## Move Forward
    px.forward(50)
    time.sleep(0.5)
    px.stop()
    time.sleep(0.1)

    ## Straighten wheels and move back
    for angle in range(-35, 0):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)
    px.backward(30)
    time.sleep(1)
    px.stop()
    time.sleep(0.1)

    ## Move back while steering to left. Thish will straighten the car
    for angle in range(0,-25, -1):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)
    px.backward(30)
    time.sleep(1.1)
    px.stop()
    time.sleep(0.1)

    ## Straighten wheel and move in front.
    for angle in range(-25, 0):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)
    px.forward(20)
    time.sleep(1)
    px.stop()
    time.sleep(0.1)

def turn_left(px):
    for angle in range(0,-30, -1):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)
    px.forward(35)
    time.sleep(1)
    for angle in range(-30, 0):
        px.set_dir_servo_angle(angle)
        time.sleep(0.01)
    

def k_turn(px):
    turn_left(px)

if __name__ == "__main__":
    # move_straight()
    # park_left()
    # park_right()
    px = Picarx()
    k_turn(px)