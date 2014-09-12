# -*- coding: utf-8 -*-
import logging
import sys


class Debug():
    '''
    Debug info print( and write the log into files
    '''
    def __init__(self, logfile):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(20)
        self.level = 20
        formatter = logging.Formatter('%(asctime)s %(levelname)-4s %(message)s', '%a, %d %b %Y %H:%M:%S',)  
        file_handler = logging.FileHandler(logfile)
        file_handler.setFormatter(formatter)
        stream_handler = logging.StreamHandler(sys.stderr)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stream_handler)
        self.uiOutputSignal = None
        self.uiOutputLevel = 1

    def setOutputSignal(self, outputSignal):
        self.uiOutputSignal = outputSignal

    def getLevel(self):
        return self.level

    def setLevel(self, level):
        self.logger.setLevel(level)
        self.level = level

    def __call__(self, msg):
        self.logger.debug(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)
        if self.uiOutputLevel >= 1 and self.uiOutputSignal:
            self.uiOutputSignal.emit(msg)

    def error(self, msg):
        self.logger.error(msg)

    def output(self, msg):
        self.logger.debug(msg)

debug = Debug("run.log")


class CommandLine(object):
    def parseCmdLine(self):

        import optparse
        usage = "usage: %prog [options] arg"
        parser = optparse.OptionParser(usage)
        parser.add_option('-T', '--taskname', dest='TASKNAME',
                          help='build task name')

        parser.add_option('-p', '--product', dest='PRODUCT',
                          help='contains product information')

        parser.add_option('-s', '--supplier', dest='SUPPLIER',
                          help='company info  from supplier search page')

        parser.add_option('-w', '--website', dest='WEBSITE',
                          help='the website where the data will get from it')
        return parser.parse_args()



