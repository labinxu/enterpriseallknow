import configparser
import string
import os
import sys


class AppConfig:
    def __init__(self, confFile):
        self.conf_file = confFile
        self.cf = configparser.ConfigParser()
        self.cf.read(confFile)

    def getLanguage(self):
        return self.cf.get('language', 'language')


appconfig = AppConfig('gui/configure/appconfig.ini')
print('language is %s' % appconfig.getLanguage())


