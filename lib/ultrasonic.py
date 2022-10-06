import logging
import time
try:
    from pin import Pin
except:
    logging.info("Not on pi")

logging.basicConfig(level=logging.DEBUG)

class Ultrasonic():
    def __init__(self, timeout=0.02):
        try:
            self.trig = Pin("D2") 
            self.echo = Pin("D3")
            self.timeout = timeout
        except:
            logging.info("not on pi")

    def _read(self):
        self.trig.low()
        time.sleep(0.01)
        self.trig.high()
        time.sleep(0.00001)
        self.trig.low()
        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()
        while self.echo.value()==0:
            pulse_start = time.time()
            if pulse_start - timeout_start > self.timeout:
                return -1
        while self.echo.value()==1:
            pulse_end = time.time()
            if pulse_end - timeout_start > self.timeout:
                return -1
        during = pulse_end - pulse_start
        cm = round(during * 340 / 2 * 100, 2)
        return cm

    def read(self, times=10):
        try:
            for i in range(times):
                a = self._read()
                logging.info(f"ultrasonic sensor reading: {a}")
                if a != -1 or a <= 300:
                    return a
            return -1
        except:
            return -1
    