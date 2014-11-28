# msgman.py
# Written by BenM, Fri Nov 28 00:28:42 2014
# Copyright (C) 2014 Wordmatter Limited
# All rights reserved.
# $Id: $
# $Log: $

from datetime import datetime
import os, time, random

OPENSTRING = "Draw opened at %s #notsobigdata"
CLOSESTRING = "Draw closed at %s #notsobigdata"
DURATIONSTRING = "Draw was open for %s #notsobigdata"

def gen_tweet_text ():
    """
    Just some random text for tweets.
    """
    ## These are the messages from Mark and Ian
    msgs = ["Customer active!","Uh-oh! Sugar rush alert!","Is it 3pm yet??!",
        "I feel lighter!","Chocolate drops!","Drawer down alert!",
        "Help! Help! Someone's got their hands in my drawers!",
        "Chocolate related innuendo? Let me think",
        "All you need is love. But a little chocolate now and then doesn't hurt",
        "There is nothing better than a friend, unless it is a friend with chocolate",
        "Don't wreck a sublime chocolate experience by feeling guilty",
        "Anything is good if it's made of chocolate",
        "What you see before you, my friend, is the result of a lifetime of chocolate",
        "Look, there's no metaphysics on earth like chocolates",
        '"Draw down"? sounds like 2008!',
        "Oh yeah, there's a chocolate for that",
        "No, it's not 3pm, it's 3am. Where have you been?!",
        "Your drawers or mine?",
        "Hold on, I'm feeling something..."]
        
    return msgs[random.randint(0,len(msgs)-1)]

def open_message (timestamp):
    """
    """
    print OPENSTRING % timestamp

def close_message (timestamp):
    """
    """
    print CLOSESTRING % timestamp

def duration_message (timestamp):
    """
    """
    print DURATIONSTRING % timestamp
        
print gen_tweet_text()
open_message(time.time())
close_message(time.time())

# Authenticated account for:
# DrawerOfPlenty@gmail.com

USER = 'Happy_Drawer'
TWTXT = 'Goodnight from the Drawer of Plenty. Look out for "You light my Xmas tree"...'

def post_a_tweet (user, twtxt):
    """
    Use twtshot to post a tweet.
    """
    #//XX TODO BenM
    # REMEMBER, we are passing this to the shell so quote the twtxt to
    # avoid breaking the command line with bad chars :)
    os.system("python twtshot/twtshot.py --quiet --user=%s --modpath=. --twtxt='%s'" % (user, twtxt.encode("utf-8")))

post_a_tweet(USER, TWTXT) 
