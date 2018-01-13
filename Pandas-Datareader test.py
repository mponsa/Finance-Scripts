# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 15:53:41 2017

@author: mponsa
""" 
import numpy as np
import pandas as pd
from pandas_datareader import data, wb
import datetime
import matplotlib.pyplot as plt
from sklearn import linear_model

#List with stocks to analyze.
stocks =['BCBA:BMA']

start = datetime.date(2017,1,1)
end = datetime.date(2017,10,6)



#Read 'OLHC' data from google finance
data = data.DataReader(stocks[0],'google',start,end)

#Linear regression for close price.
#Split train and test sets
X = data.drop(['Close'],1)
y = data['Close']

X_train = X[:-50]   
X_test = X[-50:]
X_test.dropna(inplace=True)
y_train = y[:-50]
y_test = y[-50:]

reg = linear_model.LinearRegression()
reg.fit(X_train,y_train)




#----------------------------------------------------------------------------------------------------------



        
