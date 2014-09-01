#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import * 
from time import sleep, strftime
from datetime import datetime

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT, GPIO.LOW)
GPIO.output(4, GPIO.HIGH)
time.sleep(2)
GPIO.output(4, GPIO.LOW)

GPIO.cleanup()


