#!/usr/bin/python

import RPi.GPIO as gpio
from time import sleep

class Shifter():

        dataPin=22
	latchPin=11
        clockPin=9
        clearPin=10


        def __init__(self):
            self.setupBoard()
            self.pause=0

        def tick(self):
            gpio.output(Shifter.clockPin,gpio.HIGH)
            sleep(0)
            gpio.output(Shifter.clockPin,gpio.LOW)

        def latch(self):
            gpio.output(Shifter.latchPin,gpio.HIGH)
            sleep(0)
            gpio.output(Shifter.latchPin,gpio.LOW)

        def clear(self):
	    print 'Clear!!!'
            gpio.output(Shifter.clearPin,gpio.LOW)
            Shifter.latch(self)
	    sleep(1)
            gpio.output(Shifter.clearPin,gpio.HIGH)

        def setPin(self,value):
	    print 'Printing %s' % value
		
            for i in xrange(1, 9):
		print '   loop %s - %s' % (i, value)
                if (i == value):
		    print '    OK'
                    gpio.output(Shifter.dataPin,gpio.HIGH)
                else:
                    gpio.output(Shifter.dataPin,gpio.LOW)
                Shifter.tick(self)
	    Shifter.latch(self)

        def setupBoard(self):
            gpio.setup(Shifter.dataPin,gpio.OUT)
            gpio.output(Shifter.dataPin,gpio.LOW)
            gpio.setup(Shifter.latchPin,gpio.OUT)
            gpio.output(Shifter.latchPin,gpio.LOW)
            gpio.setup(Shifter.clockPin,gpio.OUT)
            gpio.output(Shifter.clockPin,gpio.LOW)
            gpio.setup(Shifter.clearPin,gpio.OUT)
            gpio.output(Shifter.clearPin,gpio.HIGH)

def main():
    pause=0.2
    gpio.setmode(gpio.BCM)
    shifter=Shifter()
    shifter.setupBoard()
    shifter.clear()
    running=True
    while running==True:
	try:
		for i in xrange(1, 9):
			shifter.setPin(i)
			sleep(pause)
	except KeyboardInterrupt:
		running=False
		shifter.clear()

if __name__=="__main__":
    main()
