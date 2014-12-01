# twtshot.py
# Written by BenM, Thu Dec 26 17:34:45 2013
# Copyright (C) 2013 Wordmatter Limited
# All rights reserved.
# $Id$
# $Log$

# --------------------------------------------------
#
# Xmas 2013 auto tweet project! Quick and dirty please!
#
# --------------------------------------------------

import sys, re, pickle

# LOCAL, library loader func from zijitpylibs, not part of this app
#import libimport
import post, twtauth, twtutils

# LOCAL modules we depend on from twtlibpy
POST = TWTAUTH = TWTUTILS = USERS = TWTXT = ''

APP_NAME = 'twtshot'
USERSFILENAME = 'private/twtshot.dat'

# The folloinwg GLOBALS are set from the command line
QUIET = False; # No stdout or stderr, logging only
AUTHMODE = False # Authentication mode, authenticate a (new) user
USER = '' # twitter account to post to
MODPATH = '.' # Path to twtlibpy folder
LOGFILE = 'twtshot.log' # Logfile is *always* written, quiet or not
TWTXT = 'Blah blah'

# App credentials as set by twitter, see dev.twitter.com zijitengdev
# account.
#Access level		Read and write 
#Request token URL	https://api.twitter.com/oauth/request_token
#Authorize URL		https://api.twitter.com/oauth/authorize
#Access token URL	https://api.twitter.com/oauth/access_token
#Callback URL		None
#Sign in with Twitter	No
CONSUMER_KEY = 'XXXXXXXXX' # <- Removed Mon Dec  1 09:43:27 2014 
CONSUMER_SECRET = 'XXXXXXXXX' # <- Removed

# Twitter endpoints
BASEURL='https://api.twitter.com'
POSTPATH = '/1.1/statuses/update.json'

# The list of authenticated users
AUTHENTICATED = []

def import_local( root):
    '''
    Import local library funcs from this relative root.
    '''
    global POST, TWTAUTH, TWTUTILS, USERS
    # Now import the local libraries we use, all used from this file
#    POST = libimport.importlibfile( '/Users/milesd/workspace/Hack/twtlibpy/post.py')
#    TWTAUTH = libimport.importlibfile( '/Users/milesd/workspace/Hack/twtlibpy/twtauth.py')
#    TWTUTILS = libimport.importlibfile( '/Users/milesd/workspace/Hack/twtlibpy/twtutils.py')
    #//XX TODO BenM
    #Sat Dec 28 14:54:27 2013
    # Not sure about users functionality
    #USERS = libimport.importlibfile( '%s/twtlibpy/users.py' % root)

def usage():
    '''
    Command line usage.
    '''
    print '--quiet Suppress all output'
    print '--authmode Authenticate only' 
    print "--user=<name> Twitter acount to post to"
    print "--modpath=<path> Relative path to twtlibpy modules, default '.'"
    print "--logfile=<file> Name of logfile to write, default 'twtshot.log'"
    print "--twtxt=<post text> Text to post"

def getargs():
    '''
    Get the command line arguments. Args are options of the form
    --option (i.e. flag options) or --option=value. Parse with a regex
    instead of simple splitting to allow "=" also to appear in a value
    e.g. in tweet text.
    '''
    global QUIET, AUTHMODE, MODPATH, USER, LOGFILE, TWTXT
    if len(sys.argv) == 1:
        print 'Please supply arguments to %s:' % APP_NAME
        usage()
        sys.exit(0)
    for arg in sys.argv:
        match = re.match(r'(?:--([a-zA-Z]+)=(.*)|--([a-zA-Z]+))', arg)
        if match:
            #//XX TODO BenM 
            #Sat Dec 28 12:15:03 2013
            # The regex contains 3 groups, 1 and 2 are option=value, 3
            # is option flag
            # Option flags
            if match.group(3) == 'quiet':
                QUIET = True
            elif match.group(3) == 'authmode':
                AUTHMODE = True
            # Option values
            elif match.group(1) == 'modpath':
                MODPATH = match.group(2)
            elif match.group(1) == 'user':
                USER = match.group(2)
            elif match.group(1) == 'logfile':
                LOGFILE = match.group(2)
            elif match.group(1) == 'twtxt':
                TWTXT = match.group(2)
            else:
                print 'Unknown option %s:' % arg
                usage()
                sys.exit(0)
        # No match, error?
        else:
            if arg.replace('.py','') == APP_NAME:
                continue
            else:
                print 'Unknown option %s:' % arg
                usage()
                sys.exit(0)
    #
    #DEBUG!
    if not QUIET:
        print QUIET, AUTHMODE, MODPATH, USER, LOGFILE, TWTXT

def writeuserlist():
    '''
    Write the authenticated users list to file.
    '''
    global QUIET, AUTHENTICATED, USERSFILENAME
    # Only if the list is not empty
    if AUTHENTICATED:
        f = open(USERSFILENAME,'w')
        pickle.dump(AUTHENTICATED, f)
        f.close()
        if not QUIET:
            print 'Wrote users'

def readuserlist():
    '''
    Read the authenticated users list from file.
    '''
    global QUIET, AUTHENTICATED, USERSFILENAME
    f = open(USERSFILENAME,'r')
    AUTHENTICATED = pickle.load(f)
    f.close()
###
### Fri Nov 28 02:52:02 2014
### Sometimes we want to re-write the pickled file see FORCE_USER
###        AUTHENTICATED = FORCE_USER
    if not QUIET:
        print AUTHENTICATED
        print 'users read'            
    
def getuserfromlist( name):
    '''
    Get a user from the authenticated users list
    '''
    global QUIET, AUTHENTICATED
    if AUTHENTICATED == []:
        if not QUIET:
            print 'Oops, no such user found: %s' % name
        return None
    # Otherwise
    for item in AUTHENTICATED:
        if item['screen_name'] == name:
            return item
    if not QUIET:
        print 'Oops, no such user found: %s' % name
        return None
    
def run():
    '''
    Simple main function, execute this and quit. Write errors to an
    error log.
    '''
    global QUIET, AUTHMODE, MODPATH, USER, LOGFILE, TWTXT, AUTHENTICATED
    if not QUIET:
        print 'Running'
    # Read in the saved users list
    readuserlist()
### Fri Nov 28 02:52:02 2014
### Sometimes we want to re-write the pickled file see FORCE_USER
    #    writeuserlist()    
    # Authenticate only
    if AUTHMODE:
        ##This call works okay, returns a complete user id with tokens
        result = twtauth.authenticateaccount( USER, APP_NAME, CONSUMER_KEY, CONSUMER_SECRET)
        AUTHENTICATED.append(result)
        print AUTHENTICATED
        writeuserlist()
        #print AUTHENTICATED
    else:
        user = getuserfromlist(USER)
        if not user:
            return
        ## Tested OK Fri Dec 27 18:21:33 2013
        post.postupdate(appkey=CONSUMER_KEY, appsecret=CONSUMER_SECRET, token=user['oauth_token'], tokensecret=user['oauth_token_secret'], posturl=BASEURL+POSTPATH, msgtext=TWTXT, verbose=0)

def run_direct(noise_level, user, message):
    '''
    Simple main function, execute this and quit. Write errors to an
    error log.
    '''
    global QUIET, AUTHMODE, MODPATH, USER, LOGFILE, TWTXT, AUTHENTICATED
    QUIET = noise_level
    USER = user
    TWTXT = message
    AUTHMODE = False
    if not QUIET:
        print 'Running'
    # Read in the saved users list
    readuserlist()
### Fri Nov 28 02:52:02 2014
### Sometimes we want to re-write the pickled file see FORCE_USER
    #    writeuserlist()    
    # Authenticate only
    if AUTHMODE:
        ##This call works okay, returns a complete user id with tokens
        result = twtauth.authenticateaccount( USER, APP_NAME, CONSUMER_KEY, CONSUMER_SECRET)
        AUTHENTICATED.append(result)
        print AUTHENTICATED
        writeuserlist()
        #print AUTHENTICATED
    else:
        user = getuserfromlist(USER)
        if not user:
            return
        ## Tested OK Fri Dec 27 18:21:33 2013
        #
        post.postupdate(appkey=CONSUMER_KEY, appsecret=CONSUMER_SECRET, token=user['oauth_token'], tokensecret=user['oauth_token_secret'], posturl=BASEURL+POSTPATH, msgtext=TWTXT, verbose=0)

########################################

if __name__=='__main__':
    if not sys.argv :
        sys.exit(-1)
    # Otherwise
    APP_NAME = sys.argv[0].replace('.py','')
    # Update the default config for any command line options
    getargs()
    import_local(MODPATH)
    run() # Do it!
    if not QUIET:
        print "Done.."
    exit(0)

