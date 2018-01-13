# -*- coding: utf-8 -*-
"""
Created on Sat Oct 28 17:34:07 2017

@author: manue
"""

import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as web


#download daily price data for each of the stocks in the portfolio
data = web.DataReader('BCBA:BMA',data_source='google',start='01/01/2010')

data['100ma'] = data['Close'].rolling(window=100).mean()
data.dropna(inplace=True)

ax1 = plt.subplot2grid((6,1),(0,0),rowspan = 5, colspan=1)
ax2 = plt.subplot2grid((6,1),(5,0),rowspan = 1, colspan =1, sharex = ax1)

ax1.plot(data.index,data['Close'])
ax1.plot(data.index,data['Close'])
ax2.bar(data.index,data['Volume'])