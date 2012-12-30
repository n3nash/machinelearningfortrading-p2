import numpy as np
import scipy as sc
import math
import sys
import time
from multiprocessing import Pool
from multiprocessing import cpu_count
data = np.zeros (0)#this is the global data
import scipy.stats
import bisect,random
import numpy,scipy.spatial.distance, scipy.spatial.kdtree
import knn,cProfile,pstats,gendata

global i
i=0
class KNNlearner:
	def __init__(self , k , method):
		self.k = k
		self.data_x = None
		self.data_y = None
		self.method = method


	def addEvidence(self, Xtrain , Ytrain):
		#print Xtrain
		global i
		if(self.data_x == None):
			self.data_x = Xtrain
		else:
			self.data_x = np.append(self.data_x,Xtrain,axis=0)
			#print self.data_x
			#self.data_x = self.data_x.reshape(i,3)
			i = i + 1
			#print self.data_x
		if(self.data_y == None):
			self.data_y = Ytrain	
		else:
			self.data_y = np.append(self.data_y,Ytrain,axis=0)
	def change(self):
		global i
		self.data_x = self.data_x.reshape(i+1,3)
		i=0
		#print self.data_x
	def query(self,Xtest):
		avg = 0
		result2 = []
		#print self.data_x
		#print len(self.data_x)
		for i in range(0,int(math.ceil(0.6*len(self.data_x)))-1):
			result2.append(pow((self.data_x[i][0] - Xtest[0]),2) + pow((self.data_x[i][1] - Xtest[1]),2))
		#print 'result2',result2
		result3 = np.array(result2)
		#print result3
		result = result3.argsort(axis=0)
		#print result
		for j in range(0,self.k):
			avg = avg + self.data_x[result[j]][2];
		avg = avg / self.k
		#print result
		return avg

	

if __name__=="__main__":
	call_this()					
