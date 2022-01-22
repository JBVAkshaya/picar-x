import logging
from sensor import Sensor

logging.basicConfig(level=logging.DEBUG)

class Interpreter(object):
    def __init__(self, polarity, sensitivity):
        self.sensitivity = sensitivity
        self.polarity = polarity
        self.prev_output = 0.0
        pass
    def processing(self, sensor_val):
        '''
        It should then identify if there is a sharp change in the sensor values
        (indicative of an edge), and then using the edge location and sign to determine both whether
        the system is to the left or right of being centered, and whether it is very off-center or only
        slightly off-center. Make this function robust to different lighting conditions, and with an
        option to have the “target” darker or lighter than the surrounding floor.
        '''
        diff_c_r = abs(sensor_val[1]-sensor_val[2])
        diff_c_l = abs(sensor_val[1]-sensor_val[0])
        
        if  self.polarity == "lighter":
    
            if ((diff_c_l > self.sensitivity) and (diff_c_r > self.sensitivity)):
                return 'c'
            elif ((sensor_val[1]>sensor_val[0]) and (diff_c_l > self.sensitivity) and (diff_c_r < self.sensitivity)):
                return 'l'
            elif ((sensor_val[2]>sensor_val[1]) and (diff_c_r > self.sensitivity) and (diff_c_l < self.sensitivity)):
                return 'l+'
            elif ((sensor_val[1]>sensor_val[2]) and (diff_c_r > self.sensitivity) and (diff_c_l < self.sensitivity)):
                return 'r'
            elif ((sensor_val[0]>sensor_val[1]) and (diff_c_l > self.sensitivity) and (diff_c_r < self.sensitivity)):
                return 'r+'
            else:
                return 'o'
        elif    self.polarity == "darker":

            if ((diff_c_l > self.sensitivity) and (diff_c_r > self.sensitivity)):
                return 'c'
            elif ((sensor_val[1]<sensor_val[0]) and (diff_c_l > self.sensitivity) and (diff_c_r < self.sensitivity)):
                return 'l'
            elif ((sensor_val[2]<sensor_val[1]) and (diff_c_r > self.sensitivity) and (diff_c_l < self.sensitivity)):
                return 'l+'
            elif ((sensor_val[1]<sensor_val[2]) and (diff_c_r > self.sensitivity) and (diff_c_l < self.sensitivity)):
                return 'r'
            elif ((sensor_val[0]<sensor_val[1]) and (diff_c_l > self.sensitivity) and (diff_c_r < self.sensitivity)):
                return 'r+'
            else:
                return 'o'
        else:
            logging.error(f"Unknown Polarity: {self.polarity}")
            return 'Err'

    def output(self, sensor_val):
        '''
        The output method should return the position of the robot relative to the line as a value on
        the interval [−1,1], with positive values being to when the line is to the left of the robot.
        '''
        robot_position = self.processing(sensor_val)
        if robot_position == 'c':
            self.prev_output = 0.0
            return 0.0
        elif robot_position == 'l':
            self.prev_output = 0.33
            return 0.33
        elif robot_position == 'l+':
            self.prev_output = 0.66
            return -0.66
        elif robot_position == 'r':
            self.prev_output = 0.33
            return 0.33
        elif robot_position == 'r+':
            self.prev_output = 0.66
            return 0.66
        elif robot_position == 'o':
            # if self.prev_output > 0.0:
            #     return 1.0
            # elif self.prev_output < 0.0:
            #     return -1.0
            # else:
            #     return 0.0
            logging.error(f"Out of range robot position: {robot_position}")
            return 5.0
        else:
            logging.error(f"Unknown Robot Position: {robot_position}")
            return 5.0

if __name__ =="__main__":
    sensor = Sensor()
    polarity, sensitivity = sensor.calibrate()
    interpret = Interpreter(polarity,sensitivity)
    interpret.processing(sensor.sensor_reading())
    logging.debug(f"pol, sensi: {polarity,sensitivity}")