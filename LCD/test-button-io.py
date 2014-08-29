#!/usr/bin/python

import time
import RPi.GPIO as GPIO


# handle the button event
def buttonEventHandler (pin):
    print "handling button event"


# main function
def main():

    # tell the GPIO module that we want to use 
    # the chip's pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # setup pin 25 as an input
    GPIO.setup(25,GPIO.IN)

    # tell the GPIO library to look out for an 
    # event on pin 25 and deal with it by calling 
    # the buttonEventHandler function
    GPIO.add_event_detect(25,GPIO.FALLING)
    GPIO.add_event_callback(25,buttonEventHandler,100)

    # make the red LED flash
    while True:
        print "Sleeping...."
        time.sleep(2)

    GPIO.cleanup()
if __name__=="__main__":
    main()

