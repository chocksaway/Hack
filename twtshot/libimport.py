# libimport.py
# Written by BenM, Sun Apr 21 18:22:43 2013
# Copyright (C) 2011 Wordmatter Limited
# All rights reserved.
# $Id$
# $Log$
# Revision 1.1  2013/05/21 17:11:18  benm
# First commit.
#
# Revision 1.1  2013/05/14 12:13:48  benm
# First commit.
#

# --------------------------------------------------
#
# Copy this file locally and import this fixed method to enable
# scripst to import local modules from arbitrrarty locations e.g. so
# we can put all imported files into a project-specific lib folder.
#
# Usage example:
# import libimport
#
# # Import the local libraries we use, or exit
# ripfuncs = importlibfile( 'libs/ripwithparanoid.py')
#
# --------------------------------------------------

# Fri Apr 12 17:50:53 2013
# Import the modules as we want to
import os, imp

def importlibfile( filespec):
    '''
    Import local modules from files, see
    http://code.activestate.com/recipes/159571-importing-any-file-without-modifying-syspath/
    '''
    (path, name) = os.path.split( filespec)
    (name, ext) = os.path.splitext( name)
    file = None
    try:
        (file, filename, data) = imp.find_module( name, [path])
    except:
        print 'Failed loading %s from %s' % (name, path)
    finally:
        if not file == None:
            return imp.load_module(name, file, filename, data)
    return False

####################
