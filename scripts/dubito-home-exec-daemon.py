#!/usr/bin/python
# ----------------------------------------------------------------------------
# Samuel Pasquier - samuel@happycoders.org
# 
# Dubito home Automation
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ----------------------------------------------------------------------------

from subprocess import * 
from time import sleep, strftime
from datetime import datetime
import Queue
import signal
import os
import RPi.GPIO as GPIO
import sys
import getopt
import json

btnBounceTime=400
debug=False

# ----------------------------------------------------------------------------
# Pin Usage
# ----------------------------------------------------------------------------
dataPin=22
latchPin=11
clockPin=9
clearPin=10

# ----------------------------------------------------------------------------
# Shifter Class
# ----------------------------------------------------------------------------
class Shifter():
    global dataPin
    global latchPin
    global clockPin
    global clearPin

    def __init__(self):
        self.pause=0

    def tick(self):
        GPIO.output(clockPin, GPIO.HIGH)
        sleep(0)
        GPIO.output(clockPin, GPIO.LOW)

    def latch(self):
        GPIO.output(latchPin, GPIO.HIGH)
        sleep(0)
        GPIO.output(latchPin, GPIO.LOW)

    def clear(self):
        GPIO.output(clearPin, GPIO.LOW)
        Shifter.latch(self)
        sleep(0.5)
        GPIO.output(clearPin, GPIO.HIGH)

    def setPin(self, pin, value):
        for i in xrange(16, 0, -1):
            if ((value == True) and (i == pin)):
                GPIO.output(dataPin, GPIO.HIGH)
            else:
                GPIO.output(dataPin, GPIO.LOW)
            Shifter.tick(self)
            if ((i != 16) and (i % 8) == 0):
                Shifter.latch(self)
            Shifter.latch(self)

    def setupBoard(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(dataPin, GPIO.OUT)
        GPIO.output(dataPin, GPIO.LOW)
        GPIO.setup(latchPin, GPIO.OUT)
        GPIO.output(latchPin, GPIO.LOW)
        GPIO.setup(clockPin, GPIO.OUT)
        GPIO.output(clockPin, GPIO.LOW)
        GPIO.setup(clearPin, GPIO.OUT)
        GPIO.output(clearPin, GPIO.HIGH)

# ----------------------------------------------------------------------------
# Initialize Global Variables
# ----------------------------------------------------------------------------
# init Shifter
shifter = Shifter()

# ----------------------------------------------------------------------------
# Handler for SIGTERM
# ----------------------------------------------------------------------------
def sigtermHandler(_signo, _stack_frame):
    sys.exit(0)

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main(argv):
    global debug
    
    try:
        opts, args = getopt.getopt(argv, "hd")
    except getopt.GetoptError:
        print ' -d Debug Mode'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-d':
            debug = True
            print 'Debug is On'
        elif opt == '-h':
            sleep(5)
    signal.signal(signal.SIGTERM, sigtermHandler)
    # Init shifter
    shifter.setupBoard()
    for i in range (1, 9):
        sleep(2)
        if debug:
                print "START Relay %d" % (i)
        shifter.setPin(i, True)
        sleep(10)
        if debug:
                print "STOP  Relay %d" % (i)
        shifter.setPin(i, False)
    shifter.clear()

if __name__=="__main__":
    try:
        main(sys.argv[1:])
    finally:
        shifter.clear()
        GPIO.cleanup()
