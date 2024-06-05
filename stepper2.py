import RPi.GPIO as GPIO
import time
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo
import math
from time import sleep

# Define GPIO pins
out1 = 17
out2 = 18
out3 = 27
out4 = 22

# Function to rotate the servo motor
def rotate_servo():
    print("Rotating servo")
    factory = PiGPIOFactory()
    ope = 90
    clo = 270

    # Change '23' to the GPIO pin connected to the servo
    servo = Servo(23, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
    # Open the servo
    for i in range(190, 215):  # Adjusted angle range from 190 to 210 degrees
        servo.value = math.sin(math.radians(i))
        sleep(0.01)

    servo.value = math.sin(math.radians(0))  # Stops rotation when open
    sleep(3)  # Keep it open for 3 seconds

    # Close the servo
    for i in range(0, 60):  # Adjusted angle range from 0 to 60 degrees
        servo.value = math.sin(math.radians(i))
        sleep(0.01)

    servo.value = math.sin(math.radians(0))  # Stops rotation when closed
    sleep(1)

# Function to rotate the stepper motor
def rotate_stepper(duration):
    # Setup GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(out1, GPIO.OUT)
    GPIO.setup(out2, GPIO.OUT)
    GPIO.setup(out3, GPIO.OUT)
    GPIO.setup(out4, GPIO.OUT)

    # Calculate steps
    step_sleep = 0.01
    steps_per_second = 5 / step_sleep
    total_steps = int(steps_per_second * duration)

    try:
        # Rotate stepper
        for _ in range(total_steps):
            GPIO.output(out4, GPIO.HIGH)
            GPIO.output(out3, GPIO.LOW)
            GPIO.output(out2, GPIO.LOW)
            GPIO.output(out1, GPIO.LOW)
            time.sleep(step_sleep)

            GPIO.output(out4, GPIO.LOW)
            GPIO.output(out3, GPIO.HIGH)
            GPIO.output(out2, GPIO.LOW)
            GPIO.output(out1, GPIO.LOW)
            time.sleep(step_sleep)

            GPIO.output(out4, GPIO.LOW)
            GPIO.output(out3, GPIO.LOW)
            GPIO.output(out2, GPIO.HIGH)
            GPIO.output(out1, GPIO.LOW)
            time.sleep(step_sleep)

            GPIO.output(out4, GPIO.LOW)
            GPIO.output(out3, GPIO.LOW)
            GPIO.output(out2, GPIO.LOW)
            GPIO.output(out1, GPIO.HIGH)
            time.sleep(step_sleep)

    except KeyboardInterrupt:
        GPIO.cleanup()
        exit(1)

    GPIO.cleanup()

# Main execution
try:
    # Duration values for each quadrant
    duration_values = {1: 0.043, 2: 0.0650, 3: 0.08, 4: 0.0098}

    # Final duration values for each quadrant
    final_duration_values = {1: 0.059, 2: 0.03, 3: 0.018, 4: 0.088}

    material_quadrant = 4 # Change this to the desired material quadrant (1, 2, 3, or 4)

    # Get the duration for the current quadrant
    duration_stepper = duration_values.get(material_quadrant, 0)
    final_duration_stepper = final_duration_values.get(material_quadrant, 0)

    # Rotate the stepper motor first
    print("Starting first stepper motor rotation")
    rotate_stepper(duration_stepper)
    print("First stepper motor rotation completed")

    # Rotate the servo motor
    rotate_servo()
    print("Servo motor rotation completed")

    # Rotate the stepper motor again
    print("Starting second stepper motor rotation")
    rotate_stepper(final_duration_stepper)
    print("Second stepper motor rotation completed")

except KeyboardInterrupt:
    GPIO.cleanup()
    exit(1)
