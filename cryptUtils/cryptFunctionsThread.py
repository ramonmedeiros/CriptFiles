
#
# IMPORTS
#
from threading import Thread

import time
import sys


#
# CONSTANTS
#


#
# CODE
#

class CrypterThread(Thread):
    """
    Reads a file and put in a list
    """

    def __init__(self, dataDict, file, blocksize, start, end, cryptMethod):
        """
        Constructor
        
        @type  dataDict: dict
        @param dataDict: dict with data

        @type  file: basetring
        @param file: path to file

        @type  blocksize: int
        @param blocksize: size of block

        @type  start: int
        @param start: block to start operation

        @type  end: int
        @param end: block to end operation

        @type  cryptMethod: method
        @param cryptMethod: crypt method

        @rtype: None
        @returns: Nothing
        """
        # call parent
        Thread.__init__(self)

        # store vars
        self.__dataDict = dataDict
        self.__file = file
        self.__blocksize = blocksize
        self.__start = start
        self.__end = end
        self.__cryptMethod = cryptMethod
    # __init__()

    def run(self):
        """
        Run thread
        
        @rtype: None
        @returns: Nothing
        """
        # try to read file
        try:

            # set counter
            counter = self.__start
            
            # open file
            file = open(self.__file, 'r')

            # read file
            while True:
                
                # counter out of interval: break
                if counter > self.__end:
                    break
                
                # go to block
                blockPointer = self.__blocksize * counter
                file.seek(blockPointer, 0)

                # get data
                data = file.read(self.__blocksize)

                # crypt data
                self.__dataDict[counter] = self.__cryptMethod(data, 4)

                # increment counter
                counter += 1
		
        # any problem: abort
        except Exception, e:
            print e
            print "Problem while crypting file. Aborting."
            sys.exit(1)
    # run()

# CrypterThread()

class WriterThread(Thread):
    """
    Thread that writes in a file
    """

    def __init__(self, file, dict, blocksize):
        """
        Constructor

        @type  file: basestring
        @param file: path to file

        @type  dict: dict
        @param dict: dict with data to be write
 
        @type  blocksize: int
        @param blocksize: size of block
       
        @rtype: None
        @returns: Nothing
        """
         # call parent
        Thread.__init__(self)

        # store list and file
        self.__dict = dict
        self.__file = file
        self.__blocksize = blocksize
        self.__wait = False
    # __init__()

    def run(self):
        """
        Writes the output file

        @rtype:  None
        @returns: Nothing
        """
        # try to read file
        try:
            
            # open
            file = open(self.__file, 'w')

            # read file
            while True:

                # list is empty: abort
                if len(self.__dict) == 0:
                    
                    # wait reader
                    time.sleep(0.0001)
                    self.__wait == True
                    
                    # 3 tries: break
                    if self.__wait:
                        break

                # read block
                blockData = self.__dict.popitem()

                # go to position and write data
                filePosition = self.__blocksize * blockData[0]
                file.seek(filePosition, 0)
                file.write(blockData[1])
 
            # close file
            file.close()

        # any problem: abort
        except Exception, e:
            print e
            print "Problem while writing file. Aborting."
            sys.exit(1)
 
    # run()
# WriterThread()
