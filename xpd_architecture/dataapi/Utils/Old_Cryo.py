'''
Copyright (c) 2014 Brookhaven National Laboratory All rights reserved. 
Use is subject to license terms and conditions.

@author: Christopher J. Wright'''
__author__ = 'Christopher J. Wright'

import serial
from struct import *

global cryo_port

RunModes = ("Start up","Start up failed","Start up OK","Run","Set up","Shutdown OK","Shutdown failed")
PhaseIds = ("Ramp", "Cool", "Plat", "Hold", "End", "Purge", "Delete phase", "Load program", "Save program", "Soak", "Wait")
Commands = {'restart':10,'ramp':11,'plat':12,'hold':13,'cool':14,'end':15,'purge':16,'pause':17,'resume':18,'stop':19,'turbo':20}

global portName
portName = '/dev/ttyS0'

def open_cryo_port(port_name):
    global cryo_port

    cryo_port=serial.Serial(port_name,baudrate=9600,bytesize=8,parity='N',stopbits=1,timeout=4.0,xonxoff=0,rtscts=0)
    return cryo_port


def close_cryo_port():
    global cryo_port

    cryo_port.timeout=None
    cryo_port.close()


def cm_output(command):
    global cryo_port

    open_cryo_port(portName)
    cryo_port.write(command)
    close_cryo_port()

"""
def ramp_cool(temp):
  a = int(temp*100.0)
  low_byte = a&255
  d = a>>8
  hi_byte = d&255
  command = chr(6) + chr(Commands["ramp"]) + chr(hi_byte) + chr(low_byte) + chr(hi_byte) + chr(low_byte)
  cm_output(command)
"""

def cs_ramp(ramp_rate, end_temp):
    """Ramp with ramp_rate in K/hour, end temperature in Kelvin"""

    a = int(ramp_rate)
    r_low_byte = a&255
    b = a>>8
    r_hi_byte = b&255

    c = int(end_temp*100.0)
    t_low_byte = c&255
    d = c>>8
    t_hi_byte = d&255

    command = chr(6) + chr(Commands["ramp"]) + chr(r_hi_byte) + chr(r_low_byte) + chr(t_hi_byte) + chr(t_low_byte)
    cm_output(command)

def cs_plat(minutes):
    """Plat duration of minutes"""

    a = int(minutes)
    low_byte = a&255
    d = a>>8
    hi_byte = d&255
    command = chr(4) + chr(Commands["plat"]) + chr(hi_byte) + chr(low_byte)
    cm_output(command)

def cs_cool(temp):
    """Cool to temp degree K"""

    a = int(temp*100.0)
    low_byte = a&255
    d = a>>8
    hi_byte = d&255
    command = chr(4) + chr(Commands["cool"]) + chr(hi_byte) + chr(low_byte)
    cm_output(command)

def send_simple(command_code_string):
    command = chr(2) + chr(Commands[command_code_string])
    cm_output(command)

def cs_restart():
    send_simple('restart')

def cs_stop():
    send_simple('stop')

def cs_purge():
    send_simple('purge')

def cs_hold():
    send_simple('hold')

def cs_pause():
    send_simple('pause')

def cs_resume():
    send_simple('resume')

def cm_input():
    global cryo_port,abort_flag,reading_serial_line

    open_cryo_port(portName)
    response = ""
    c = ''
    i = 0
    while(1):
        try:
            c = cryo_port.read(1)
        except KeyboardInterrupt:
            print "Interrupt caught while reading!\n"
            break
        if (c == ''):
            print "cryo timeout\n"
            break
        if (ord(c) == 32):
            #      print "found start of status\n"
            break
    response = c
    for i in range (0,31):
        c = cryo_port.read(1)
        response = response + c

    close_cryo_port()

    decoded = unpack('BBHHhBBHHHHHBBBBBBHHBB',response)
    print "Gas Set Point = %.2f" %  (swap_short(decoded[2])/100.0)
    print "Gas Temp = %.2f" %  (swap_short(decoded[3])/100.0)
    print "Run Mode = %s" %  (RunModes[decoded[5]])
    print "Phase ID = %s" %  (PhaseIds[decoded[6]])
    print "Ramp rate = %.2f" %  (swap_short(decoded[7]))
    print "Evap temp = %.2f" %  (swap_short(decoded[9])/100.0)
    print "version %.1f" % (decoded[20]/10.0)





def swap_short(a):
    b = a<<8
    c = b&65280
    d = a>>8
    e = d&255
    return c+e



#NOTE ORD IS OPPOSITE CHR

if __name__ == '__main__':
    open_cryo_port("/dev/ttyS0")
    cm_input()
    #ramp_cool(100.0)
    #cool(100.0)
    #send_simple("restart")
    #cm_input()
    close_cryo_port()