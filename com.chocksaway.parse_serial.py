__author__ = 'milesd'

import serial

ser = serial.Serial('/dev/tty.usbmodem1412', 9600)
while True:
    print ser.readline()
