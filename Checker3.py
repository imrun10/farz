#map to quadrant 
# paper --> 1 --> CW spin to the first quadrant which is 45 degrees 
# metal --> 2 --> CW spin to the second quadrant which is 135 degrees 
# plastic --> 3 --> CCW spin to the third quadrant which is 45 degrees 
# other --> 4 --> CCW spin to the fourth quadrant which is 135 degrees


# basic idea ( how it will work):
#def map_to_quadrant(quadrant):
#    if quadrant == 1:
#        move_stepper(CW, 200)  # 200 steps for 45 degrees clockwise
#    elif quadrant == 2:
#        move_stepper(CW, 600)  # 600 steps for 135 degrees clockwise
#    elif quadrant == 3:
#        move_stepper(CCW, 200) # 200 steps for 45 degrees counterclockwise
#    elif quadrant == 4:
#        move_stepper(CCW, 600) # 600 steps for 135 degrees counterclockwise
#    else:
#        print("Invalid quadrant")

import time
import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
import math
from time import sleep

#CW: clockwise 
#CCW: Counter clockwise
CW = 1 
CCW = 0
Dir = 20
Stp = 21

paper = 1
metal = 2
plastic = 3
other = 4
servoPin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)

# CHNAGE THE ANGLE HERE
Q1_ANGLE = 3000
Q2_ANGLE = 4000
Q3_ANGLE = 5000
Q4_ANGLE = 60000000000


def rotate(pins): # pass in pin to rotate

    factory = PiGPIOFactory()
    ope = 90
    clo = 270

    
    servo = Servo(pins, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
#open 70 - 100   closed  250 - 290


    for i in range(190, 208):             # open rotation 0-100 how much it rotates
        servo.value = math.sin(math.radians(i))
        sleep(0.01) #dont touch this

    servo.value = math.sin(math.radians(0)) #stops rotation when open
    sleep(3) #stays open for 3 sec

    for i in range(0, 25): #close rotaion start from 190 for reverse rotation 190-273 how much it closes
        servo.value = math.sin(math.radians(i))
        sleep(0.01) #dont touch this


    servo.value = math.sin(math.radians(0)) #stops rotation when closed
    sleep(1) #avoid bug
   
    return 1 #avoid bug


GPIO.setmode(GPIO.BCM)
GPIO.setup(Dir, GPIO.OUT)
GPIO.setup(Stp, GPIO.OUT)

def rotate_to_quadrant(material_code,direction):
    GPIO.output(Dir, direction)  # Default to counterclockwise rotation

    # Map material to quadrant angle
    material_to_quadrant = {
        paper: Q1_ANGLE,
        metal: Q2_ANGLE,
        plastic: Q3_ANGLE,
        other: Q4_ANGLE+199
    }

    if material_code in material_to_quadrant:
        desired_angle = material_to_quadrant[material_code]
        steps = int(desired_angle / 1.8)  # 1.8 degrees per step for DRV8825

      

        # Rotate stepper motor
        for _ in range(steps):
            GPIO.output(Stp, GPIO.HIGH)
            time.sleep(0.001)  # Adjust this delay as necessary
            GPIO.output(Stp, GPIO.LOW)
            time.sleep(0.001)  # Adjust this delay as necessary
try:
    # Example: Rotate to the third quadrant (plastic)
    rotate_to_quadrant(other,1)  #**CHANGE THE MATERIAL HERE
    sleep(1)
    rotate(17)
    sleep(1)
    rotate_to_quadrant(other,0)  #**CHANGE THE MATERIAL HERE
    GPIO.cleanup()
except KeyboardInterrupt:
    # Clean up GPIO channels on program exit
    GPIO.cleanup()
