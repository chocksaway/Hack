# oauthlib.py
# Written by BenM, Mon Oct 15 15:52:04 2012
# Copyright (C) 2011 Wordmatter Limited
# All rights reserved.
# $Id: oauthlib.py,v 1.8 2013/05/21 14:14:15 benm Exp $
# $Log: oauthlib.py,v $
# Revision 1.8  2013/05/21 14:14:15  benm
# Tweaks for twt-console. Working component.
#
# Revision 1.7  2013/05/20 17:18:28  benm
# Sync and tidy for twt-console restart.
#
# Revision 1.4  2012/10/26 16:56:36  benm
# Tweaks from twtconsole usage.
#
# Revision 1.3  2012/10/24 13:16:33  benm
# Small tidy for twtcns Twitter Console. Seems to be quite solid :)
#
# Revision 1.2  2012/10/18 08:12:12  benm
# Messy but working ok.
#
# Revision 1.1  2012/10/17 15:47:21  benm
# Baseline commit oauth 1.0A authentication code plus test clients for twitter (authenticate and post update) and BlueVia (get sandbox location).
#

######################################################################
##
## OAuth authentication library - follows oauthtest3.py
##
######################################################################

import sys
import time
import random
import base64
import hashlib
import hmac
import string
import urllib
import types

# Not included in standard distribution
import httplib2

err = [ 'Error: Not implemented',
        'Error: Missing parameters in library call',
        'Error: Failed request returned %s'
        ]

ACCESS_TOKEN = None
ACCESS_TOKEN_SECRET = None

######################################################################
##
## For OAuth 1.0A full handshake a.k.a. "3-legged auth"
##
######################################################################

def maketimestamp() :
    return str(int(time.time()))

def makenonce() :
    '''
    For basic idea see
    http://blog.andydenmark.com/2009/03/how-to-build-oauth-consumer.html.
    Since twitter requires HMAC-SHA1, we may as well use that instead
    of MD5.
    Here, create a random integer string and hash its hexadecimal
    representation with the time to create a unique (enough) one-time
    number
    '''
    rand = ''.join(str(random.randint(0, 9)) for i in range(40))
    return str(hashlib.sha1( str(time.time()) + str(rand)).hexdigest())

def dictquotedstring( dict, sep='&', quotevalues=False) :
    '''
    Return dictionary as a urlquoted string, use defaults to generate
    param string suitable for passing to a signing method. For oauth
    header, curl, etc. use sep=", " and quotevalues=False.
    '''
    s = ''
    for key in sorted(dict.iterkeys()):
        if key and dict[key]: # In case it's None, quoting will fail
            k = urllib.quote( key)
            try:
                v = urllib.quote( dict[key])
            except:
                v = dict[key]
            # Filter empty values
            if v and quotevalues==False:
                s += '%s=%s%s' % ( k,v,sep)
                # " " Quote the value string 
            elif v and quotevalues==True:
                s += '%s="%s"%s' % ( k,v,sep)
    s = s.rstrip( sep)
    #print s
    # Slash "/" in value! %2F?
    s = s.replace('/', '%2F')
    #print s
    return s

def makesignature( sigbase, consumer_secret, token_secret) :
    '''
    Make the signature string, consumer secret MUST be a string,
    token_secret may be ""
    '''
    if not consumer_secret:
        return ''
    if not token_secret: # In case it's None then quoting will fail
        token_secret=''
    sigkey = '%s&%s' % (urllib.quote_plus(consumer_secret),
                            urllib.quote_plus(token_secret))
#    print 'sigkey:'
#    print sigkey
    digest = hmac.new( sigkey, sigbase, hashlib.sha1).digest()
    return base64.encodestring(digest).rstrip()

######################################################################
##
## OAuth 1.0A Signed requests require an oauth parameters dictionary
##
######################################################################

oauth1Aparams = {
    'oauth_consumer_key' : None,
    'oauth_token' : None,
    'oauth_verifier' : None,
    'oauth_nonce' : None,
    'oauth_timestamp' : None,
    'oauth_callback' : None,
    'oauth_signature_method' : 'HMAC-SHA1',
    'oauth_version' : '1.0',
    'oauth_realm' : None
    }

######################################################################
##
## Two methods that construct and send the signed authentication
## requests.
##
## Client must provide the service-specific function to get the
## verifier from a callback URL or oob PIN method, required to get an
## access token for the authenticating user.
##
######################################################################

# Tue May 21 15:12:33 2013
# In use by twt-console.

# Wed Oct 17 11:54:53 2012
# New version, we know this works for authentication, now need to make
# it work for twitter post
def buildsignedrequest( key=None, secret=None, token=None, token_secret=None, verifier=None, requrl=None, callbackurl=None, method=None, opts=None) :
    """
    Generate signature and authentication headers for a signed
    request. The OAuth params are encapsulated in the signature, and
    reproduced in the headers. Return the headers, which should be
    used in the request along with the requrl as passed, and the
    method.

    Used by getoken() and API example calls to BlueVia APIs.
    """
    authparams = oauth1Aparams.copy()
    authparams.update({
        'oauth_consumer_key' : key,
        'oauth_token' : token,
        'oauth_verifier' : verifier,
        'oauth_callback' : callbackurl,
        'oauth_nonce' : makenonce(),
        'oauth_timestamp' : maketimestamp()})

#    print 'Build the signature base string'
#    print 'Building and signing...'

    # Create a new params dict from authparams and opts, like the
    # specification says :)

    # If there are optional parameters
    if opts:
        i = 0
        params = {}
        while i < len( opts):
            # There is only 1 item in each dict in the opts list
            params.update( opts[i])
#        optstring += '%s=%s' % (urllib.quote(o[0]),urllib.quote(o[1]))
            i += 1
#    print optstring

        params.update( authparams)
#        print params
        sigbase = '%s&%s&%s' % ( method, urllib.quote_plus(requrl), urllib.quote_plus( dictquotedstring( params)))

    else:
        # No optional params
        sigbase = '%s&%s&%s' % ( method, urllib.quote_plus(requrl), urllib.quote_plus( dictquotedstring( authparams)))

    # Now make the signature string
    sig = makesignature( sigbase, secret, token_secret)
#    print "Generated signature:"
#    print sig
    # Now add the signature into the authparams
    authparams['oauth_signature']=sig
    # So, that should be all folks?!

    headers = {'Authorization': 'OAuth %s' % dictquotedstring(authparams,sep=", ",quotevalues=True),
               'Content-Type': 'application/x-www-form-urlencoded;charset=UTF8'}
    # DEBUG
#    print "Generated headers:"
#    print headers
    return headers

# ----------
#
# Tue May 21 15:11:15 2013
# Used by twitter console.
#
# ----------

def gettoken( key=None, secret=None, token=None, token_secret=None, verifier=None, requrl=None, callbackurl=None, method=None) :
    """
    Usage:

    For request token require:
    key = consumer key, secret = consumer secret, no token_secret
    callbackurl = 'oob' for PIN, or service provided redirect URL, or
    localhost and extract??

    For access token require:
    key = consumer key, secret = consumer secret
    token/token_secret = request token and secret
    verifier = the code got from getverifier()    
    """
    # Generate the signature and headers needed for a signed
    # request. Pass in the superset of possible parameters. Only the
    # headers are returned, encapsuilating the signature.
    headers = buildsignedrequest( key, secret, token, token_secret, verifier, requrl, callbackurl, method)

    # Use the headers
    response, content = sendrequest( requrl, method, headers=headers)
    #print '???'
    #print response, content
    ### This request expects a 200 response "OK"
    if response['status'] == '200':
        # Unpack JSON result to get the token
        result = {}
        ls = content.split('&')
        for each in ls:
            p = each.split('=')
            result[p[0]] = p[1]
        return result
    else:
        # None instead of json if the response is bad
        print err[2] % response['status']
        exit()

# ----------
#
# Tue May 21 15:11:15 2013
# Used by twitter console.
#
# ----------

def callapi( key=None, secret=None, token=None, token_secret=None, verifier=None, requrl=None, callbackurl=None, method=None, opts=None) :
    """
    Like gettoken() but for generic API requests 
    """
    ## We need to build the optstring exactly as ordered since for
    ## some APIs the order of GET query params is significant
    ## e.g. BlueVia
    optstring = ''
    i = 0
    while i < len( opts):
        optstring += '%s&' % dictquotedstring( opts[i])
        i += 1
    optstring = optstring.rstrip( '&')
#    print 'optstring:'
#    print optstring 

    # Generate the signed header
    # For the header we pass the (ordered) opts list of optional
    # parameter single-item dictionaries
    headers = buildsignedrequest( key, secret, token, token_secret, verifier, requrl, callbackurl, method, opts) #optstring)

    # Now send the request
    # For the request we use the optstring
    if method == 'POST':
        response, content = sendrequest( '%s' % requrl, method, body=optstring, headers=headers)
        return response, content
    elif method == 'GET':
        response, content = sendrequest( '%s?%s' % (requrl, optstring), method, headers=headers)
        return response, content

def sendrequest( url=None, method=None, body=None, headers=None) :
    """
    Use this method to:
    
    request request token
    request access token
    make API requests
    """
    if not url and method:
        return err[1]
#    httplib2.debuglevel = 2
    # Create the http object
    http = httplib2.Http(disable_ssl_certificate_validation=True)
#    print "SEND!"      
    return http.request( url, method=method, body=body, headers=headers)
