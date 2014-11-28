# twtauth.py
# Written by BenM, Wed Oct 24 12:59:52 2012
# Copyright (C) 2011 Wordmatter Limited
# All rights reserved.
# $Id$
# $Log$
# Revision 1.2  2013/05/21 15:23:26  benm
# Project restructure.
#
# Revision 1.1  2012/11/01 21:50:21  benm
# Baseline twitter library used by twt-console.
#

######################################################################
##
## Twitter authentication
##
######################################################################

import sys
import time

# From zijitpylibs, this lives one directory level up in twt-console,
# enables us to import the oauthlib libraries from their expected
# locations.  ./oauthlibpy
import libimport

# Make us location independent e.g. if we want to run from ~/bin
infspec = '..'
infspec = '.'

# Local
# Uses only: oauthlib.gettoken( ..)
oauthlib = libimport.importlibfile( '%s/oauthlibpy/oauthlib.py' % infspec)

# Twitter authentication endpoints
BASEURL='https://api.twitter.com'
REQTOKPATH='/oauth/request_token'
ACCESSTOKPATH='/oauth/access_token'
AUTHPATH='/oauth/authorize' # For PIN

def getpincode( token=None, requrl=None, force=False, user=None) :
    """
    Twitter specific.

    Where token = request token, force forces a twitter login and user
    pre-fills the twitter sign-in name.

    Step 2. Using the request token, request user authorisation to
    access the account, and get the verifier. Construct and redirect
    user to the PIN-based authorisation URL and collect the PIN.
    https://dev.twitter.com/docs/api/1/get/oauth/authorize

    PIN based auth for twitter cf:
    https://dev.twitter.com/docs/auth/pin-based-authorization

    JS sample also at: https://gist.github.com/979955

    This is not a signed request, just a constructed URL and some user
    interactions.
    """
    # Collect optional parameters
    opts = ''
    if force:
        opts = 'force_login=%s&' % force
    if user:
        opts += 'screen_name=%s&' % user
    # Redirect the user. For command-line this is PIN based
    # authorisation
    print '\nPIN authorisation for user', user
    print 'Paste the URL below into your browser and follow instructions to get a PIN code:\n**'
    print '%s?%soauth_token=%s' % (requrl, opts, token)
    #
    pin = raw_input('**\nPlease type in the PIN code >')
    print 'Authenticating with PIN ' + pin
    #Now use the PIN code as the OAuth verifier
    return pin

def authenticateaccount( username, appname, appkey, appsecret) :
    '''
    '''
    print 'Authenticating %s for %s\n**' % (appname, username)
    reqtoken = ''
    reqtokensecret = ''
    # Step 1. OAuth 1.0A - Get a request token
    result = oauthlib.gettoken( key=appkey, secret=appsecret, requrl=BASEURL+REQTOKPATH, callbackurl='oob', method='GET')
    if result and result[ 'oauth_callback_confirmed'] == 'true':
        # Expected result:
        #{'oauth_token_secret': 'blah', 'oauth_token': 'blah', 'oauth_callback_confirmed': 'true'}
        reqtoken = result['oauth_token']
        reqtokensecret = result['oauth_token_secret']

    # Step 2. OAuth 1.0A - Get verifier code, use request token to
    # request user authorisation and get the verifier PIN code
    pin = getpincode( reqtoken, requrl=BASEURL+AUTHPATH, force=True, user=username)

    # Step 3. OAuth 1.0A - Get an access token, using the request
    # token and verifier code
    result = oauthlib.gettoken( key=appkey, secret=appsecret, token=reqtoken, token_secret=reqtokensecret, verifier=pin, requrl=BASEURL+ACCESSTOKPATH, method='GET')
    if result and len( result) == 4:
        return result
    else:
        print 'Failed to return valid USER'
        exit()
