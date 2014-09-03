#!/usr/bin/python

import time
import RPi.GPIO as GPIO

def main():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(25,GPIO.IN)
    while True:
        if (GPIO.input(25) == False):
		print "button pressed"
        else:
             	print "...."

        time.sleep(1)
    #print "button pushed"
    GPIO.cleanup()

if __name__=="__main__":
    main()
