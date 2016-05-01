#!/usr/bin/python
# Spawn pseudo-tty for input testing.
# Copyright 2016, Sebastien Lacoste-Seris
# Author: Sebastien Lacoste-Seris (Kaneda)  <sebastien@lacoste-seris.net>
# License: GPLv3
import os, sys, select, pigpio, atexit

# TTY device name (link)
ttyDeviceName = "/dev/ttyTIC"
# RX GPIO port
rxPort=26
pi=None

def exit_handler():
    print 'My application is ending!'
    os.unlink(ttyDeviceName)
    if pi != None:
        pi.bb_serial_read_close(rxPort)
        pi.stop()
    print 'Software serial ended'

atexit.register(exit_handler)
parent, child = os.openpty()
tty = os.ttyname(child)
os.system('stty cs8 -icanon -echo < %s' % (tty))
os.symlink(tty,ttyDeviceName)

print 'Software Serial ' + tty  + ' linked to ' + ttyDeviceName

try:
    print 'Setting up Softserial port'
    pi = pigpio.pi()
    pi.set_mode(rxPort, pigpio.INPUT)
    pi.bb_serial_read_open(RX, 1200, 8)
    print "Teleinfo modem successfully opened"
    
except:
    if pi != None:
        pi.bb_serial_read_close(rxPort)
        pi.stop()
    error = "Error opening Teleinfo modem on PIN '%s' : %s" % (rxPort, traceback.format_exc())
    raise TeleinfoException(error)
    
try:
    running = True
    while running:
        (count, data) = pi.bb_serial_read(rxPort)
        if count > 0:
            os.write(parent, data)
        
finally:
    print 'Ending loop'


