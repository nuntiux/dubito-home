#!/usr/bin/python
# ----------------------------------------------------------------------------
# Samuel Pasquier - samuel@happycoders.org
# 
# Dubito home  Automation
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

from Adafruit_CharLCD import Adafruit_CharLCD
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
doorCheckPin=14
btnU=17
btnD=2
btnR=27
btnL=3
btnOk=4
btnDoor=14 # 14 & 15 are unused today

# ----------------------------------------------------------------------------
# Shifter Class
# ----------------------------------------------------------------------------
class Shifter():
    global dataPin
    global latchPin
    global clockPin
    global clearPin

    def __init__(self):
        self.setupBoard()
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
# init LCD
lcd = Adafruit_CharLCD()
# init LCD Queue message
lcdQueue = Queue.Queue()
# init Shifter
shifter = Shifter()

# ----------------------------------------------------------------------------
# lcdPrint
# ----------------------------------------------------------------------------
def lcdPrint(text):
    lcdQueue.put(text)

# ----------------------------------------------------------------------------
# Utilities function
# ----------------------------------------------------------------------------
def runCmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output.replace("\n", "")

# ----------------------------------------------------------------------------
# Menu
# ----------------------------------------------------------------------------
class MenuItem():
    def __init__(self, name, parent, action, relay):
        self.name = name
        self.menuList = []
        self.parent = parent
        self.menuPos = 0
        self.action = action
        self.relay = relay
        self.state = False

    #
    # Handle Navigation thru menu
    #
    def menuUp(self):
        if (self.menuPos > 0):
            self.menuPos -= 1
        # refresh
        if (self.action is not None):
            self.action()
        else:
            self.displayMenu()

    def menuDown(self):
        if (self.menuPos < (len(self.menuList) - 1)):
            self.menuPos += 1
        # refresh
        if (self.action is not None):
            self.action()
        else:
            self.displayMenu()

    def menuEnter(self):
        global menuCurrent
        if (self.menuPos < len(self.menuList)):
            menuCurrent = self.menuList[self.menuPos]
            menuCurrent.refreshDisplay()
        elif self.relay is not None:
            shifter.setPin(self.relay, not self.state)
            self.state = not self.state
            if (self.action is not None):
                self.action()

    def menuLeft(self):
        global menuCurrent
        if (self.parent is not None):
            menuCurrent = self.parent
        menuCurrent.displayMenu()

    def menuRight(self):
        self.menuEnter()

    #
    # refresh the current display
    #
    def refreshDisplay(self):
        # If there is an action function, just run it
        if (self.action is not None):
            self.action()
        else:
            # it might be a submenu
             self.displayMenu()

    #
    # Display the current menu and hightlight the position in the menu
    #
    def displayMenu(self):
        lcdPrint("CLEAR")
        if (len(self.menuList) > 0):
            if (self.menuPos % lcd.numlines == 0):
                for j in range (self.menuPos, self.menuPos + lcd.numlines):
                    if  (j < len(self.menuList)):
                        lcdPrint('%s %s\n' %
                                ("\2" if j == self.menuPos else " ",
                                    self.menuList[j].name))
            else:
                tmp = (self.menuPos / lcd.numlines) * lcd.numlines
                for j in range (tmp, tmp + lcd.numlines):
                    if  (j < len(self.menuList)):
                        lcdPrint('%s %s\n' %
                                ("\2" if j == self.menuPos else " ",
                                    self.menuList[j].name))

    #
    # Add a submenu
    #
    def appendMenu(self, newMenu):
        newMenu.menuPos = len(self.menuList)
        self.menuList.append(newMenu)

# ----------------------------------------------------------------------------
# Action Menu
# ----------------------------------------------------------------------------
def networkAction():
    lcdPrint("CLEAR")
    # Ping google
    cmd = "ping -c 1 www.google.com 2>&1 | grep packet | cut -d, -f3 | " \
          "sed 's/packet //g' "
    lcdPrint("PING:%s\n" % (runCmd(cmd)))
    # Get IP address
    cmd = "ip addr show wlan0 | grep inet | grep -v inet6 | " \
          "awk '{print $2}' | cut -d/ -f1 "
    lcdPrint("IP:%s" %(runCmd(cmd)))

# ----------------------------------------------------------------------------
# Status Menu
# ----------------------------------------------------------------------------
def statusAction():
    lcdPrint("CLEAR")
    cmd = "uptime | cut -d , -f 1| sed 's/.*up //g'"
    lcdPrint("U\2 %s\n" %(runCmd(cmd)))
    cmd = "uptime | sed 's/.*average: //g' | cut -d, -f 1,2"
    lcdPrint("L\2 %s" %(runCmd(cmd)))

# ----------------------------------------------------------------------------
# Garage Menu
# ----------------------------------------------------------------------------
def garageAction():
    lcdPrint("CLEAR")
    lcdPrint("Status: %s\n" % ("Closed" if GPIO.input(doorCheckPin) else
        "Open"))
    lcdPrint("Press \6 or \2")

# ----------------------------------------------------------------------------
# Generic function to switch relay
# ----------------------------------------------------------------------------
def switchMenu():
    global menuCurrent
    lcdPrint("CLEAR")
    lcdPrint("%s:%s\n" %(menuCurrent.name, "On" if menuCurrent.state else 
        "Off"))
    lcdPrint("Press \6 or \2")

# ----------------------------------------------------------------------------
# Menu Definition
# ----------------------------------------------------------------------------
menu = MenuItem("Main", None, None, None)

# -----------------
# Watering
menuWatering = MenuItem("Watering", menu, None, None)
# Manual Watering
menuWaterManual = MenuItem("Manual", menuWatering, None, None)
menuWaterManual.appendMenu(MenuItem("Lawn Front 1", menuWaterManual,
    switchMenu, 1))
menuWaterManual.appendMenu(MenuItem("Lawn Front 2", menuWaterManual,
    switchMenu, 2))
menuWaterManual.appendMenu(MenuItem("Lawn Right", menuWaterManual,
    switchMenu, 3))
menuWaterManual.appendMenu(MenuItem("Lawn Center", menuWaterManual,
    switchMenu, 4))
menuWaterManual.appendMenu(MenuItem("Lawn Side", menuWaterManual,
    switchMenu, 5))
menuWaterManual.appendMenu(MenuItem("Garden Beds", menuWaterManual,
    switchMenu, 6))
menuWaterManual.appendMenu(MenuItem("Fruits Trees", menuWaterManual,
    switchMenu, 7))
menuWaterManual.appendMenu(MenuItem("Mint", menuWaterManual,
    switchMenu, 8))
menuWatering.appendMenu(menuWaterManual)
# Automatic Watering
menuWatering.appendMenu(MenuItem("Automatic Settings", menuWatering, None, None))
# Watering Status
menuWatering.appendMenu(MenuItem("Status", menuWatering, None, None))
menu.appendMenu(menuWatering)

# -----------------
# Garage Door
menu.appendMenu(MenuItem("Garage Door", menu, garageAction, 9))
# -----------------
# Network
menu.appendMenu(MenuItem("Network", menu, networkAction, None))
# -----------------
# Status
menu.appendMenu(MenuItem("Status", menu, statusAction, None))


menuCurrent = menu

# ----------------------------------------------------------------------------
# Button Handler from interrupt
# ----------------------------------------------------------------------------
def buttonEventHandlerU (pin):
    global debug

    if (debug):
        print "KEYBOARD  ==> Up"
    menuCurrent.menuUp()

def buttonEventHandlerD (pin):
    if (debug):
        print "KEYBOARD  ==> Down"
    menuCurrent.menuDown()

def buttonEventHandlerR (pin):
    if (debug):
        print "KEYBOARD  ==> Right"
    menuCurrent.menuRight()

def buttonEventHandlerL (pin):
    if (debug):
        print "KEYBOARD  ==> Left"
    menuCurrent.menuLeft()

def buttonEventHandlerOk (pin):
    if (debug):
        print "KEYBOARD  ==> Ok"
    menuCurrent.menuEnter()

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
            lcd.setDebug(True)
            print 'Debug is On'
        elif opt == '-h':
            sleep(5)
    signal.signal(signal.SIGTERM, sigtermHandler)
    lcd.begin(16,2)
    lcd.clear()
    lcd.message('BOOTING')
    # tell the GPIO module that we want to use the chip's pin numbering
    # scheme
    GPIO.setmode(GPIO.BCM)
    lcd.message('.')
    #GPIO.setwarnings(False)
    # Init shifter
    shifter.setupBoard()
    shifter.clear()
    # setup btn pin as an input
    lcd.message('.')
    GPIO.setup(btnU, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btnD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btnR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btnL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btnOk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(doorCheckPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    lcd.message('.')
    GPIO.add_event_detect(btnU, GPIO.FALLING, callback=buttonEventHandlerU,
            bouncetime=btnBounceTime)
    GPIO.add_event_detect(btnD, GPIO.FALLING, callback=buttonEventHandlerD,
            bouncetime=btnBounceTime)
    GPIO.add_event_detect(btnR, GPIO.FALLING, callback=buttonEventHandlerR,
            bouncetime=btnBounceTime)
    GPIO.add_event_detect(btnL, GPIO.FALLING, callback=buttonEventHandlerL,
            bouncetime=btnBounceTime)
    GPIO.add_event_detect(btnOk, GPIO.FALLING, callback=buttonEventHandlerOk,
            bouncetime=btnBounceTime)
    lcd.message('.')
    menuCurrent.displayMenu()
    running = True
    while running == True:
        try:
            while not lcdQueue.empty():
                msg = lcdQueue.get()
                if (msg == "CLEAR"):
                    lcd.clear()
                else:
                    lcd.message(msg)
            sleep(0.3)
            # Refresh the display in case something went wrong
            if (debug):
                print 'REFRESH   ==> %s ' % menuCurrent.name
            #lcd.noDisplay()
            #lcd.display()
            #menuCurrent.refreshDisplay()
        except KeyboardInterrupt:
            running = False

if __name__=="__main__":
    try:
        main(sys.argv[1:])
    finally:
        lcd.clear()
        lcd.message('GOING DOWN...\n')
        shifter.clear()
        lcd.message('Daemon killed')
        GPIO.cleanup()


