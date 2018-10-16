
# coding: utf-8

# In[1]:


import fxcmpy
import pandas as pd
import numpy as np
import datetime as dt

from pyti.stochastic import percent_k
from pyti.stochastic import percent_d
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib import style
style.use('ggplot')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[2]:


socket = fxcmpy.fxcmpy(config_file = 'fxcm.cfg')


# In[3]:


data = socket.get_candles(instrument = 'GBP/USD', period = 'D1', start = dt.datetime(2017,1,1), end = dt.datetime(2018, 6, 10))


# In[4]:


data['percent_k'] = percent_k(data['askclose'], 20)
data['percent_d'] = percent_d(data['askclose'], 20)


# In[7]:


fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111,  xlabel = 'Date',ylabel='Close')
data['askclose'].plot(ax=ax1, color='r', lw=1)

ss_plot = plt.figure(figsize=(50,8))
ax3 = ss_plot.add_subplot(111,  ylabel='Percent')
data['percent_k'].plot(ax=ax3, color='r')
data['percent_d'].plot(ax=ax3, color='g')
data['ovr'] = .80
data['ovr'].plot(ax=ax3, color = 'b', )
data['blw'] = .20
data['blw'].plot(ax=ax3, color = 'b',)


# In[8]:


data['signal'] = np.where(np.logical_and(data['percent_k'] > data['percent_d'], data['percent_k']>.8),1,0)
data['position'] = data['signal'].diff()
data


# In[9]:


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


# In[10]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(111, ylabel='Profits in $')
data['total'].plot(ax=ax1, color='r', lw=2.)

# Placing markers for our position entry
ax1.plot(data.loc[data.position == 1.0].index,
data.total[data.position == 1.0],
'*', markersize=8, color='g')

# Placing markers for our position exit
ax1.plot(data.loc[data.position == -1.0].index,
data.total[data.position == -1.0],
'*', markersize=8, color='b')
plt.show()

