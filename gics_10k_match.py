import zipfile as zf
import urllib
import re
import sys
import random

LINK = "http://funglab.berkeley.edu/pub/tic_company_gics"
GICS = "tic_company_gics.txt"
GICSCODE = '45'
FILEDIR = 'company_gics.txt'

def download_gics(link=LINK, filedir=GICS):
	# Download txt-like webpage as it is
	urllib.urlretrieve(link, filedir)

def read_gics(filedir=GICS, code=GICSCODE):
	# Return a list containing all the companies in the industry
	code = '|{}'.format(code)
	with open(filedir) as gics:
		content = gics.readlines()
		for i in range(0,len(content)):
			content[i] = re.sub('\n','',content[i])
			content[i] = re.sub('\t','|',content[i])
			# need to remove tic before match gics code
			# some tics might contain the code number
			content[i] = re.sub('^\w+[\.]*[0-9a-zA-Z]*[\.]*\|','',content[i])
		companylist = list([x.lower() for x in set(content) if code in x])
		companylist = gics_format(companylist)
	return companylist

def gics_format(clist):
	for i in range(0,len(clist)):
		# remove gics code
		clist[i] = re.sub('\|45$','',clist[i])
		# remove tail '-**' like tags
		clist[i] = re.sub('[ ]+\-[a-z]+[0-9]*[ ]*[\-]*[a-z]*[0-9]*$','',clist[i])
		# remove tail '-**' like tags (corner cases)
		clist[i] = re.sub('-[a-z]{1,4}[0-9]*$','',clist[i])
		# remove all '/*' in tail
		clist[i] = re.sub('/\w+$','',clist[i])
		# patterns
		clist[i] = re.sub(' hldgs ',' holdings ',clist[i])
		clist[i] = re.sub('grp','group',clist[i])
		clist[i] = re.sub('intl','(international|intl)',clist[i])
		clist[i] = re.sub(' sys ',' (system|systems) ',clist[i])
		clist[i] = re.sub('-','( |-)',clist[i])
		clist[i] = re.sub(' (corp\.|corp)$','[,]* (corp|corporation)',clist[i])
		clist[i] = re.sub(' ltd$','[,]* ltd',clist[i])
		clist[i] = re.sub(' co$',' (co|company)',clist[i])
		clist[i] = re.sub(' cp$','',clist[i])
		clist[i] = re.sub(' inc$','[,]* inc',clist[i])
		clist[i] = re.sub('( com|\.com)$','( com|\.com)',clist[i])
		clist[i] = re.sub('( com |\.com )','( com |\.com )',clist[i])
		clist[i] = re.sub('( com\[|\.com\[)','( com|\.com)[',clist[i])
		# corner cases
		clist[i] = re.sub('cmp','computer',clist[i])
		clist[i] = '_' + clist[i]
	return clist

def write_company(ls,directory=FILEDIR):
	with open(directory,'w') as output:
		for c in ls:
			output.write(c+'\n')

def read_company(directory):
	# Read in the name list
	with open(directory, 'r') as namelist:
		content = namelist.readlines()
	# take out the '\n' sign
	for i in range(0,len(content)):
		content[i] = re.sub('\n','',content[i])
		content[i] = re.sub('[\\\\r]+$','',content[i])
	return content

def match_company(names_gics, names_10k, logdir):
	with open(logdir,'w') as log:
		res = []
		count = 0
		find = False
		for mch in names_gics:
			sys.stdout.write(str(count)+'\n')  # same as print
			sys.stdout.flush()
			count += 1
			for name in names_10k:
				if re.search(mch,name.lower()) is not None:
					res.append(name)
					names_10k.remove(name)
					find = True
			if not find:
				log.write(mch + '\n')
			find = False
	return res

def rnd_smpl(file_10K,smpsize):
	sample = [file_10K[i] for i in sorted(random.sample(xrange(len(file_10K)), smpsize))]
	return sample

def partial_extract(zipfilename,namelist):
	with zf.ZipFile(zipfilename,'r') as myzip:
		write_company(namelist,'./filelist.txt')
		map(myzip.extract,namelist)

if __name__ == '__main__':
	#######################################################
	# GET THINGS READY
	# download_gics()
	# company = read_gics()
	# write_company(company,'IT_companies.txt')
	# write_company(company)
	# -----------------------------------------------------
	# Total number of companies in IT industry: 4266 (GOAL)
	# log1: 1902
	# log2: 1854
	# log3: 1858
	# log4: 1900
	# log5: 1843
	#######################################################
	# MATCH COMPANIES' NAMES IN 1O-K ZIPFILE
	# company_gics = read_company('company_gics.txt')
	# company_file = read_company('company_file.txt')
	# log = 'Not_find_log.txt'
	# res = match_company(company_gics,company_file,log)
	# write_company(res,'IT_10K.txt')
	target_files = read_company('IT_10K.txt')
	samplelist = rnd_smpl(target_files,1000)
	partial_extract('E:/sec-10-k.zip',samplelist)
	#######################################################