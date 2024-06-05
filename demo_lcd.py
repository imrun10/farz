#! /usr/bin/env python

# Simple string program. Writes and updates strings.
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel

# Import necessary libraries for communication and display use
import drivers
from time import sleep

# Load the driver and set it to "display"
# If you use something from the driver library use the "display." prefix first

def debugLcd(text):
    display = drivers.Lcd()

    # Main body of code

    print(text)
    
    display.lcd_display_string(text, 1)   # Refresh the first line of display with a different message
    sleep(5)                                           # Give time for the message to be read
    display.lcd_clear()                                # Clear the display of any data
    sleep(2)                                           # Give time for the message to be read
    display.lcd_clear()


debugLcd("paper  :) BDGY##78272JUR")
debugLcd("metal")
debugLcd("plastic")
debugLcd("other")

