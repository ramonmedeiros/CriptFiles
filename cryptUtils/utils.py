#!/usr/bin/python

#
# IMPORTS
#
from M2Crypto import DSA
from M2Crypto import RSA

import os
import sys
#
# CONSTANTS
#
BLOCKSIZE_CRYPT = { 1024:64, 512:16}
BLOCKSIZE_DECRYPT = { 1024:128, 512:32} 
HOME_DIR = os.environ.get('HOME')
CRYPTER_DIR = HOME_DIR + '/.rCrypter'
PRIVATE_KEY = CRYPTER_DIR + '/key.priv'


#
# CODE
#
def checkrCrypterFiles():
    """
    Verifies if keys and rCrypter directory is available and report algorithm used

    @rtype: basestring
    @returns: algorithm used on keys
    """
    # rCrypter directory does not exists: create it
    if not os.path.exists(CRYPTER_DIR):
        os.mkdir(CRYPTER_DIR)

    # key exists: report algorithm
    if os.path.exists(PRIVATE_KEY):
        
        # open file
        key = open(PRIVATE_KEY, 'r')
        data = key.read()

        # key is RSA: report
        if 'RSA' in data:
            return 'RSA'

        # key is DSA: report
        elif 'DSA' in data:
            return 'DSA'
        
        # private key not recognized: report
        else:
            print "Key not recognized. Aborting"
            sys.exit(1)

# checkrCrypterFiles()

def createKeys(algorithm, size):
    """
    Creates a private and public key
    
    @type  algorithm: basestring
    @param algorithm: algorithm name

    @type  size: int
    @param path: size of keys
    
    @rtype: int
    @returns: exit status
    """
    # rCrypter directory does not exists: create it
    if not os.path.exists(CRYPTER_DIR):
        os.mkdir(CRYPTER_DIR)

    # key already exists: ask if user want to create a new one
    if os.path.exists(PRIVATE_KEY):
        print "Key already exists. Do you want to create a new one?"
        answer = raw_input('(Y/N)')

        # user does not pretend to create a new one: abort
        if answer.uppercase() == 'N':
            return 0

    # create keys
    privateKey = eval(algorithm).gen_key(size, 65537)
    
    # try to save key
    try:
        privateKey.save_key(PRIVATE_KEY)

    # issue to save keys: report
    except Exception:
        print "Cannot save keys. Aborting."
        sys.exit(1)
    
    return 0
# createKey()

def cryptImage(path, key):
    """
    Encrypts a image

    @type  path: basestring
    @param path: path to image

    @type  key: dict
    @param key: pair of keys

    @rtype: int
    @returns: exit status
    """
    # image doesn't exists: abort
    if os.path.exists(path) == False:
        print "Image not found. Aborting."
        sys.exit(1)

    # key doesn't exists: ask to create one
    if os.path.exists(PRIVATE_KEY) == False:
        print "Key doesn't exists. Create it."
        sys.exit(1)

    # try to crypt image
    try:

        # rename and open images
        newPath = '.' + path
        os.rename(path, newPath)
        image = open(newPath, 'r')
        newImage = open(path, 'a')
    
        # get blocksize
        size = BLOCKSIZE_CRYPT[key.__len__()]

        # read file until EOF
        while True:
        
            # read blocksize
            data = image.read(size)
        
            # data is empty: end of file
            if data == "":
                break

            # crypt image
            cryptedText = key.public_encrypt(data, RSA.pkcs1_oaep_padding)

            # write new image
            newImage.write(cryptedText)
    
        # close image and delete old one
        image.close()
        newImage.close()
        os.remove(newPath)
    
    # any problem: abort
    except Exception:
        print "Image cannot be crypted. Aborting"
        sys.exit(1)

    # return success
    return True
# cryptImage()

def loadKey():
    """
    Reads the key

    @rtype: object
    @returns: key object on success
    """
    # check keys
    algorithm = checkrCrypterFiles()

    # try to read keys
    try:
        private = eval(algorithm).load_key(PRIVATE_KEY)

    # any problem: report
    except Exception:
        print "The key cannot be loaded. Aborting."
        sys.exit(1)

    # return pair of keys
    return private
# loadKeys()

def decryptImage(path, key):
    """
    Decrypt image

    @type  path: basestring
    @param path: path to image

    @type  key: object
    @param key: key instance

    @rtype: int
    @returns: exit status
    """ 
    # image doesn't exists: abort
    if os.path.exists(path) == False:
        print "Image not found. Aborting."
        sys.exit(1)

    # try to decrypt image
    try:

        # rename and open images
        newPath = '.' + path
        os.rename(path, newPath)
        image = open(newPath, 'r')
        newImage = open(path, 'a')
        
        # get blocksize
        size = BLOCKSIZE_DECRYPT[key.__len__()]

        # decrypt image
        while True:
        
            # read data
            data = image.read(size)
     
            # data is empty: end of file
            if data == "":
                break

            # crypt image
            cryptedText = key.private_decrypt(data, RSA.pkcs1_oaep_padding)

            # append to new image
            newImage.write(cryptedText)

        # close image and remove old one
        image.close()
        newImage.close()
        os.remove(newPath)
    
    # any problem: abort
    except Exception:
        print "Image cannot be crypted. Aborting."
        sys.exit(1)

    # return success
    return True
# decryptImage()
