import sys
sys.path.insert(1, '../../picar-x/lib')
from rossros import Bus, ConsumerProducer, Producer, Consumer, Timer
import rossros as rs 
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
    default_termination_bus = Bus(False)
    sensor_input_bus = Bus()
    interpret_output_bus = Bus()
    car = Picarx()
    sensor = Sensor()
    interpret = Interpreter(sensor.polarity, sensor.sensitivity)
    control_car = Controller(car, 20.0)
    consumer_producer = ConsumerProducer(interpret.output, 
                                        input_busses=sensor_input_bus, 
                                        output_busses=interpret_output_bus,
                                        delay=1.0,
                                        termination_busses=default_termination_bus,
                                        name="interpret_sensor_cp")
    producer = Producer(sensor.read,
                 sensor_input_bus,
                 delay=1.0,
                 termination_busses=default_termination_bus,
                 name="sensor_p")
    
    consumer = Consumer(control_car.control,
                 interpret_output_bus,
                 delay=1.0,
                 termination_busses=default_termination_bus,
                 name="control_c")

    timer_producer = Timer(default_termination_bus,  # busses that should be set to true when timer triggers
                 duration=1.0,  # how many seconds the timer should run for (0 is forever)
                 delay=0,  # how many seconds to sleep for between checking time
                 termination_busses=default_termination_bus,
                 name="timer_p")

    producer_consumer_list = [producer, consumer_producer, consumer, timer_producer]

    rs.runConcurrently(producer_consumer_list)
    # sensor_bus = Bus()
    # interpret_bus = Bus()
    # car = Picarx()
    # sensor = Sensor()
    # interpret = Interpreter(sensor.polarity, sensor.sensitivity)
    # control_car = Controller(car)
    # logging.info("Starting multitasking...")
    # while True:
    #     with concurrent.futures.ThreadPoolExecutor(max_workers =3) as executor:
    #         logging.debug("start sen")
    #         eSensor = executor.submit(sensor.sensor_reading, sensor_bus , 1.0)
    #         logging.debug("start inter")
    #         eInterpreter = executor.submit (interpret.interpret_sensor, sensor_bus, interpret_bus , 1.0)
    #         logging.debug("start control")
    #         eController = executor.submit (control_car.car_control, interpret_bus , 1.0)
    
    #     eSensor.result()
    #     eInterpreter.result()
    #     eController.result()