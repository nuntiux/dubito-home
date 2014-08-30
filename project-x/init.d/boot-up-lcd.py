#!/usr/bin/python
# ----------------------------------------------------------------------------
# Samuel Pasquier - samuel@happycoders.org
# 
# Raspberry Pi boot-up script
# ----------------------------------------------------------------------------

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import * 
from time import sleep, strftime
from datetime import datetime
import RPi.GPIO as GPIO
import sys
import getopt

btnBounceTime=200
debug=False

# ----------------------------------------------------------------------------
# Pin Usage
# ----------------------------------------------------------------------------
dataPin=22
latchPin=11
clockPin=9
clearPin=10
btnU=17
btnD=2
btnR=27
btnL=3
btnOk=4
btnDoor=14 # 14 & 15 are unused today

# init LCD
lcd = Adafruit_CharLCD()

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
        sleep(1)
        GPIO.output(clearPin, GPIO.HIGH)

    def setPin(self,value):
        for i in xrange(16, 0, -1):
            if (i == value):
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

shifter=Shifter()

# ----------------------------------------------------------------------------
# Button Handler
# ----------------------------------------------------------------------------
def buttonEventHandlerU (pin):
    print "Button U Pressed"
    lcd.clear()
    lcd.message('Button U Pressed')
    shifter.setPin(1)

def buttonEventHandlerD (pin):
    print "Button D Pressed"
    lcd.clear()
    lcd.message('Button D Pressed')
    shifter.setPin(2)

def buttonEventHandlerR (pin):
    print "Button R Pressed"
    lcd.clear()
    lcd.message('Button R Pressed')
    shifter.setPin(3)

def buttonEventHandlerL (pin):
    print "Button L Pressed"
    lcd.clear()
    lcd.message('Button L Pressed')
    shifter.setPin(4)

def buttonEventHandlerOk (pin):
    print "Button Ok Pressed"
    lcd.clear()
    lcd.message('Button Ok Pressed')
    shifter.setPin(5)


# ----------------------------------------------------------------------------
# Utilities function
# ----------------------------------------------------------------------------
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hd")
    except getopt.GetoptError:
        print ' -d Debug Mode'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-d':
            debug = True
            print 'Debug is On'

    # Get IP address
    cmd = "ip addr show wlan0 | grep inet | grep -v inet6 | " \
          "awk '{print $2}' | cut -d/ -f1"
    lcd.begin(16,1)
    lcd.clear()
    lcd.message('BOOTING...')
    sleep(2)
    lcd.clear()
    ipaddr = run_cmd(cmd)
    lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
    lcd.message('%s' % ( ipaddr ) )

    # tell the GPIO module that we want to use the chip's pin numbering
    # scheme
    GPIO.setmode(GPIO.BCM)
    #GPIO.setwarnings(False)
    # Init shifter
    shifter.setupBoard()
    shifter.clear()
    # setup btn pin as an input
    GPIO.setup(btnU, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btnD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btnR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btnL, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(btnOk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
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
    
    running=True
    while running==True:
        try:
            if (debug):
                print '...waiting...'
            sleep(2)
        except KeyboardInterrupt:
		    running=False
		    shifter.clear()
    GPIO.cleanup()

if __name__=="__main__":
    main(sys.argv[1:])


