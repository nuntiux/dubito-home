#!/usr/bin/python

import time
import RPi.GPIO as GPIO


#time_stamp = time.time()

# handle the button event
def buttonEventHandler (pin):
	#global time_stamp
	#time_now = time.time()
	#if (time_now - time_stamp) >= 0.2:
    		print "handling button event"
	#else:
	#	print "bounce"
	#time_stamp = time_now


# main function
def main():

    # tell the GPIO module that we want to use 
    # the chip's pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    # setup pin 25 as an input
    GPIO.setup(25,GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # tell the GPIO library to look out for an 
    # event on pin 25 and deal with it by calling 
    # the buttonEventHandler function
    GPIO.add_event_detect(25,GPIO.FALLING, callback=buttonEventHandler, bouncetime=200)

    # make the red LED flash
    while True:
        print "Sleeping...."
        time.sleep(2)

    GPIO.cleanup()
if __name__=="__main__":
    main()

