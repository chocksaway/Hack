# -*- coding: utf-8 -*-
# (C) Copyright Connected Digital Economy Catapult Limited 2014
import facebook

import pytest
import datetime


def messages():
    HASHTAG_CLOSE = "#drawerofplenty #close"

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

    for each in msgs:
        print (each % (str(123), HASHTAG_CLOSE))


messages()