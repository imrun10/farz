from gpiozero import Servo
import math
from time import sleep
 
from gpiozero.pins.pigpio import PiGPIOFactory
 



def rotate(pins):
    factory = PiGPIOFactory()


    
    servo = Servo(pins, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)



    for i in range(0, 92):
        servo.value = math.sin(math.radians(i))
        sleep(0.01)

    servo.value = math.sin(math.radians(0))
    sleep(3)

    for i in range(190, 270):
        servo.value = math.sin(math.radians(i))
        sleep(0.01)


    servo.value = math.sin(math.radians(0))


rotate(17)
