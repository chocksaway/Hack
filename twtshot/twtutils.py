# twtutils.py
# Written by BenM, Wed Oct 24 18:23:20 2012
# Copyright (C) 2011 Wordmatter Limited
# All rights reserved.
# $Id$
# $Log$

######################################################################
##
## My usefuls
##
######################################################################

import time

def pause():
    time.sleep(1)

def truncate( msgtext='', maxlen=None ) :
    """
    Truncate a tweet text to some length if the untruncated tweet will
    exceed that length. Return (text, length)
    """
    if not maxlen:
        maxlen = 140
    l = len( msgtext)
    if l > maxlen:
        return ( '%s...' % msgtext[ 0: maxlen-3], maxlen)
    else:
         return msgtext, l

######################################################################
##
## Set functions from
## http://www.saltycrane.com/blog/2008/01/how-to-find-intersection-and-union-of/
##
######################################################################

def unique(a):
    """ return the list with duplicate elements removed """
    return list(set(a))

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))
     
