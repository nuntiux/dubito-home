#!/usr/bin/python

import time
import RPi.GPIO as GPIO

def main():

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(25,GPIO.IN)
    while True:
        if GPIO.input(25):
             # the button is being pressed, so turn on the green LED
             # and turn off the red LED
             print "button true"
        else:
             # the button isn't being pressed, so turn off the green LED
             # and turn on the red LED
             print "button false"

        time.sleep(0.1)
    print "button pushed"
    GPIO.cleanup()

if __name__=="__main__":
    main()
