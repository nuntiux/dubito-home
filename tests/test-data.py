#!/usr/bin/python
# ----------------------------------------------------------------------------
# Samuel Pasquier - samuel@happycoders.org
#
# Raspberry Pi boot-up script
# ----------------------------------------------------------------------------

import sys
import getopt
import json
import random

debug=False

# ----------------------------------------------------------------------------
# Current Value of each Shifters
# ----------------------------------------------------------------------------
shifters= [ ]

# Some Config
NUM_SHIFTER         =   3
NUM_BIT_PER_SHIFTER =   8

# ----------------------------------------------------------------------------
# Turn a relay On
# 0 -> first relay
# ----------------------------------------------------------------------------
def turnRelayOn(relay):
    # Sanity Check
    if ((relay < 0) or (relay >= NUM_SHIFTER * NUM_BIT_PER_SHIFTER)):
        return False
    for i in range (0, NUM_SHIFTER):
        startingBit = i * NUM_BIT_PER_SHIFTER
        if ((relay >= startingBit) and
            (relay < (startingBit + NUM_BIT_PER_SHIFTER))):
            # Find the bit to set
            bit = (relay - (i * NUM_BIT_PER_SHIFTER)) % NUM_BIT_PER_SHIFTER
            # Create bitmask
            bitmask = 0b1 << bit
            shifters[i] |= bitmask
            print "SET %d (shifter:%d, bit:%d, mask:%s) => %s" % (relay, i,
                    bit, bin(bitmask), bin(shifters[i]))
            return True
    return False

# ----------------------------------------------------------------------------
# Turn a relay Off
# 0 -> first relay
# ----------------------------------------------------------------------------
def turnRelayOff(relay):
    # Sanity Check
    if ((relay < 0) or (relay >= NUM_SHIFTER * NUM_BIT_PER_SHIFTER)):
        return False
    for i in range (0, NUM_SHIFTER):
        startingBit = i * NUM_BIT_PER_SHIFTER
        if ((relay >= startingBit) and
            (relay < (startingBit + NUM_BIT_PER_SHIFTER))):
            # Find the bit to set
            bit = (relay - (i * NUM_BIT_PER_SHIFTER)) % NUM_BIT_PER_SHIFTER
            # Create bitmask
            bitmask = 0b1 << bit
            shifters[i] &= ~bitmask
            print "UNSET %d (shifter:%d, bit:%d, mask:%s) => %s" % (relay, i,
                    bit, bin(bitmask), bin(shifters[i]))
            return True
    return False

def switchRelay(relay):
    if ((relay < 0) or (relay >= NUM_SHIFTER * NUM_BIT_PER_SHIFTER)):
        return False
    for i in range (0, NUM_SHIFTER):
        startingBit = i * NUM_BIT_PER_SHIFTER
        if ((relay >= startingBit) and
            (relay < (startingBit + NUM_BIT_PER_SHIFTER))):
            # Find the bit to set
            bit = (relay - (i * NUM_BIT_PER_SHIFTER)) % NUM_BIT_PER_SHIFTER
            # Create bitmask
            bitmask = 0b1 << bit
            if (shifters[i] & bitmask == bitmask):
                shifters[i] &= ~bitmask
            else:
                shifters[i] |= bitmask
            print "UNSET %d (shifter:%d, bit:%d, mask:%s) => %s" % (relay, i,
                    bit, bin(bitmask), bin(shifters[i]))
            return True
    return False

# ----------------------------------------------------------------------------
# Add to sequence
# ----------------------------------------------------------------------------
def createStep(relay, seconds):
    return ({ 'relay': relay, 'seconds': seconds })

# ----------------------------------------------------------------------------
# Usage 
# ----------------------------------------------------------------------------
def printUsage():
    print "%s - Usage" % (__name__)
    print " -d  Turn debug on"
    print " -h  Print this help"

# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------
def main(argv):
    global debug
    try:
        opts, args = getopt.getopt(argv, "hd")
    except getopt.GetoptError:
        printUsage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-d':
            debug = True
            print 'Debug is On'
        elif opt == '-h':
            printUsage()
    # Initialize Shifter
    for i in range(0, NUM_SHIFTER):
        shifters.append(0x0)
    turnRelayOn(1)
    turnRelayOn(7)
    turnRelayOn(11)
    switchRelay(7)
    sequence = []
    sequence.append(createStep(1, random.randrange(1, 240)))
    sequence.append(createStep(3, random.randrange(1, 240)))
    sequence.append(createStep(9, random.randrange(1, 240)))
    matin = { 'name': "matin", 'seq': sequence , 'cron': "fooo" }
    print json.dumps(matin, indent = 4)

# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv[1:])
