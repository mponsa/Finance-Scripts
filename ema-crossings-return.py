# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 18:04:27 2017

@author: mponsa
"""



import pandas as pd
import numpy as np
import pandas_datareader.data as pdr
import datetime
import matplotlib.pyplot as plt
from sklearn import linear_model

def emaCross(df,fast,slow):
    df['emaf'] =  pd.stats.moments.ewma(df['Close'],fast)
    df['emas'] =  pd.stats.moments.ewma(df['Close'],slow)
    prevf = data['emaf'].shift(1)
    prevs = data['emas'].shift(1)
    df['Nsignal'] = ((df['emaf'] <= df['emas']) & (prevf >= prevs))
    df['Psignal'] = ((df['emas'] <= df['emaf']) & (prevs >= prevf))
    
    result = df[(data['Psignal'] == True) | (df['Nsignal'] == True)]
    result['Date'] = pd.to_datetime(result.index)
    dateshift = result['Date'].shift(1)
    result['DiffDays'] = result['Date']- dateshift  
    result['Return'] = result['Close'].diff()
    
    return result.drop(['Date','emaf','emas'],1)
    
#List with stocks to analyze.
stocks =['BCBA:BMA']

start = datetime.date(2000,1,1)
end = datetime.date(2017,10,13)

#Read 'OLHC' data from google finance
data= pdr.DataReader(stocks[0],'google',start,end)

crossings = emaCross(data,12,26)


plt.plot(data['Close'])
plt.scatter(data[data['Psignal'] == True].index,data['Close'][data['Psignal'] == True], c = 'g')  
plt.scatter(data[data['Nsignal'] == True].index,data['Close'][data['Nsignal'] == True], c = 'r')

