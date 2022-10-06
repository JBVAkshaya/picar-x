# from .basic import _Basic_class
import time

class Servo(object):
    MAX_PW = 2500
    MIN_PW = 500
    _freq = 50
    def __init__(self, pwm):
        super().__init__()

    def map(self, x, in_min, in_max, out_min, out_max):
        return -1
        
    # angle ranges -90 to 90 degrees
    def angle(self, angle):
        pass

import smbus, math
from i2c import I2C

class PWM(I2C):
    REG_CHN = 0x20
    REG_FRE = 0x30
    REG_PSC = 0x40
    REG_ARR = 0x44

    ADDR = 0x14

    CLOCK = 72000000

    def __init__(self, channel, debug="critical"):
        super().__init__()
        pass

    def i2c_write(self, reg, value):
        pass

    def freq(self, *freq):
        pass

    def prescaler(self, *prescaler):
        pass

    def period(self, *arr):
        pass

    def pulse_width(self, *pulse_width):
        pass

    def pulse_width_percent(self, *pulse_width_percent):
        pass

#import RPi.GPIO as GPIO

class Pin(object):
    # OUT = GPIO.OUT
    # IN = GPIO.IN
    # IRQ_FALLING = GPIO.FALLING
    # IRQ_RISING = GPIO.RISING
    # IRQ_RISING_FALLING = GPIO.BOTH
    # PULL_UP = GPIO.PUD_UP
    # PULL_DOWN = GPIO.PUD_DOWN
    PULL_NONE = None

    _dict = {}

    _dict_1 = {}

    _dict_2 = {}

    def __init__(self, *value):
        super().__init__()
        
        
    def check_board_type(self):
        pass

    def init(self, mode, pull=PULL_NONE):
        pass

    def dict(self, *_dict):
        pass

    def __call__(self, value):
        return -1

    def value(self, *value):
        pass

    def on(self):
        return -1
    def off(self):
        return -1

    def high(self):
        return -1

    def low(self):
        return -1
    def mode(self, *value):
        pass

    def pull(self, *value):
        return -1

    def irq(self, handler=None, trigger=None, bouncetime=200):
        pass

    def name(self):
        return -1

    def names(self):
        return ['NA', 'NA']

    class cpu(object):
        pass

        def __init__(self):
            pass

class ADC(I2C):
    #ADDR=0x14

    def __init__(self, chn):
        super().__init__()
        
    def read(self):
        return -1

    def read_voltage(self):
        return -1
        