#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import * 
from time import sleep, strftime
from datetime import datetime

lcd = Adafruit_CharLCD()

lcd.clear()
lcd.begin(16,1)

lcd.message("Starting GPIO14");
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.OUT)
for j in range (4):
	GPIO.output(2, True)
	lcd.message("On")
	sleep(20)
	GPIO.output(2, False)
	lcd.message("Off")
	sleep(1)
	lcd.clear()




