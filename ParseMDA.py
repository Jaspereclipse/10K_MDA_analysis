#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8 
#################################################
# Parse 10-K file(.txt) and Extract MDA section #
# It is becoming stronger!!                     #
#################################################

import sys
reload(sys)
sys.setdefaultencoding('utf8') # for ’ to work in regex  
import bs4
import re
import json

DEFAULT_FILENAME = 'Files/FiveCompany/Widepoint/0001144204-15-016396.txt'

class ParseMDA(object):
    def __init__(self, filename=DEFAULT_FILENAME):
        self.file_to_parse = filename
        with open(self.file_to_parse, 'r') as txt_file:
            self.txt = unicode(txt_file.read(),errors = 'replace') 

    def find_div_with_text(self):
        soup = bs4.BeautifulSoup(self.txt, "html.parser")
        scores = soup.find_all(text=re.compile('(DISCUSSION AND ANALYSIS)|(Discussion and Analysis)'))
        divs = []
        for i in range(0,len(scores)):
            score = scores[i]
            while score.parent is not None:
                score = score.parent
            divs.append(score)
        if len(divs) > 0:
            return divs[0].getText()

    def merge_index(self,list1,list2):
        ctr1 = 0
        ctr2 = 0
        l = []
        ind = []
        while len(l) < len(list1) + len(list2):
            if ctr1 < len(list1) and ctr2 < len(list2):
                if list1[ctr1] <= list2[ctr2]:
                    l.append(list1[ctr1])
                    ctr1 += 1
                    ind.append(1)
                else:
                    l.append(list2[ctr2])
                    ctr2 += 1
                    ind.append(2)
            elif ctr1 >= len(list1):
                l.append(list2[ctr2])
                ctr2 += 1
                ind.append(2)
            elif ctr2 >= len(list2):
                l.append(list1[ctr1])
                ctr1 += 1
                ind.append(1)
        return (l,ind)

    def mda_parse(self,content):
        pattern_start = re.compile('(?<! \x93)(?<![a-z] )Item(\xa0)*[.]{0,10}(\n)*[ ]*[7|(SEVEN)][ ]*[-\.:(\xc2\x97)\x96]{1}',flags=re.IGNORECASE)
        pattern_end = re.compile('(?<! \x93)(?<![a-z] )Item(\xa0)*[.]{0,10}(\n)*[ ]*[8|(EIGHT)][ ]*[-\.:(\xc2\x97)\x96]{1}',flags=re.IGNORECASE)
        start = [s.start(0) for s in re.finditer(pattern_start, content)]
        end = [e.start(0) for e in re.finditer(pattern_end, content)]
        series = self.merge_index(start,end)
        l = series[0]
        ind = series[1]
        for i in range(0,len(l)-1):
            if ind[i+1] > ind[i]:
                if l[i+1]-l[i] > 10000: # minimum length in MDA section
                    return content[l[i]:l[i+1]]

if __name__ == '__main__':
    pf = ParseMDA()
    div = pf.find_div_with_text()
    content = pf.mda_parse(div)
    mda = open("Files/mda/mda_Widepoint.txt","w")
    mda.write(content)
    mda.close()