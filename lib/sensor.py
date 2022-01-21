from cv2 import log
from adc import ADC
import logging

class Sensor(object):
    def __init__(self):
        self.chn_0 = ADC("A0")
        self.chn_1 = ADC("A1")
        self.chn_2 = ADC("A2")
    
    def sensor_reading(self):
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list

if __name__=="__main__":
    sensor = Sensor()
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"Sensor reading: {sensor.sensor_reading()}")
