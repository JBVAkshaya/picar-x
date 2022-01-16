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
    px.backward(50)
    time.sleep(0.5)

if __name__ == "__main__":
    move_straight()