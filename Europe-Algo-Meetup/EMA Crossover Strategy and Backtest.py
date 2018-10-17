#!/usr/bin/env python
# coding: utf-8

# <h1>EMA Crossover Strategy</h1>

# In[1]:


import fxcmpy
import pandas as pd
import numpy as np
import datetime as dt

# Importing the EMA indicator
from pyti.exponential_moving_average import exponential_moving_average as ema

# Allows for printing the whole data frame
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# <h3>Connecting and Retrieving Prices</h3>

# In[2]:


con = fxcmpy.fxcmpy(config_file='fxcm.cfg')


# In[3]:


# retrieve daily candles for the GBP/JPY currency pair from 01/01/2016 until 06/10/2018

df = con.get_candles('GBP/JPY', period='D1',start= dt.datetime(2016, 1, 1),end = dt.datetime(2018, 6, 10))

#df = pd.read_csv('historical_data.csv', index_col = 0, parse_dates=True)


# <h3>Define the EMA Strategy</h3>

# In[4]:


# Define our pip cost and lot size
pip_cost = .0911
lot_size = 10

# Define our EMA Fast / Slow parameters
ema_fast = 12
ema_slow = 20

# Populate our dataframe with fast and slow EMA figures
df['mva_fast'] = ema(df['askclose'], ema_fast)
df['mva_slow'] = ema(df['askclose'], ema_slow)

# When the EMA fast crosses the EMA slow, a buy signal is triggered
df['signal'] = np.where(df['mva_fast'] > df['mva_slow'],1,0)
df['position'] = df['signal'].diff()


# In[5]:


# Check on the dataframe to see the newly created columns

df


# <h3>A Simple Backtest</h3>

# In[6]:


begin_prices = []
end_prices = []
profits = 0

# Finding when a position is initiated and getting the open / close prices for the position
for i, row in df.iterrows():
    if row['position'] == 1:
        begin_prices.append(float(row['askopen']))
    if row['position'] == -1:
        end_prices.append(float(row['askopen']))

# Calculating the profit / loss using our pip cost and lot size
for i in range(len(begin_prices)):
    profit = (end_prices[i] - begin_prices[i]) * 100 * pip_cost * lot_size
    profits += profit
    print("The return for trade " + str(i + 1) + " is: " + str(int(profit)))
    
print("The return for the period is: " + str(int(profits)))


# <h3>A Better Backtest</h3>

# In[7]:


# Profit / loss figures are good, but they don't tell the whole story
# It's better to see what happens with the positions while they're open, as well

returns = 0

# Gets the number of pips that the market moved during the day
df['difference (pips)'] = (df['askclose'] - df['askopen']) * 100
#df['p/l'] = df['difference'] * pip_cost * lot_size

# Calculates the daily return while a position is active
# 'Total' column records our running profit / loss for the strategy
for i, row in df.iterrows():
    if row['signal'] == 1:
        returns += (row['difference (pips)'] * pip_cost * lot_size)
        df.loc[i,'total'] = returns
    else:
        df.loc[i,'total'] = returns


# In[8]:


# Check on the dataframe to see our newly created columns

df


# <h3>Visualizing Trading Signals</h3>

# In[9]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111,  ylabel='GBP/JPY Price')

# Plotting market prices and moving averages
df['askclose'].plot(ax=ax1, color='r', lw=1.)
df[['mva_fast', 'mva_slow']].plot(ax=ax1, lw=2.)

# Placing markers for our position entry
ax1.plot(df.loc[df.position == 1.0].index, 
         df.mva_fast[df.position == 1.0],
         '^', markersize=10, color='m')

# Placing markers for our position exit
ax1.plot(df.loc[df.position == -1.0].index, 
         df.mva_slow[df.position == -1.0],
         'v', markersize=10, color='k')

# Plotting our returns
#ax2 = ax1.twinx()
#ax2.grid(False)
#ax2.set_ylabel('Profits in $')
#ax2.plot(df['total'], color = 'green')

plt.show()


# <h3>Visualizing Returns</h3>

# In[10]:


fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111,  ylabel='Profits in $')

# Plotting our returns
df['total'].plot(ax=ax1, color='r', lw=1.)

# Placing markers for our position entry
ax1.plot(df.loc[df.position == 1.0].index, 
         df.total[df.position == 1.0],
         '^', markersize=10, color='m')

# Placing markers for our position exit
ax1.plot(df.loc[df.position == -1.0].index, 
         df.total[df.position == -1.0],
         'v', markersize=10, color='k')

plt.show()


# In[ ]:




