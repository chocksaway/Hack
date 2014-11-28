__author__ = 'milesd'

import serial
import time
import logging
from logging.handlers import SysLogHandler
import os.path
import socket
import re
import facebook



ser = serial.Serial('/dev/tty.usbmodem1412', 9600)

ts_open = None

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


def on_open():
    global ts_open
    print ("on_open")
    ts_open = time.time()
    print ts_open


def on_close():
    print ("on_close")
    ts_close  = time.time() - ts_open
    print ts_close

logging.info('Starting Chocolate Drawer')

drawer_open = False

# post_to_facebook()

while True:
    ####print ("hello world")

    if ser.readline():
        print("we have input")
        my_val = ser.readline()
        print (my_val)
        if "Button NOT pushed" in ser.readline() and drawer_open:
            drawer_open = False
            on_close()
        elif "Button pushed" in ser.readline():
            drawer_open = True
            on_open()

