__author__ = 'milesd'

import serial
import time

ben = True

ser = serial.Serial('/dev/tty.usbmodem1412', 9600)

ts_open = None

def on_open():
    global ts_open
    print ("on_open")
    ts_open = time.time()
    print ts_open


def on_close():
    print ("on_close")
    #ts_close  = time.time() - ts_open
    #print ts_close


drawer_open = False

while True:
    ####print ("hello world")

    if ser.readline() :
        print("we have input")
        my_val = ser.readline()
        print (my_val)
        if "Button pushed" in my_val:
            drawer_open = True
            on_open()
        elif "Button NOT pushed" in my_val and drawer_open:
            drawer_open = False
            on_close()
