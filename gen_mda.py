#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding=utf8

########################
#  Parse mda in scale  #
########################
from ParseMDA import ParseMDA
from gics_10k_match import read_company
import sys
import HTMLParser

if __name__ == '__main__':
	filelist = read_company('sec-10-k/filelist.txt')
	ctr = 1
	sctr = 1
	for f in filelist:
		sys.stdout.write('Total: '+str(ctr)+'\n')
		sys.stdout.flush()
		ctr += 1
		filedir = 'sec-10-k/{}'.format(f)
		pf = ParseMDA(filedir)
		div = None
		try:
			div = pf.find_div_with_text()
		except HTMLParser.HTMLParseError:
			print "Oops! Damn it..."
		if div is not None:
			content = pf.mda_parse(div)
			if content is not None:
				output = 'mda/mda_{}.txt'.format(f)
				with open(output,"w") as mda:
					mda.write(content)
				sys.stdout.write('Successful: '+str(sctr)+'\n')
				sys.stdout.flush()
				sctr += 1
			else:
				sys.stdout.write(str(f)+'\n')
				sys.stdout.flush()