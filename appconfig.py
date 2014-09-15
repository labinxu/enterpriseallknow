import os
import configparser
from utils import debug


class AppConfig:
    def __init__(self, confFile):
        self.conf_file = confFile
        if os.path.exists(confFile):
            self.cf = configparser.ConfigParser()
            self.cf.read(confFile, encoding='utf8')
        else:
            debug.error('%s not found' % confFile)

    def getLanguage(self):
        return self.cf.get('language', 'language')

    def getZhText(self, moduleName, engText):
        return self.cf.get(moduleName, engText)

    def getSites(self):
        return self.cf.items('sites')

appconfig = AppConfig('./configure/appconfig.ini')
