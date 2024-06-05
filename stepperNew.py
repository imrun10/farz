import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
import time
#define GPIO pins


GPIO_pins = (14, 15, 18) # Microstep Resolution MS1-MS3 -> GPIO Pin
direction= 20       # Direction -> GPIO Pinstep = 21      # Step -> GPIO Pin
step = 21
# Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")
mymotortest.motor_go(False, "Full" , 600,11*.0004, False, .05)


