import logging

class InterpretUltrasonic:
    def __init__(self):
        pass

    def output(self, sensor_val):
        if sensor_val>4.0 and sensor_val < 15:
            return 0
        else: 
            return 1