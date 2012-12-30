import re
import gzip
import itertools
import string
import os
import sys

def make_list_remove():
	 global remove_type
	 for c in string.punctuation:
         	remove.append(c)
	 list = ['1','2','3','4','5','6','7','8','9','10']
	 for one in list:
	 	remove.append(one)

def read_directory(fileName):
	WordList = []
	global Wordlist
	global remove
	f = open(fileName, 'r').read()
	WordList = f.split()
	WordList = [''.join(c for c in s if c not in remove) for s in WordList]
	for word in WordList:
		for c in remove:
			word.strip(c)
	#print WordList
	return WordList
		#for c in string.punctuation:
	     		#word= word.replace(c,"")

def calculate_hash_bad(List):
	global badlist
	global WordList
	for word in List:
		compute = hash(word)%1000
		try:
			badlist[compute] = badlist[compute] + 1
		except:
			badlist[compute] = 1	


def calculate_hash_good(List):
	global goodlist
	global WordList
	for word in List:
		compute = hash(word)%1000
		try:
			goodlist[compute] = goodlist[compute] + 1
		except:
			goodlist[compute] = 1

def compute_total_good():
	global totalgood
	global goodlist
	global goodpList
	#print goodlist
	for key,value in goodlist.items():
		totalgood = totalgood + value
	for key,value in goodlist.items():
		#print 'value is',value,'total',totalgood
		goodp = (float(value*1)/float(totalgood))
		#print 'value in goodp',goodp
		goodpList.append(goodp)

def compute_total_bad():
	global totalbad
	global badlist
	global badpList
	#print badlist
	for key,value in badlist.items():
		totalbad = totalbad + value
	for key,value in badlist.items():
		badp = (float(value*1)/float(totalbad))
		badpList.append(badp)

def compute_weights():
	global goodpList,badpList,weights
	weights = []
	#print goodpList,'NEXT NEXT',badpList
	for goodp,badp in zip(goodpList,badpList):
		#print 'values are',float(goodp - badp)/float(goodp + badp)
		try:
			weights.append(float(goodp - badp)/float(goodp + badp))
		except:
			weights.append(0)
	#print weights

def testing_data(fileName):
	WordList = []
	newwordList = {}
	global weights
	i=0
	sum = 0
	bad = 0
	good = 0
	isgood = re.search("goodnews",fileName)
	if(isgood == None):
		bad = 1
	else:
		good = 1
        f = open(fileName, 'r').read()
        WordList = f.split()
	name = fileName.split('/')
	#print name
	WordList = [''.join(c for c in s if c not in remove) for s in WordList]
        for word in WordList:
		for c in remove:
                	word.strip(c)

        for word in WordList:
                compute = hash(word)%1000
		if compute in newwordList:
                	newwordList[compute] = newwordList[compute] + 1
		else:
			newwordList[compute] = 1
	for key,value in newwordList.items():
		sum = sum + (value*weights[i])
		if i>=len(weights)-1:
			break
		i=i+1
	global count
	if(sum > 0):
		print 'file:',name[len(name)-2],'/',name[len(name)-1]
		print 'class:','good'
		if(good == 1):
			count = count + 1
	else:
		print 'file:',name[len(name)-2],'/',name[len(name)-1]
		print 'class:','bad'
		if(bad == 1):
			count = count + 1

if __name__=="__main__":
	global weights,WordList,newwordList,badpList,goodpList
	flist = []
	glist = []
	count = 0
	i=0
	goodlist = {}
	for i in xrange(1000):
     		goodlist[i] = 0
	badlist = {}
	i=0
	for i in xrange(1000):
                badlist[i] = 0
	#goodlist = dict.fromkeys((range(1000)))
	#badlist = dict.fromkeys((range(1000)))
	weights = [0 for x in range(1000)]
	totalgood=0
	totalbad = 0
	totalcount = 0
	remove = []
	WordList = []
	goodpList = []
	badpList = []
	newwordList = {}

	make_list_remove()
	filespath = '/hzr71/research/QSDataLabel/'
	glist.append(sys.argv[1])	
	glist.append(sys.argv[2])
	glist.append(sys.argv[3])
	flist = open(filespath+glist[0]).read()
	files = flist.split('\n')
	del files[len(files)- 1]
	for file in files:
		list = read_directory(file)
		calculate_hash_good(list)
	compute_total_good()
	flist = open(filespath+glist[1]).read()
	files = flist.split('\n')
	del files[len(files)- 1]
	for file in files:
		list = read_directory(file)
		calculate_hash_bad(list)
	compute_total_bad()
	compute_weights()
	flist = open(filespath+glist[2]).read()
        files = flist.split('\n')
	del files[len(files)- 1]
        for file in files:
		totalcount = totalcount + 1
                testing_data(file)
	print 'score is',count,'/',totalcount

