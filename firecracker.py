#!/usr/bin/env python3
"""
X10 Firecracker CM17A Interface
"""

#-----------------------------------------------------------
# Copyright (c) 2010-2013 Collin J. Delker
# Copyright (c) 2020 Daniel L. Srebnick (port to python3)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.# 
#-----------------------------------------------------------
#
# NOTES:
#   This software requires the pySerial python module:
#   http://pyserial.sourceforge.net/
#
#   Commands can be sent from the command line or from
#   python scripts by calling send_command().
#
#   X10 Firecracker CM17A protocol specificaiton:
#   ftp://ftp.x10.com/pub/manuals/cm17a_protocol.txt
#
#-----------------------------------------------------------
import sys
import time

# Check for a running instance
import socket

def get_lock(process_name):
   get_lock._lock_socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)

   try:
      get_lock._lock_socket.bind('\0' + process_name)
   except:
      pass

get_lock('firecracker.sock')
while False:
   time.sleep(2)

# Check for serial port or RPi-GPIO support
serial_installed = False
try:
    import serial
    serial_installed = True
except:
    pass

try:
    import RPi.GPIO as GPIO
    serial_installed = True
except:
    pass

if not serial_installed:
    print ('No python serial module installed.')
    raise ValueError

#----------------------------------------------------------
# Constants
#----------------------------------------------------------
__version__ = '0.4'

# Firecracker spec requires at least 0.5ms between bits
DELAY_BIT = 0.001 # Seconds between bits
DELAY_INIT = 0.5  # Powerup delay
DELAY_FIN = 1     # Seconds to wait before disabling after transmit

# House and unit code table
HOUSE_LIST = [
   0x6000, # a
   0x7000, # b
   0x4000, # c
   0x5000, # d
   0x8000, # e
   0x9000, # f
   0xA000, # g
   0xB000, # h
   0xE000, # i
   0xF000, # j
   0xC000, # k
   0xD000, # l
   0x0000, # m
   0x1000, # n
   0x2000, # o
   0x3000  # p
   ]

UNIT_LIST = [
  0x0000, # 1
  0x0010, # 2
  0x0008, # 3
  0x0018, # 4
  0x0040, # 5
  0x0050, # 6
  0x0048, # 7
  0x0058, # 8
  0x0400, # 9
  0x0410, # 10
  0x0408, # 11
  0x0418, # 12
  0x0440, # 13
  0x0450, # 14
  0x0448, # 15
  0x0458  # 16
  ]
MAX_UNIT = 16
    
# Command Code Masks
CMD_ON   = 0x0000
CMD_OFF  = 0x0020
CMD_BRT  = 0x0088
CMD_DIM  = 0x0098

# Data header and footer
DATA_HDR = 0xD5AA
DATA_FTR = 0xAD

# Raspberry Pi GPIO pins. Change to whatever you want to use.
DTR_PIN = 24
RTS_PIN = 25

#----------------------------------------------------------
# Raspberry Pi GPIO class
#----------------------------------------------------------
class RPiGPIO():
    """ Class to emulate serial port using Raspberry Pi GPIO. Only DTR and RTS pins are used. 
        DTR = pin 4 of DB9 serial connector
        RTS = pin 7 of DB9 serial connector
        GND = pin 5 of DB9 serial connector.
        Must use level-shifter to convert RPi's 3.3V output to 5V.
    """
    def __init__( self ):
        GPIO.setmode( GPIO.BCM )
        GPIO.setup( DTR_PIN, GPIO.OUT )
        GPIO.setup( RTS_PIN, GPIO.OUT )

    def setDTR( self, val ):
        GPIO.output( DTR_PIN, val )
    
    def setRTS( self, val ):
        GPIO.output( RTS_PIN, val )

    def close( self ):
        GPIO.cleanup()


#----------------------------------------------------------
# Functions
#----------------------------------------------------------
def set_standby(s):
    """ Put Firecracker in standby """
    s.setDTR(True)
    s.setRTS(True)


def set_off(s):
    """ Turn firecracker 'off' """
    s.setDTR(False)
    s.setRTS(False)


def send_data(s, data, bytes):
    """ Send data to firecracker """
    mask = 1 << (bytes - 1)
    
    for i in range(bytes):
        bit = data & mask
        if bit == mask:
            s.setDTR(False)
        elif bit == 0:
            s.setRTS(False)

        time.sleep(DELAY_BIT)
        set_standby(s)
        time.sleep(DELAY_BIT)      # Then stay in standby at least 0.5ms before next bit
        data = data << 1           # Move to next bit in sequence


def build_command(house, unit, action):
    """ Generate the command word """
    cmd = 0x00000000    
    house_int = ord(house.upper()) - ord('A')

    # Add in the house code
    if house_int >= 0 and house_int <= ord('P') - ord('A'):
        cmd = cmd | HOUSE_LIST[ house_int ]
    else:
        print ("Invalid house code ", house, house_int)
        return

    # Add in the unit code. Ignore if bright or dim command,
    # which just applies to last unit.
    if unit > 0 and unit <= MAX_UNIT:
        if action.upper() != 'BRT' and action.upper() != 'DIM':
            cmd = cmd | UNIT_LIST[ unit - 1 ]
    else:
        print ("Invalid Unit Code", unit)
        return

    # Add the action code
    if action.upper() == 'ON':
        cmd = cmd | CMD_ON
    elif action.upper() == 'OFF':
        cmd = cmd | CMD_OFF
    elif action.upper() == 'BRT':
        cmd = cmd | CMD_BRT
    elif action.upper() == 'DIM':
        cmd = cmd | CMD_DIM
    else:
        print ("Invalid Action Code", action)
        return
    
    return cmd


def send_command( portname, house, unit, action ):
    """ Send Command to Firecracker

    portname: Serial port to send to
    house:    house code, character 'a' to 'p'
    unit:     unit code, integer 1 to 16
    action:   string 'ON', 'OFF', 'BRT' or 'DIM'
    """

    cmd = build_command( house, unit, action )
    if cmd != None:
        try:
            if portname == 'pi':
                s = RPiGPIO()
            else:
                s = serial.Serial(portname)
        except serial.SerialException:
            print ('ERROR opening serial port', portname)
            return False

        set_standby(s)               # Initialize the firecracker
        time.sleep( DELAY_INIT )     # Make sure it powers up
        send_data( s, DATA_HDR, 16 ) # Send data header
        send_data( s, cmd, 16 )      # Send data
        send_data( s, DATA_FTR, 8 )  # Send footer
        time.sleep( DELAY_FIN )      # Wait for firecracker to finish transmitting
        set_off(s)                   # Shut off the firecracker
        s.close()
        return True


#----------------------------------------------------------
# Main Program Entry from Command Line
#----------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 4:
        print ("USAGE:  python firecracker.py house unit action [port]")
        print ("   house  = [a,p]")
        print ("   unit   = [0,16]")
        print ("   action = (ON, OFF, BRT, DIM)")
        print ("   port   = serial port (e.g. COM1 or /dev/tty.usbserial)")
        quit()
        
    house = sys.argv[1]
    unit = int(sys.argv[2])
    action = sys.argv[3]

    try:
        portname = sys.argv[4]
    except:
        #-------------------------------------------------------
        # REPLACE portname with the default serial port your
        # firecracker is connected to. In Windows, this could
        # be "COM1" etc. On Mac/Unix, this will be 
        # '/dev/tty.something'. With my usb-to-serial adapter,
        # it shows up as '/dev/tty.usbserial'.
        #
        # To use Raspberry pi GPIO, use port = 'pi'.
        #-------------------------------------------------------
        portname = '/dev/tty.usbserial'

    send_command( portname, house, unit, action )

