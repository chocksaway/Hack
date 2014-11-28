# msgman.py
# Written by BenM, Fri Nov 28 00:28:42 2014
# Copyright (C) 2014 Wordmatter Limited
# All rights reserved.
# $Id: $
# $Log: $

from datetime import datetime
import os, time, random

import twtshot

OPENSTRING = "Draw opened at %s #notsobigdata"
CLOSESTRING = "Draw closed at %s #notsobigdata"
DURATIONSTRING = "Draw was open for %s #notsobigdata"

HASHTAG = "#drawerofplenty"

def post_a_tweet (user, twtxt):
    """
    Use twtshot to post a tweet.
    """
    #//XX TODO BenM
    # REMEMBER, we are passing this to the shell so quote the twtxt to
    # avoid breaking the command line with bad chars :)
    # os.system("python twtshot/twtshot.py --quiet --user=%s --modpath=. --twtxt='%s'" % (user, twtxt.encode("utf-8")))

    twtshot.run_direct(True, user, twtxt.encode("utf-8"))

    miles = 123


def gen_tweet_text ():
    """
    Just some random text for tweets.
    """
    ## These are the messages from Mark and Ian
    msgs = ["Customer active",# %s %s",
            "Uh-oh! Sugar rush alert! %s %s",
            "Is it 3pm yet??! %s %s",
            "I feel lighter! %s %s",
            "Chocolate drops! %s %s",
            "Drawer down alert! %s %s",
            "Help! Help! Someones got their hands in my drawers! %s %s",
            "Chocolate related innuendo? Let me think %s %s",
            "All you need is love. But a little chocolate now and then doesn't hurt %s %s",
            "There is nothing better than a friend, unless it is a friend with chocolate %s %s",
            "Dont wreck a sublime chocolate experience by feeling guilty %s %s",
            "Anything is good if its made of chocolate %s %s",
            "What you see before you, my friend, is the result of a lifetime of chocolate %s %s",
            "Look, theres no metaphysics on earth like chocolates %s %s",
            '"Draw down"? sounds like 2008! %s %s',
            "Oh yeah, there's a chocolate for that %s %s",
            "No, its not 3pm, its 3am. Where have you been?! %s %s",
            "Your drawers or mine? %s %s",
            "Hold on, Im feeling something... %s %s"]
        
    return #msgs[random.randint(0,len(msgs)-1)]
    return msgs[0]

def open_message (timestamp):
    """
    """
    #drawerofplentty
    #    print OPENSTRING % timestamp
    text = gen_tweet_text()
    print text
    #text = (text % (timestamp, HASHTAG))
    #print text
    post_a_tweet("Happy_Drawer", "What the drawer...")
    
def close_message (timestamp):
    """
    """
    print CLOSESTRING % timestamp

def duration_message (timestamp):
    """
    """
    print DURATIONSTRING % timestamp

        
