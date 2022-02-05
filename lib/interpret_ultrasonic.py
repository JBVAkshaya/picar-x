import logging

class InterpretUltrasonic:
    def __init__(self):
        pass

    def output(self, sensor_val):
        if sensor_val < 150:
            return 0
        else: 
            return 1