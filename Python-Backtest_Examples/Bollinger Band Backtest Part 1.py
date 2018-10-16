
# coding: utf-8

# In[1]:


import fxcmpy
import pandas as pd
import numpy as np
import datetime as dt

#we import the functions of the Bollinger band
from pyti.bollinger_bands import upper_bollinger_band as ubb
from pyti.bollinger_bands import middle_bollinger_band as mbb
from pyti.bollinger_bands import lower_bollinger_band as lbb
from pyti.bollinger_bands import percent_bandwidth as percent_b

#import plots and styling
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('ggplot')

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[2]:


socket = fxcmpy.fxcmpy(config_file = 'fxcm.cfg')
print (socket.get_instruments_for_candles())


# In[3]:


data = socket.get_candles(instrument = 'GBP/USD', period = 'D1', start = dt.datetime(2016,1,1), end = dt.datetime(2018, 6, 10))


# In[5]:


data['upper_band'] = ubb(data['askclose'], period = 20)
data['mid_band'] = mbb(data['askclose'], period = 20 )
data['lower_band'] = lbb(data['askclose'], period = 20 )
data['percent_b'] = percent_b(data['askclose'], period =20)


# In[6]:


data


# In[7]:


fig = plt.figure(figsize=(12,8))

ax1 = fig.add_subplot(111,  xlabel = 'Date',ylabel='Close')

data['askclose'].plot(ax=ax1, color='r', lw=1)
data['upper_band'].plot(ax=ax1, color = 'b', lw= 1)
data['mid_band'].plot(ax=ax1, color = 'g', lw= 1)
data['lower_band'].plot(ax=ax1, color = 'y', lw= 1)


# In[8]:


band_fig = plt.figure(figsize=(12,8))
ax2 = band_fig.add_subplot(111,  ylabel='%B')
data['percent_b'].plot(ax=ax2, color = 'b', lw= 1)


# In[9]:


data['signal'] = np.where((data['percent_b'] >.2),1,0)
data['position'] = data['signal'].diff()
data


# In[10]:


pip_cost = 1
lot_size = 10

returns = 0

# Gets the number of pips that the market moved during the day
data['difference (pips)'] = (data['askclose'] - data['askopen']) * 100
#df['p/l'] = df['difference'] * pip_cost * lot_size

# Calculates the daily return while a position is active
# 'Total' column records our running profit / loss for the strategy
CountPL=False
for i, row in data.iterrows():
  if CountPL==True:
    returns += (row['difference (pips)'] * pip_cost * lot_size)
    data.loc[i,'total'] = returns
  else:
    data.loc[i,'total'] = returns

  if row['signal'] == 1:
    CountPL=True
  else:
    CountPL=False
data


# In[11]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111, ylabel='Profits in $')

data['total'].plot(ax=ax1, color='r', lw=1.)

# Placing markers for our position entry
ax1.plot(data.loc[data.position == 1.0].index,
    data.total[data.position == 1.0],
    '^', markersize=10, color='m')

# Placing markers for our position exit

ax1.plot(data.loc[data.position == -1.0].index,
    data.total[data.position == -1.0],
    'v', markersize=10, color='k')

plt.show()

