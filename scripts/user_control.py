from distutils.log import debug
from robot_actions import move_straight, k_turn, park_right, park_left

import logging 

logging_format = "%(asctime)s : %(message)s"
logging.basicConfig ( format = logging_format , level = logging.INFO ,
datefmt ="% H :% M :% S ")

logging.getLogger().setLevel(logging.DEBUG)

if __name__=="__main__":
    while(1):
        val = input('Enter action: \n To move straight: 8, \n To park right: 6, \n To park left: 4, \n To make K turn: 5')
    logging.debug("Entered val: %d", val)

