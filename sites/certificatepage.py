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
            debug.error()
            return
        dditems = contactItems.find_all('dd')

        contacts = dditems[0].text.expandtabs(1).strip().split('：')
        self.contactPerson = len(contacts) == 2 and contacts[1] or contacts[0]

        numbers = dditems[1].text.expandtabs(1).strip().split('：')
        self.mobilePhone = len(numbers) == 2 and numbers[1] or numbers[0]

        numbers = dditems[2].text.expandtabs(1).strip().split('：')
        self.phoneNumber = len(numbers) == 2 and numbers[1] or numbers[0]


