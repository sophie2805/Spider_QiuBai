#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import urllib2
__author__ = 'Sophie2805'

class FetchData(object):
    def __init__(self,URL,referURL,pattern_1,pattern_2):
        self.URL = URL
        self.pattern_1 = pattern_1
        self.patttern_2 = pattern_2
        self.referURL = referURL

    def getHtml(self):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            'Referer':self.referURL  #http://www.qiushibaike.com/
        }
        req = urllib2.Request(
            url = self.URL, #http://www.qiushibaike.com/text
            headers = headers)
        return urllib2.urlopen(req).read()

    def getData(self,html):
        p_1 = re.compile(self.pattern_1)
        div_content = p_1.findall(html.decode('utf8'))
        row = 0
        for m in range(len(div_content)):
            div_content[m] = re.sub(self.patttern_2,'',div_content[m])
            div_content[m] = ("---" + str(row+1) + "---" + div_content[m]).encode('utf-8')
            row += 1
        return div_content


