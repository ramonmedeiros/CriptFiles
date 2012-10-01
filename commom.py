
#
# IMPORTS
#
import os
import sys


#
# CONSTANTS
#
MOUNTS_DIR = '/var/rCrypter'
MOUNTS_FILE = '/var/rCrypter/mounts'


#
# CODE
#
def searchMounts(image):
    """
    Find mounted images

    @type  image: basestring
    @param image: image name
    """
    # read mount files
    file = open(MOUNTS_FILE, 'r')
    data = file.read()
    file.close()
    
    # convert string in dict
    mount = eval(data)

    return mount[image]
# searchMounts()

def recordMount(imagePath, mountpoint):
    """
    Record mounted images

    @type  imagePath: basestring
    @param imagePath: path to image
    """
    # create directory to store mounts
    if os.path.exists(MOUNTS_DIR) == False:
        os.mkdir(MOUNTS_DIR)

    # try to store mount
    try:
        # open file
        file = open(MOUNTS_FILE, 'w')

        # write mount
        mount = { imagePath: mountpoint }

        # write and close
        file.write(str(mount))
        file.close()
    
    # any error: report
    except Exception:
        print "Cannot log mount information."
        sys.exit(1)

    return 0
# recordMount()
