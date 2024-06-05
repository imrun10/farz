import RPi.GPIO as GPIO # Importing the RPi.GPIO library as GPIO for Raspberry Pi GPIO control import time # Importing the time module for time-related functions
import time
# Define GPIO pins connected to L298N motor driver
IN1 = 17  # Assigning GPIO pin numbers to inputs of the L298N motor driver
IN2 = 18  
IN3 = 27  
IN4 = 22  

# Set GPIO mode
GPIO.setmode(GPIO.BCM)  # Setting the GPIO mode to use Broadcom SOC channel numbers

# Set up GPIO pins as outputs
GPIO.setup(IN1, GPIO.OUT)  # Configuring GPIO pins as outputs
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Function to move stepper motor clockwise
def move_clockwise(steps, delay):
    for _ in range(steps):  # Looping through the specified number of steps
        set_step(1, 0, 1, 0)  # Setting the stepper motor sequence for clockwise movement
        time.sleep(delay)  # Pausing for the specified delay
        set_step(0, 1, 1, 0)
        time.sleep(delay)
        set_step(0, 1, 0, 1)
        time.sleep(delay)
        set_step(1, 0, 0, 1)
        time.sleep(delay)

# Function to set the inputs to the L298N motor driver
def set_step(w1, w2, w3, w4):
    GPIO.output(IN1, w1)  # Setting the GPIO output values according to the provided sequence
    GPIO.output(IN2, w2)
    GPIO.output(IN3, w3)
    GPIO.output(IN4, w4)

# Example usage
if __name__ == "__main__":
    try:
        while True:  # Running an infinite loop
            move_clockwise(40, 0.005)  # Moving the stepper motor clockwise for 200 steps with a delay of 0.02 seconds between steps
            time.sleep(1)  # Pausing for 1 second
    except KeyboardInterrupt:  # Handling KeyboardInterrupt (Ctrl+C)
        GPIO.cleanup()  # Cleaning up GPIO resources upon program exit

