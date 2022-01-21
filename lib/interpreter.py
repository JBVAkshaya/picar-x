import logging
from sensor import Sensor

logging.basicConfig(level=logging.DEBUG)

class Interpreter(object):
    def __init__(self, polarity, sensitivity):
        self.sensitivity = sensitivity
        self.polarity = polarity

        pass
    def processing(self, sensor_val):
        '''
        It should then identify if there is a sharp change in the sensor values
        (indicative of an edge), and then using the edge location and sign to determine both whether
        the system is to the left or right of being centered, and whether it is very off-center or only
        slightly off-center. Make this function robust to different lighting conditions, and with an
        option to have the “target” darker or lighter than the surrounding floor.
        '''
        logging.debug(f"sensor vals: {sensor_val}")
        pass

    def output(self):
        '''
        The output method should return the position of the robot relative to the line as a value on
        the interval [−1,1], with positive values being to the left of the robot.
        '''
        pass

if __name__ =="__main__":
    sensor = Sensor()
    polarity, sensitivity = sensor.calibrate()
    interpret = Interpreter(polarity,sensitivity)
    interpret.processing(sensor.sensor_reading())
    logging.debug(f"pol, sensi: {polarity,sensitivity}")
    