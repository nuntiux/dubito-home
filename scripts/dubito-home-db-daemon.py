#!/usr/bin/python
# ----------------------------------------------------------------------------
# Samuel Pasquier - samuel@happycoders.org
#
# Dubito home Automation - DB daemon 
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

import sys
import getopt
import json
import random
from time import sleep

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
    global debug
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
            if debug:
                print "SET %d (shifter:%d, bit:%d, mask:%s) => %s" % (relay,
                        i, bit, bin(bitmask), bin(shifters[i]))
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
            if debug:
                print "UNSET %d (shifter:%d, bit:%d, mask:%s) => %s" % (relay,
                        i, bit, bin(bitmask), bin(shifters[i]))
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
            if debug:
                print "UNSET %d (shifter:%d, bit:%d, mask:%s) => %s" % (relay,
                        i, bit, bin(bitmask), bin(shifters[i]))
            return True
    return False

# ----------------------------------------------------------------------------
# Add to sequence
# ----------------------------------------------------------------------------
def createStep(relay, seconds):
    return ({ 'relay': relay, 'seconds': seconds })

# ----------------------------------------------------------------------------
# Play a registered sequence
# ----------------------------------------------------------------------------
def playSequence(seq):
    global debug
    if debug:
        print "PLAY SEQUENCE (name:%s, cron:%s)" % (seq["name"], seq["cron"])
    for i in seq["seq"]:
        if debug:
            print "    ITEM (relay:%d, seconds:%d)" %(i["relay"], i["seconds"])
        turnRelayOn(i["relay"])
        sleep(i["seconds"])
        turnRelayOff(i["relay"])


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
    sequence = []
    sequence.append(createStep(1, random.randrange(1, 5)))
    sequence.append(createStep(3, random.randrange(1, 5)))
    sequence.append(createStep(9, random.randrange(1, 5)))
    matin = { 'name': "matin", 'seq': sequence , 'cron': "fooo" }
    print json.dumps(matin, indent = 4)
    playSequence(matin)

# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main(sys.argv[1:])
