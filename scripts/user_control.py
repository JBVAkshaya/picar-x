from distutils.log import debug
from robot_actions import move_straight, k_turn, park_right, park_left

import logging 

logging_format = "%(asctime)s : %(message)s"
logging.basicConfig ( format = logging_format , level = logging.INFO ,
datefmt ="% H :% M :% S ")

logging.getLogger().setLevel(logging.DEBUG)

if __name__=="__main__":
    while(1):
        val = int(input('To move straight: 8, \n To park right: 6, \n To park left: 4, \n To make K turn: 5 \n To exit: 0 \n Enter action:'))
        logging.debug(" \n Entered val: %d", val)
        if val == 8:
            move_straight()
        elif val == 6:
            park_right()
        elif val == 4:
            park_left()
        elif val == 5:
            k_turn()
        elif val == 0:
            break
        else:
            logging.error('Entered invalid action.')
