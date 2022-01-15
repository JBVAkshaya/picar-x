import sys
sys.path.insert(1, '../../picar-x/lib')
from picarx_improved import Picarx
import time

import logging 

logging_format = "%(asctime)s : %(message)s"
logging.basicConfig ( format = logging_format , level = logging.INFO ,
datefmt ="% H :% M :% S ")

logging.getLogger().setLevel(logging.DEBUG)

if __name__ == "__main__":
    px = Picarx()
    px.forward(50)
    time.sleep(1)
