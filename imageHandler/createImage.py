#!/usr/bin/python

#
# IMPORTS
#
import os
import time
import sys


#
# CONSTANTS
#
DD_COMMAND = 'dd if=/dev/zero of=%s bs=1024 count=%d > /dev/null'
INITIAL_SIZE = 500
MAKE_EXT3 = 'mkfs -t ext3 -F %s > /dev/null'


#
# CODE
#
def createImage(path):
    """
    Creates a base image
    
    @type  path: basestring
    @param path: path to image
    """
    # file already exists: abort
    if os.path.exists(path):
        print "This file already exists, aborting."
        sys.exit(1)        

    # try to create image
    try:
        file = open(path, 'w')
        file.close()

    # file cannot be created: abort
    except OSError:
        print "The image already exists, aborting."
        sys.exit(2)

    # allocate 10M for initial space
    try:
        
        # store 10MB
        args = str(DD_COMMAND % (path, INITIAL_SIZE))
        cmd = os.popen(args)
        cmd.close()

        # wait
        time.sleep(1)

        # create ext3
        args = str(MAKE_EXT3 % path)
        cmd = os.popen(args)
        cmd.close()

    # cannot create ext3 image: abort
    except OSError:
        print "The image cannot be created, aborting."
        sys.exit(3)

   
   # TODO: crypt image
# createImage()


