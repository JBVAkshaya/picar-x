import sys
sys.path.insert(1, '../../picar-x/lib')
from bus import Bus
import time
import concurrent.futures
import logging

logging.basicConfig(level=logging.DEBUG)

def func1(b1, delay_time):
    while True:
        logging.debug("in func1")
        b1.write("writing in func1")
        time.sleep(delay_time)

def func2(b1, b2, delay_time):
    while True:
        logging.debug("in func2")
        val = b1.read()
        b2.write(val)
        time.sleep(delay_time)

#### Multitasking
if __name__=="__main__":
    sensor_bus = Bus()
    interpret_bus = Bus()
    
    logging.info("Starting multitasking...")

    with concurrent.futures.ThreadPoolExecutor(max_workers =2) as executor:
        logging.debug("start sen")
        eSensor = executor.submit(func1, sensor_bus , 1)
        logging.debug("start inter")
        eInterpreter = executor.submit (func2, sensor_bus, interpret_bus , 1)
        

    eSensor.result()
    eInterpreter.result()