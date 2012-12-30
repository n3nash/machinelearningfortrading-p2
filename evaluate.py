
import datetime as dt

import numpy as np
import pandas as pand
import matplotlib.pyplot as plt

from qstkutil import DataAccess as da
from qstkutil import dateutil as du

from qstkfeat.features import *
from qstkfeat.classes import classFutRet
import qstkfeat.featutil as ftu

#used john cornwell's code
def learnerTest( naTrain, naTest ):
    
    kdtlearner = ftu.createKnnLearner( naTrain, 5 )

    naResult = kdtlearner.query( naTest[:,:-1] )

    correlation = np.corrcoef(naResult,naTest[:,-1])
    return correlation
    	#return naResult

        
train_data=0
test_data=0
def store_train_and_test(train , test):
        global train_data
        global test_data
        train_data = train
        test_data = test

def find_best_feature(features):

#first for loop gets the first best feature.

	hmax = 0
	for i in range(0,9):
		 print 'testing feature set[',i,',9]'
                 args = []
                 features = []
                 global train_data
                 global test_data
                 features.append(copyfeatures[i])
                 features.append(copyfeatures[9])
                 args.append(copyargs[i])
                 args.append(copyargs[9])
                 ldfFeatures_new = ftu.applyFeatures( dfPrice, dfVolume, features, args )
                 naFeatTrain = ftu.stackSyms( ldfFeatures_new, dtStartTrain, dtEndTrain)
                 naFeatTest = ftu.stackSyms( ldfFeatures_new, dtStartTest, dtEndTest )
                 store_train_and_test(naFeatTrain,naFeatTest)
                 #print naFeatTrain,"NEXT"
                 #print naFeatTest
                 ltWeights = ftu.normFeatures( naFeatTrain, -1.0, 1.0, False )
                 ftu.normQuery( naFeatTest[:,:-1], ltWeights )
		
                 corr_of_this = learnerTest(naFeatTrain,naFeatTest)

		 print 'corr coef = ',corr_of_this[0][1]
		
                 if(corr_of_this[0][1] > hmax):
                        hmax = corr_of_this[0][1]
                        feature = copyfeatures[i]
                        best = i
        #print "best corr coef",hmax,'for',best

#now all combinations are checked for all other 8 possible ones.

 	allbest = []
	args = []
	features = []
	features.append(copyfeatures[best])
  	args.append(copyargs[best])
	h = 1
	allbest.append(best)
	for k in range(0,8):
		found = 0
        	for i in range(0,9):
		 	if(i not in allbest):
		 		global train_data
				global test_data
		 		features.append(copyfeatures[i])
				h = h+1
		 		features.append(copyfeatures[9])
		 		args.append(copyargs[i])
		 		args.append(copyargs[9])
			
				print 'testing feature set [',allbest,',',i,',9]'

                 		ldfFeatures_new = ftu.applyFeatures( dfPrice, dfVolume, features, args )
		 		naFeatTrain = ftu.stackSyms( ldfFeatures_new, dtStartTrain, dtEndTrain)
    		 		naFeatTest = ftu.stackSyms( ldfFeatures_new, dtStartTest, dtEndTest )
    		 		store_train_and_test(naFeatTrain,naFeatTest)
    		 		#print naFeatTrain,"NEXT"
    		 		#print naFeatTest
    		 		ltWeights = ftu.normFeatures( naFeatTrain, -1.0, 1.0, False )
    		 		ftu.normQuery( naFeatTest[:,:-1], ltWeights )
	
	                 	corr_of_this = learnerTest(naFeatTrain,naFeatTest)
                 		if(corr_of_this[0][1] > hmax):
					found = 1
                       			hmax = corr_of_this[0][1]
					argument = copyargs[i]
                       			feature = copyfeatures[i]
					args.remove(copyargs[i])
					features.remove(copyfeatures[i])
					args.remove(copyargs[9])
					features.remove(copyfeatures[9])
					best = i
				#allbest.append(best)
					print 'corr coef =', hmax
				#best = i + best
		 		else:
					h = h - 1
					print 'corr coef = ',corr_of_this[0][1]
					#args.remove(copyargs[i])
					args.remove(copyargs[9])
				
					#features.remove(copyfeatures[i])
					features.remove(copyfeatures[9])
		if found==1:
			allbest.append(best)
			args.append(argument)
			features.append(feature)
		else:
			break
			#for k in range(0,h):
				#print 'best is',features[k]
        print 'best feature set [',allbest,',9]'
	print "corr coef = ",hmax
	return

global dtStartTrain
global dtEndTrain
global dtStartTest
global dtEndTest

#reffered to john cornwell's code
if __name__ == '__main__':
    
    lsSym = ['AA', 'AXP', 'BA', 'BAC', 'CAT', 'CSCO', 'CVX', 'DD', 'DIS', 'GE', 'HD', 'HPQ', 'IBM', 'INTC', 'JNJ', \
             'JPM', 'KFT', 'KO', 'MCD', 'MMM', 'MRK', 'MSFT', 'PFE', 'PG', 'T', 'TRV', 'UTX', 'WMT', 'XOM','VZ'  ]
    
    dtStarttrain = dt.datetime(2007,01,01)
    dtEndtrain = dt.datetime(2009,12,31)
    dtStartTest = dt.datetime(2010,01,01)
    dtEndTest = dt.datetime(2010,06,30)
    
    norObj = da.DataAccess('Norgate')   
    lfdTimestamps = du.getNYSEdays(dtStarttrain, dtEndtrain, dt.timedelta(hours=16))    
    ldtTimestamps = du.getNYSEdays( dtStartTest, dtEndTest, dt.timedelta(hours=16) )

    lTimestamps = du.getNYSEdays(dtStarttrain , dtEndTest , dt.timedelta(hours=16))
    global dfPrice
    global dfVolume
    dfPrice = norObj.get_data( lTimestamps, lsSym, 'close' )
    dfVolume = norObj.get_data( lTimestamps, lsSym, 'volume' )
    
    lfcFeatures = [ featMA,featMA, featRSI,featRSI,featDrawDown,featRunUp,featVolumeDelta,featVolumeDelta,featAroon, classFutRet ]
    global copyfeatures
    copyfeatures = lfcFeatures
    #ldArgs = [{}] * len(lfcFeatures) 
    
    ''' Custom Arguments '''
    ldArgs = [ {'lLookback':10, 'bRel':True},\
               {'lLookback':20,},\
               {'lLookback':10},\
		{'lLookback':20},\
		{},\
		{},\
		{'lLookback':10},\
		{'lLookback':20},\
		{'bDown':False},\
		{'lLookforward':5}]           
    global copyargs
    copyargs = ldArgs         
    
    ldfFeatures = ftu.applyFeatures( dfPrice, dfVolume, lfcFeatures, ldArgs )
   
        #for i, fcFunc in enumerate(lfcFeatures[:-1]):
            
    lSplit = int(len(lfdTimestamps))
    dtStartTrain = lfdTimestamps[0]
    dtEndTrain = lfdTimestamps[lSplit-1]
    lSplit2 = int(len(ldtTimestamps))
    dtStartTest = ldtTimestamps[0]
    dtEndTest = ldtTimestamps[lSplit2-1]
     
    naFeatTrain = ftu.stackSyms( ldfFeatures, dtStartTrain, dtEndTrain)
    naFeatTest = ftu.stackSyms( ldfFeatures, dtStartTest, dtEndTest )
    store_train_and_test(naFeatTrain,naFeatTest)

    ltWeights = ftu.normFeatures( naFeatTrain, -1.0, 1.0, False )
    ''' Normalize query points with same weights that come from test data '''
    ftu.normQuery( naFeatTest[:,:-1], ltWeights )
    find_best_feature(ldfFeatures)	
    #learnerTest( naFeatTrain, naFeatTest )  
    
