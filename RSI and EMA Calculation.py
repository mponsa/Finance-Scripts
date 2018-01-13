# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 10:53:38 2017

@author: mponsa
"""

import numpy as np
import pandas as pd
from pandas_datareader import data,wb
import matplotlib.pyplot as plt
import datetime 

stock = 'BCBA:YPFD'
start = datetime.date(2005,1,1)

df = data.DataReader(stock,'google',start = start)

#RSI Calculation.
window_length = 14
close = df['Close']

# Make the positive gains (up) and negative gains (down) Series
delta = close.diff()
up, down =  delta.copy(), delta.copy()
up[up < 0] = 0
down[down > 0] = 0
# Calculate the EWMA
roll_up1 = pd.stats.moments.ewma(up, window_length)
roll_down1 = pd.stats.moments.ewma(down.abs() , window_length)
RS1 = roll_up1/roll_down1
RSI1 = 100.0 - (100.0 / (1.0 + RS1))
# Calculate the SMA
roll_up2 = pd.rolling_mean(up,window_length)
roll_down2 = pd.rolling_mean(down.abs(),window_length)
RS2 = roll_up2 / roll_down2
RSI2 = 100.0 - (100.0 / (1.0 + RS2))



#12-EMA Calculation
ema12 = pd.stats.moments.ewma(close,12)

#26-EMA Calculation
ema26 = pd.stats.moments.ewma(close,26)

#Signal
signal = pd.ewma(close,span=9)

#MACD
macd = ema12-ema26

#10-SMA Calculation
sma10 = pd.rolling_mean(close,window=10)

#50-SMA Calculation
sma50 = pd.rolling_mean(close,window=50)

#Crossover = macd - signal
crossover = macd-signal


#Calculate  CCI
tp = ((df['High'] + df['Close'] + df['Low']) / 3).dropna()
tpsma20 = pd.rolling_mean(tp,window=20)
tpsma20dev = pd.rolling_std(tpsma20,window=20) 
constant = 0.15
cci = ((tp - tpsma20)/(constant * tpsma20dev)).dropna()

#On balance volume calculation (OBV) (If diff >0  volume running sum)
multiplier = close.diff()
multiplier[multiplier < 0] = -1
multiplier[multiplier > 0] = 1
multiplier[multiplier ==  0] = 0
multiplier[0] = 1
obv = multiplier * df['Volume']
obv = obv.cumsum()


plt.figure()
RSI1.plot()
RSI2.plot()
plt.legend(['RSI via EWMA', 'RSI via SMA'])

plt.figure()
cci.plot()
plt.legend(['CCI'])

plt.figure()
ema12[-365:].plot()
ema26[-365:].plot()
sma10[-365:].plot()
sma50[-365:].plot()
close[-365:].plot()
plt.legend(['12d-ema','26d-ema','sma10','sma50','Close price'])

plt.figure()
macd.plot()
plt.legend(['MACD'])

plt.figure()
signal.plot()
plt.legend(['Signal'])

plt.figure()
obv.plot()
plt.legend(["On Balance Volume"])

plt.show()

#Signals
#ema12 cross ema26
signal1 = ema12 - ema26
signal1[signal1 < 0] = -1
signal1[signal1 > 0] = 1
signaltest = signal1.copy()

signal1[signal1.eq(signal1.shift(1)) == True] = 0


#sma10 cross sma50
signal2 = sma10 - sma50
signal2[signal2 < 0] = -1
signal2[signal2 > 0] = 1
signal2[signal2.eq(signal2.shift(1)) == True] = 0

#overbought or oversold conditions 1 = oversold and -1 overbought
RSIsig = RSI1.copy()
RSIsig[RSIsig < 30] = 1
RSIsig[RSIsig > 70] = -1

allconditions = signal1 * signal2 * RSIsig

result = close.to_frame(name='Close').join(allconditions.to_frame(name='Signals'))

result = result[-665:]

plt.scatter(result[result['Signals'] == 1].index,result['Close'][result['Signals'] == 1], color = 'g')
plt.scatter(result[result['Signals'] == -1].index,result['Close'][result['Signals'] == -1],color = 'r')
plt.plot(close[-665:])
plt.plot(sma10[-665:])
plt.plot(sma50[-665:])
plt.show()


