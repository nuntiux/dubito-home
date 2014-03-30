#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import * 
from time import sleep, strftime
from datetime import datetime

lcd = Adafruit_CharLCD()

lcd.clear()
lcd.begin(16,1)

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
MATRIX = [ [ 1, 2, 3, 'A' ],
	   [ 4, 5, 6, 'B' ],
	   [ 7, 8, 9, 'C' ],
	   [ 'E', 0, 'F', 'G' ] ]

ROW = [ 11, 9, 10, 22 ]
COL = [ 27, 17, 4, 3 ]

# handle the button event
def buttonEventHandler (pin):
	print "handling button event %s" % pin
	lcd.message ('Btn %s' % pin)
	time.sleep(1)

GPIO.setmode(GPIO.BCM)

for j in range (4):
	GPIO.setup(ROW[j], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	GPIO.add_event_detect(ROW[j],GPIO.FALLING)
	GPIO.add_event_callback(ROW[j],buttonEventHandler,100)
	GPIO.setup(COL[j], GPIO.OUT)
	GPIO.output(COL[j], 1)

lcd.clear()
while True:
	lcd.message ('Waiting')
	time.sleep(1)
	lcd.message ('.')
	time.sleep(1)
	lcd.message ('.')
	time.sleep(1)
	lcd.message ('.')
	time.sleep(1)
	lcd.clear()

GPIO.cleanup()


#for j in range (4):
#	GPIO.setup(COL[j], GPIO.OUT)
#	GPIO.output(COL[j], 1)
#
#for i in range (4):
#	print "Init %d pin %d" % ( i , ROW[i])
#	GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
#
#try:
#	while (True):
#		for j in range (4):
#			GPIO.output(COL[j], 0)
#			for i in range (4):
#				if GPIO.input(ROW[i]) == 0:
#					lcd.clear()
#					print MATRIX[i][j]
#					lcd.message ('Key Pressed: %s' % ( MATRIX[i][j]))
#					if MATRIX[i][j] == 'F':
#						sleep(2)
#						lcd.clear()
#					while (GPIO.input(ROW[i]) == 0):
#						pass
#			GPIO.output(COL[j], 1)
#		
#except KeyboardInterupt:
#	GPIO.cleanup()
#

