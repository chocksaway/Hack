# post.py
# Written by BenM, Wed Oct 24 13:53:08 2012
# Copyright (C) 2011 Wordmatter Limited
# All rights reserved.
# $Id$
# $Log$
# Revision 1.4  2013/06/22 17:13:15  benm
# Tweaks for Python 2.7 test.
#
# Revision 1.3  2013/05/22 15:21:06  benm
# Fix for posting, this is now a working tool :)
#
# Revision 1.2  2013/05/21 15:23:26  benm
# Project restructure.
#
# Revision 1.1  2012/11/01 21:50:21  benm
# Baseline twitter library used by twt-console.
#

######################################################################
##
## Post to twitter
##
######################################################################

# From zijitpylibs, this lives one directory level up in twt-console,
# enables us to import the oauthlib libraries from their expected
# locations.  ./oauthlibpy
import libimport

# Make us location independent e.g. if we want to run from ~/bin
infspec = '..'
infspec = '.'

# Local
# Uses: oauthlib.callapi( ..)  
oauthlib = libimport.importlibfile( '%s/oauthlibpy/oauthlib.py' % infspec)
twtutils = libimport.importlibfile( '%s/twtlibpy/twtutils.py' % infspec)

# Fri Dec 27 18:25:11 2013
# Added verbose flag
def postupdate( appkey=None, appsecret=None, token=None, tokensecret=None, posturl=None, msgtext=None, verbose=5 ) :
    # Optional parameters, use a list not a dictionary to we can
    # control the order
    # For POST opts are the body
    # For GET opts are the ?<params> query parameters

    # Warn if message is being truncated. truncate() only truncates if
    # too long
    if len( msgtext) > 140:
        # Fri Dec 27 18:25:11 2013
        # Only in verbose mode
        if verbose: print 'Too long, truncating):'
    txt, l = twtutils.truncate( msgtext ) # Returns a pair
    # Fri Dec 27 18:25:11 2013
    # Only in verbose mode
    if verbose:
        print 'Post: (%s) %s' % (l, txt)
        confirm = raw_input('Please confirm post [y | n]:\n')
        if not confirm == 'y':
            print 'Cancelled...'
            return

    optparams = [{'status' : txt}]
    ###
    response, content = oauthlib.callapi( key=appkey, secret=appsecret, token=token, token_secret=tokensecret, requrl=posturl, method='POST', opts=optparams)
    if verbose:
        if response['status'] == '200':
            print 'Posted'
        else:
            print 'Oops, got an error %s' % response['status']
            print response, content


