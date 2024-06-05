import cv2
import serial
from lobe import ImageModel
import os
import time
from gpiozero import Servo
import math
from time import sleep
import RPi.GPIO as GPIO
from roboflow import Roboflow
from gpiozero.pins.pigpio import PiGPIOFactory
import numpy as np
from PIL import Image
import tensorflow as tf

#PINS
CW = 1 
CCW = 0
Dir = 20
Stp = 21

paper = 1
metal = 2
plastic = 3
other = 4
servoPin = 4
import drivers
GPIO.cleanup()

import RPi.GPIO as GPIO
import time





def sensor():
    # Set the GPIO mode to BCM (Broadcom SOC channel numbering)
    GPIO.setmode(GPIO.BCM)

    # Set the pin number connected to the touch sensor
    TOUCH_PIN = 12

    # Set the GPIO pin as an input

    # Variable to track the touch sensor state

    # Variable to track the start time of touch

    activated = False
    try:
        while True:
            input("press enter")

            print("Activated")
            prediction = predict()
            print(prediction)
            finalResult = handleResult(prediction)
            motors(finalResult)
            activated = True
            # Reset touch start time after activation


            time.sleep(0.1)  # A small delay to debounce the input

    
    except KeyboardInterrupt:
        # Clean up the GPIO settings on program exit
        GPIO.cleanup()
    return activated            

def motors(quad):
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
        for i in range(190, 210):  # Adjusted angle range from 190 to 210 degrees
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

    try:
        # Duration values for each quadrant
        duration_values = {1: 0.043, 2: 0.0650, 3: 0.08, 4: 0.0098} #1:paper, 2: metal, 3: plastic, 4: general

        # Final duration values for each quadrant
        final_duration_values = {1: 0.064, 2: 0.03, 3: 0.018, 4: 0.088}

        material_quadrant = quad  # Change this to the desired material quadrant (1, 2, 3, or 4)

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

# Define the file path for the snapshot
file_address = "/home/pi/Documents/ML Bins/snapshot.jpg"

# GPIO Mode (BCM) sets the pins
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use GPIO pins
GPIO.cleanup()
GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(Dir, GPIO.OUT)
GPIO.setup(Stp, GPIO.OUT)


def predict():
    model_path = 'best_float32.tflite'

    def capture_image():
        
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('snapshot.jpg', frame)
        cap.release()

    capture_image()

    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Obtain the height and width of the corresponding image from the input tensor
    image_height = input_details[0]['shape'][1] # 640
    image_width = input_details[0]['shape'][2] # 640

    # Image Preparation
    image_name = 'snapshot.jpg'
    image = Image.open(image_name)
    image_resized = image.resize((image_width, image_height)) # Resize the image to the corresponding size of the input tensor and store it in a new variable

    image_np = np.array(image_resized)
    image_np = np.true_divide(image_np, 255, dtype=np.float32)
    image_np = image_np[np.newaxis, :]

    # inference
    interpreter.set_tensor(input_details[0]['index'], image_np)

    start = time.time()
    interpreter.invoke()
    print(f'run time：{time.time() - start:.2f}s')

    # Obtaining output results
    output = interpreter.get_tensor(output_details[0]['index'])
    output = output[0]
    output = output.T

    boxes_xywh = output[..., :4] #Get coordinates of bounding box, first 4 columns of output tensor
    scores = np.max(output[..., 4:], axis=1) #Get score value, 5th column of output tensor
    classes = np.argmax(output[..., 4:], axis=1) # Get the class value, get the 6th and subsequent columns of the output tensor, and store the largest value in the output tensor.

    # Threshold Setting
    threshold = 0.3

    # List to store predicted labels
    predicted_labels = []

    for box, score, cls in zip(boxes_xywh, scores, classes):
        if score >= threshold:
            predicted_labels.append(cls)

    classes = {
        0: "BIODEGRADABLE",
        1: "CARDBOARD",
        2: "GLASS",
        3: "METAL",
        4: "PAPER",
        5: "PLASTIC"
    }

    prediction_label = classes[list(set(predicted_labels))[0]]
    print("Predicted Label : ", prediction_label)
    return prediction_label 


def debug(): #rotates all bins
    enter = input("choose debug")
    if enter == "1":
        predict()


#Save to file 
def increment_value(term: str):
    filename = "save.txt"  # Replace with the actual file name

    # Read the file
    with open(filename, 'r') as file:
        data = file.readlines()

    # Process the data
    values = {}
    for line in data:
        key, value = line.strip().split(':')
        values[key.strip()] = int(value.strip())

    # Increment the value for the specified term
    if term in values:
        values[term] += 1

    # Save the updated values back to the file
    with open(filename, 'w') as file:
        for key, value in values.items():
            file.write(f"{key}: {value}\n")

    print(f"Incremented {term} by one.")



# Function to take a snapshot using the webcam
def take_snapshot(file_path):
    # Open the webcam
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise Exception("Could not open the webcam.")

    # Read a frame from the webcam
    ret, frame = cap.read()

    # Check if the frame was read successfully
    if not ret:
        raise Exception("Failed to capture a frame from the webcam.")

    # Save the frame to the specified file path
    cv2.imwrite(file_path, frame)

    # Release the webcam
    cap.release()

# Function to handle the snapshots
def handle_snapshots(file_path):
    try:
        os.remove(file_path)
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

def handleResult(result):#simplifies all the potentional options
    
    if result == "PAPER" or result == "CARDBOARD":
        return 1 #paper
    elif result == "METAL":
        return 2 #metal
    elif result == "PLASTIC" or result== "GLASS":
        return 3 #plastic
    else: 
        return 4 #general




def SendMessage(result):
    print("SENDING",result)
    if result == "General":
        stepperRotation(general)
    elif result == "paper":
        stepperRotation(paper)
    elif result == "plastic":
        stepperRotation(plastic)
    else:
        stepperRotation(metal)

    print("Prediction:", result)
    increment_value(result) # or send tis to database

# Main loop

def stepperRotation(quadrant):
    # CHNAGE THE ANGLE HERE
    Q1_ANGLE = 300
    Q2_ANGLE = 400
    Q3_ANGLE = 500
    Q4_ANGLE = 600


    def rotate(pins): # pass in pin to rotate

        factory = PiGPIOFactory()
        ope = 90
        clo = 270

        
        servo = Servo(pins, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
    #open 70 - 100   closed  250 - 290




        for i in range(0, 25):             # open rotation 0-100 how much it rotates
            servo.value = math.sin(math.radians(i))
            sleep(0.01) #dont touch this

        servo.value = math.sin(math.radians(0)) #stops rotation when open
        sleep(3) #stays open for 3 sec

        for i in range(190, 208): #close rotaion start from 190 for reverse rotation 190-273 how much it closes
            servo.value = math.sin(math.radians(i))
            sleep(0.01) #dont touch this


        servo.value = math.sin(math.radians(0)) #stops rotation when closed
        sleep(1) #avoid bug
    
        return 1 #avoid bug


    GPIO.setmode(GPIO.BCM)

    def rotate_to_quadrant(material_code,direction):
        GPIO.output(Dir, direction)  # Default to counterclockwise rotation

        # Map material to quadrant angle
        material_to_quadrant = {
            paper: Q1_ANGLE,
            metal: Q2_ANGLE,
            plastic: Q3_ANGLE,
            other: Q4_ANGLE
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

    except KeyboardInterrupt:        # Clean up GPIO channels on program exit
        GPIO.cleanup()

#def everthing in stepper
        
while True:
    sensor()
    #print(sensor())

GPIO.cleanup()
