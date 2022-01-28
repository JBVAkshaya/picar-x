import sys
sys.path.insert(1, '../../picar-x/lib')
from bus import Bus
from picarx_improved import Picarx
from controller import Controller
from interpreter import Interpreter
from sensor import Sensor
import time
import concurrent.futures
import logging

logging.basicConfig(level=logging.DEBUG)

#### Multitasking
if __name__=="__main__":
    sensor_bus = Bus()
    interpret_bus = Bus()
    car = Picarx()
    sensor = Sensor()
    interpret = Interpreter(sensor.polarity, sensor.sensitivity)
    control_car = Controller(car)
    logging.info("Starting multitasking...")
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers =3) as executor:
            logging.debug("start sen")
            eSensor = executor.submit(sensor.sensor_reading, sensor_bus , 200)
            logging.debug("start inter")
            eInterpreter = executor.submit (interpret.interpret_sensor, sensor_bus, interpret_bus , 150)
            logging.debug("start control")
            eController = executor.submit (control_car.car_control, interpret_bus , 100, 20)
    
        eSensor.result()
        eInterpreter.result()
        eController.result()