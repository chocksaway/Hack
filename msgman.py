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

HASHTAG_CLOSE = "#drawerofplenty #close"

HASHTAG_OPEN = "#drawerofplenty #open"

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


def gen_tweet_text():
    """
    Just some random text for tweets.
    """
    ## These are the messages from Mark and Ian

    msgs = ["Customer active %s %s",
            "Uh-oh! Sugar rush alert! %s %s",
            "Is it 3pm yet??! %s %s",
            "I feel lighter! %s %s",
            "Chocolate drops! %s %s",
            "Drawer down alert! %s %s",
            "Help! Help! Someone’s got their Chocolate Fingers in my draws! %s %s",
            "Chocolate related innuendo? Let me think %s %s",
            "Don’t make me get my Snickers in a Twix. Replenish, replenish! %s %s",
            "Hey smarty pants, get your hand out my Smartie draws %s %s",
            "Ooo, I just felt a Ripple of excitement! %s %s",
            "Thank Crunchie it’s Friday! %s %s",
            "Is that Peter? Karney leave the sweets alone? %s %s",
            "Fill me up, Reece’s Peanut Buttercups! %s %s",
            "Don’t be greedy, remember to feed me. %s %s",
            "All you need is love. But a little chocolate now and then doesn't hurt %s %s",
            "There is nothing better than a friend, unless it is a friend with chocolate %s %s",
            "Dont wreck a sublime chocolate experience by feeling guilty %s %s",
            "Anything is good if its made of chocolate %s %s",
            "What you see before you, my friend, is the result of a lifetime of chocolate %s %s",
            "Look, theres no metaphysics on earth like chocolates %s %s",
            '"Draw down"? sounds like 2008! %s %s',
            "Oh yeah, there's a sweetie for that %s %s",
            "No, its not 3pm, its 3am. Where have you been?! %s %s",
            "Your drawers or mine? %s %s",
            "Hold on, Im feeling something... %s %s"]


    return msgs[random.randint(0,len(msgs)-1)]

    #return msgs[0]

    # return "Customer active %s %s"

## Entry
def open_message (timestamp):
    """
    """
    message = gen_tweet_text()
    message = message % (str(timestamp), HASHTAG_OPEN)

    post_a_tweet("Happy_Drawer", message)

    update_excel(timestamp, "OPEN", message)

def close_message (timestamp):
    """
    """

    message = gen_tweet_text()
    message = message % (str(timestamp), HASHTAG_CLOSE)

    post_a_tweet("Happy_Drawer", message)

    update_excel(timestamp, "CLOSE", message)

def duration_message (timestamp):
    """
    """
    print DURATIONSTRING % timestamp



def update_excel(timestamp, event_type, message):
    # testCsvOutput.csv
    my_str = str(time.strftime("%m-%d-%Y")) + "," + str(time.strftime("%H:%M:%S")) + "," + event_type + ",\"" + message + "\"\n"
    print my_str

    with open("/tmp/testCsvOutput.csv", "a") as my_file:
        my_file.write(my_str)