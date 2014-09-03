#!/usr/bin/python

#
# based on code from lrvick and LiquidCrystal
# lrvic - https://github.com/lrvick/raspi-hd44780/blob/master/hd44780.py
# LiquidCrystal - https://github.com/arduino/Arduino/blob/master/libraries/LiquidCrystal/LiquidCrystal.cpp
#

from time import sleep

class Adafruit_CharLCD:

    # commands
    LCD_CLEARDISPLAY        = 0x01
    LCD_RETURNHOME          = 0x02
    LCD_ENTRYMODESET        = 0x04
    LCD_DISPLAYCONTROL      = 0x08
    LCD_CURSORSHIFT         = 0x10
    LCD_FUNCTIONSET         = 0x20
    LCD_SETCGRAMADDR        = 0x40
    LCD_SETDDRAMADDR        = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT          = 0x00
    LCD_ENTRYLEFT           = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display on/off control
    LCD_DISPLAYON           = 0x04
    LCD_DISPLAYOFF          = 0x00
    LCD_CURSORON            = 0x02
    LCD_CURSOROFF           = 0x00
    LCD_BLINKON             = 0x01
    LCD_BLINKOFF            = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE         = 0x08
    LCD_CURSORMOVE          = 0x00
    LCD_MOVERIGHT           = 0x04
    LCD_MOVELEFT            = 0x00

    # flags for function set
    LCD_8BITMODE            = 0x10
    LCD_4BITMODE            = 0x00
    LCD_2LINE               = 0x08
    LCD_1LINE               = 0x00
    LCD_5x10DOTS            = 0x04
    LCD_5x8DOTS             = 0x00

    def setDebug(self, debug):
        self.debug = debug

    def __init__(self, pin_rs=7, pin_e=8, pins_db=[25, 24, 23, 18], GPIO = None):
        # Emulate the old behavior of using RPi.GPIO if we haven't been given
        # an explicit GPIO interface to use
        if not GPIO:
            import RPi.GPIO as GPIO
        self.GPIO = GPIO
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db
        self.debug = False
        self.lock = False

        self.GPIO.setmode(GPIO.BCM)
        self.GPIO.setup(self.pin_e, GPIO.OUT)
        self.GPIO.setup(self.pin_rs, GPIO.OUT)

        for pin in self.pins_db:
            self.GPIO.setup(pin, GPIO.OUT)
        self.write4bits(0x33) # initialization
        self.write4bits(0x32) # initialization
        self.write4bits(0x28) # 2 line 5x7 matrix
        self.write4bits(0x0C) # turn cursor off 0x0E to enable cursor
        self.write4bits(0x06) # shift cursor right
        self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF
        self.displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS
        self.displayfunction |= self.LCD_2LINE

        """ Initialize to default text direction (for romance languages) """
        self.displaymode =  self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode) #  set the entry mode
        self.numlines = 2
        self.currline = 0
        self.row_offsets = [ 0x00, 0x40, 0x14, 0x54 ]
        self.numcols = 16
        self.curcol = 0
        #0 - Up Char
        self.write4bits(self.LCD_SETCGRAMADDR+0)
        self.write4bits(0b00100, True)
        self.write4bits(0b01110, True)
        self.write4bits(0b11111, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b00100, True)
        #1 - Down
        self.write4bits(self.LCD_SETCGRAMADDR+8)
        self.write4bits(0b00100, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b11111, True)
        self.write4bits(0b01110, True)
        self.write4bits(0b00100, True)
       
        #2 - Right
        self.write4bits(self.LCD_SETCGRAMADDR+16)
        self.write4bits(0b00000, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b00110, True)
        self.write4bits(0b11111, True)
        self.write4bits(0b00110, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b00000, True)
        self.write4bits(0b00000, True)
        
        #3 - Left
        self.write4bits(self.LCD_SETCGRAMADDR+24)
        self.write4bits(0b00000, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b01100, True)
        self.write4bits(0b11111, True)
        self.write4bits(0b01100, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b00000, True)
        self.write4bits(0b00000, True)

        #4 - Off
        self.write4bits(self.LCD_SETCGRAMADDR+32)
        self.write4bits(0b11111, True)
        self.write4bits(0b10001, True)
        self.write4bits(0b10001, True)
        self.write4bits(0b10001, True)
        self.write4bits(0b10001, True)
        self.write4bits(0b10001, True)
        self.write4bits(0b10001, True)
        self.write4bits(0b11111, True)

        #5 - Checked
        self.write4bits(self.LCD_SETCGRAMADDR+40)
        self.write4bits(0b10001, True)
        self.write4bits(0b01010, True)
        self.write4bits(0b01010, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b00100, True)
        self.write4bits(0b01010, True)
        self.write4bits(0b01010, True)
        self.write4bits(0b10001, True)

        #6 - Full
        self.write4bits(self.LCD_SETCGRAMADDR+48)
        self.write4bits(0b00000, True)
        self.write4bits(0b01110, True)
        self.write4bits(0b11111, True)
        self.write4bits(0b11111, True)
        self.write4bits(0b11111, True)
        self.write4bits(0b11111, True)
        self.write4bits(0b01110, True)
        self.write4bits(0b00000, True)

        #7 - 
        self.write4bits(self.LCD_SETCGRAMADDR+56)
        self.write4bits(0b10101, True)
        self.write4bits(0b01010, True)
        self.write4bits(0b10101, True)
        self.write4bits(0b01010, True)
        self.write4bits(0b10101, True)
        self.write4bits(0b01010, True)
        self.write4bits(0b10101, True)
        self.write4bits(0b01010, True)
        self.clear()


    def begin(self, cols, lines):
        if (self.debug):
            print "LCD BEGIN  ==> S"
        if (lines > 1):
            self.numlines = lines
            self.displayfunction |= self.LCD_2LINE
            self.currline = 0
        self.numcols = cols
        self.curcol = 0
        if (self.debug):
            print "LCD BEGIN  ==>  F"
    
    def home(self):
        if (self.debug):
            print "LCD HOME   ==> S"
        self.currline = 0
        self.write4bits(self.LCD_RETURNHOME) # set cursor position to zero
        self.delayMicroseconds(3000) # this command takes a long time!
        if (self.debug):
            print "LCD HOME   ==>  F"
    

    def clear(self):
        if (self.debug):
            print "LCD CLEAR  ==> S"
        if (self.lock):
            print "LCD CLEAR  ==> EXIT"
            return
        self.lock = True
        self.currline = 0
        self.write4bits(self.LCD_CLEARDISPLAY) # command to clear display
        self.delayMicroseconds(3000)    # 3000 microsecond sleep, clearing the display takes a long time
        if (self.debug):
            print "LCD CLEAR  ==>  F"
        self.lock = False

    def setCursor(self, col, row):
        self.row_offsets = [ 0x00, 0x40, 0x14, 0x54 ]
        if ( row > self.numlines ): 
            row = self.numlines - 1 # we count rows starting w/0
        self.write4bits(self.LCD_SETDDRAMADDR | (col + self.row_offsets[row]))
        self.currline = row

    def noDisplay(self): 
        """ Turn the display off (quickly) """
        self.displaycontrol &= ~self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def display(self):
        """ Turn the display on (quickly) """
        self.displaycontrol |= self.LCD_DISPLAYON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def noCursor(self):
        """ Turns the underline cursor on/off """
        self.displaycontrol &= ~self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def cursor(self):
        """ Cursor On """
        self.displaycontrol |= self.LCD_CURSORON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def noBlink(self):
        """ Turn on and off the blinking cursor """
        self.displaycontrol &= ~self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def Blink(self):
        """ Turn on and off the blinking cursor """
        self.displaycontrol |= self.LCD_BLINKON
        self.write4bits(self.LCD_DISPLAYCONTROL | self.displaycontrol)

    def DisplayLeft(self):
        """ These commands scroll the display without changing the RAM """
        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVELEFT)
    
    def scrollDisplayRight(self):
        """ These commands scroll the display without changing the RAM """
        self.write4bits(self.LCD_CURSORSHIFT | self.LCD_DISPLAYMOVE | self.LCD_MOVERIGHT);
    
    def leftToRight(self):
        """ This is for text that flows Left to Right """
        self.displaymode |= self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode);

    def rightToLeft(self):
        """ This is for text that flows Right to Left """
        self.displaymode &= ~self.LCD_ENTRYLEFT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def autoscroll(self):
        """ This will 'right justify' text from the cursor """
        self.displaymode |= self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def noAutoscroll(self): 
        """ This will 'left justify' text from the cursor """
        self.displaymode &= ~self.LCD_ENTRYSHIFTINCREMENT
        self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)

    def write4bits(self, bits, char_mode=False):
        """ Send command to LCD """
        self.delayMicroseconds(2000) # 1000 microsecond sleep
        bits=bin(bits)[2:].zfill(8)
        self.GPIO.output(self.pin_rs, char_mode)
        for pin in self.pins_db:
            self.GPIO.output(pin, False)
        for i in range(4):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i], True)
        self.pulseEnable()
        for pin in self.pins_db:
            self.GPIO.output(pin, False)
        for i in range(4,8):
            if bits[i] == "1":
                self.GPIO.output(self.pins_db[::-1][i-4], True)
        self.pulseEnable()

    def delayMicroseconds(self, microseconds):
        seconds = microseconds / float(1000000)    # divide microseconds by 1 million for seconds
        sleep(seconds)

    def pulseEnable(self):
        self.GPIO.output(self.pin_e, False)
        self.delayMicroseconds(10)        # 1 microsecond pause - enable pulse must be > 450ns 
        self.GPIO.output(self.pin_e, True)
        self.delayMicroseconds(10)        # 1 microsecond pause - enable pulse must be > 450ns 
        self.GPIO.output(self.pin_e, False)
        self.delayMicroseconds(10)        # commands need > 37us to settle


    def message(self, text):
        if (self.debug):
            print "LCD PRINT  ==> S"
        if (self.lock):
            print "LCD PRINT  ==> EXIT"
            return
        self.lock = True
        """ Send string to LCD. Newline wraps to second line"""
        for char in text:
            if char == '\n':
                self.write4bits(0xC0) # next line
            else:
                self.write4bits(ord(char),True)
        if (self.debug):
            print "LCD PRINT  ==>  F"
        self.lock = False

if __name__ == '__main__':
    lcd = Adafruit_CharLCD()
    lcd.clear()
    lcd.message("  Adafruit 16x2\n  Standard LCD")
