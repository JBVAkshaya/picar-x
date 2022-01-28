from cv2 import log
from adc import ADC
import logging
import time

class PolarityException(Exception):
    pass

class SensitivityException(Exception):
    pass

class EnvException(Exception):
    pass

class Sensor(object):
    def __init__(self):
        self.chn_0 = ADC("A0")
        self.chn_1 = ADC("A1")
        self.chn_2 = ADC("A2")
        self.polarity, self.sensitivity = self.calibrate(self._read())
    
    def _read(self):
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())

        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list

    def sensor_reading(self, sensor_bus, delay_time):
        '''
        Sensor data Producer: Publishes the data to sensor_bus bus. 
        '''
        
        while True:
            sensor_bus.write(self._read())
            time.sleep(0.001*delay_time)

    def _get_polarity(self, sensor_vals):
        if ((sensor_vals[1] - sensor_vals[0]) < 0 and (sensor_vals[1] - sensor_vals[2]) < 0):
            return "darker"
        elif ((sensor_vals[1] - sensor_vals[0]) > 0 and (sensor_vals[1] - sensor_vals[2]) > 0):
            return "lighter"
        else:
            raise PolarityException(f"No definite Polarity in sensor reading: {sensor_vals}")

    def _get_sensitivity(self, sensor_vals):
        sensitivity = -1
        diff_l_r = abs(sensor_vals[0] - sensor_vals[2])
        diff_l_c = abs(sensor_vals[0] - sensor_vals[1])
        diff_r_c = abs(sensor_vals[2] - sensor_vals[1])

        if ((diff_l_r < diff_r_c) and (diff_l_r < diff_l_c)):
            sensitivity = diff_l_r + (min(diff_l_c, diff_r_c) - diff_l_r)/2.0
            if sensitivity <60:
                raise EnvException(f"Cannot differentiate Background and line in sensor space.\nVals: {sensor_vals}")
        else:
            raise SensitivityException(f"Bizar sensor reading: {sensor_vals}.\nSet the robot so that center sensor is on line and left and right sensors on ground")
        
        return sensitivity


    def calibrate(self, sensor_vals):
        # Read sensor value:
        polarity, sensitivity = 'Err', -1
        try:
            polarity = self._get_polarity(sensor_vals)
            sensitivity = self._get_sensitivity(sensor_vals)
        except PolarityException as e:
            logging.exception(e)
        except SensitivityException as e:
            polarity = -1
            logging.exception(e)
        except EnvException as e:
            polarity = 'Err'
            logging.exception(e)    
        except Exception as e:
            logging.exception(f"Unknown error: {e}")
        return polarity, sensitivity


if __name__=="__main__":
    sensor = Sensor()
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f"Sensor reading: {sensor._read()}")
    logging.info("Calibrating...")
    logging.info(f"Sensor Polarity and sensitivity: {sensor.calibrate(sensor._read())}")