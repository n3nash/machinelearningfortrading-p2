import KNNlearner as p
import numpy as np
import time
import math
import matplotlib.pyplot as plt

def call_this():
        for data in range(0,2):
		learner = {}
                if(data == 0):
                        f = open('/nethome/nagarwal36/QSTK/Examples/KNN/data-classification-prob.csv', 'r')
			file = 'data-classification-prob.csv'
			plot = 'plot1.pdf'
                else:
                        global i
                        i=0
                        f = open('/nethome/nagarwal36/QSTK/Examples/KNN/data-ripple-prob.csv','r')
			file = 'data-ripple-prob.csv'
			plot = 'plot2.pdf'
		karr = []
		plott = []
		for k in range(1,80):
			#print "k is",k
			learner = p.KNNlearner(k,'mean')
			karr.append(k);
			f = open('/nethome/nagarwal36/QSTK/Examples/KNN/'+file, 'r')
                	x = np.array([map(float,s.strip().split(',')) for s in f.readlines()])
                	starttime = time.clock()
                	for eviden in range(0,int(math.ceil(0.6*len(x)))):
				#print x[eviden]
                        	learner.addEvidence(x[eviden],x[eviden])
                	endtime = time.clock()
                	#print 'add evidence time',endtime-starttime
                	learner.change()

                #f1 = open('/nethome/nagarwal36/QSTK/Examples/KNN/data1.csv','r')
                	second_half = x #np.array([map(float,s.strip().split(',')) for s in f1.readlines()])
                	result = []
                	coff = []
                	expected = []
                	actual = []
                	begintime = time.clock()
                	for i in range(int(math.ceil(0.6*len(second_half))),len(second_half)):
                        	result = learner.query(second_half[i])
                        	expected.append(result)
                        	actual.append(second_half[i][2])
                	finaltime = time.clock()
                	#print 'query time',finaltime - begintime
                	try:
                        	#print expected
                        	#print actual
                        	value = np.corrcoef([actual,expected])
				plott.append(value[0][1])
                	except:
                        	print "ERROR"
		plt.clf()
		plt.plot(karr,plott)
		plt.ylabel("correlation coefficient")
		plt.xlabel("k values")
		plt.savefig(plot,type='pdf')

call_this()
