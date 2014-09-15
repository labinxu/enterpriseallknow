# -*- coding: utf-8 -*-
from sites.pageparser import PageParser
from utils import debug


class CertifiactePageParser(PageParser):
    def __init__(self, pageurl):
        PageParser.__init__(self, pageurl)
        self.yellowpageUrl = None

    def getYellowPageUrl(self):
        if self.yellowpageUrl:
            return self.yellowpageUrl

        if not self.soup:
            self.soup = self.getSoup()

        linkitem = self.soup.find('a', attrs={'class': 'comment-link'})
        if linkitem:
            self.yellowpageUrl = linkitem.get('href')

        return self.yellowpageUrl

    def parserInfo(self):
        if not self.soup:
            self.soup = self.getSoup()
            if not self.soup:
                return None
        keywords = {'class': 'module-content gray-b-bg'}
        contactItems = self.soup.find('div', attrs=keywords)
        if not contactItems:
            debug.error('Can not found div tag %s' % self.pageUrl)
            return
        dditems = contactItems.find_all('dd')
        for dditem in dditems:
            tmplist = dditem.text.expandtabs(1)
            tmplist = tmplist.replace(';', '').strip().split('：')
            if len(tmplist) == 2:
                if '联系人' in tmplist[0]:
                    self.contactPerson = tmplist[1]
                elif '固定电话' in tmplist[0]:
                    self.phoneNumber = tmplist[1]
                elif '联系电话' in tmplist[0]:
                    self.mobilePhone = tmplist[1]
            else:
                debug.error('%s %s' % (tmplist, self.pageUrl))
