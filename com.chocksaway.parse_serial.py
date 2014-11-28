__author__ = 'milesd'

import serial
import time
import logging
from logging.handlers import SysLogHandler
import os.path
import socket
import re
import facebook
import datetime
import msgman


ser = serial.Serial('/dev/tty.usbmodem1412', 9600)

ts_open = 0.0

syslog_host = '54.77.151.169'
syslog_port = 514
name = "chocolate_drawer"


def configure_syslog():
    """
    Configure syslog logging channel.
    It is turned on by setting `syslog_host` in the config file.
    The port default to 514 can be overridden by setting `syslog_port`.
    """
    if syslog_host:
        handler = SysLogHandler(address=(syslog_host,
                                         syslog_port))

        ip = socket.gethostbyname(socket.gethostname())
        formatter = logging.Formatter(ip + ' ' + name + ' %(message)s')
        handler.setFormatter(formatter)

        logging.getLogger().addHandler(handler)


# This is not currently working
def post_to_facebook():
    graph = facebook.GraphAPI("802501623140662|0C6xaYrHqgjBHNcTEmnxlvx15KE")
    profile = graph.get_object("me")
    friends = graph.get_connections("me", "friends")
    graph.put_object("me", "feed", message="I am writing on my wall!")


def on_open(open_stamp):
    miles = 123
    print ("+++++++++++++++++++++++++++++++++++++++++++++on_open")
    # send a message to Twitter
    msgman.open_message(open_stamp)


def on_close(close_stamp):
    print ("on_close")


logging.info('Starting Chocolate Drawer')

drawer_open = False

# post_to_facebook()

while True:
    ####print ("hello world")

    if ser.readline():
        print("we have input")
        my_val = ser.readline()
        print (my_val)
        if "Drawer NOT Open" in ser.readline() and drawer_open:
            print ("Drawer NOT Open")
            drawer_open = False
            # on_close(time.time())
        elif "Drawer Open" in ser.readline():
            print ("Drawer Open")

            drawer_open = True
            on_open(time.time())

