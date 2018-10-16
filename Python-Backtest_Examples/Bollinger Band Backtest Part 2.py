
# coding: utf-8

# In[1]:



#Create imports for modules
import fxcmpy
import pandas as pd
import numpy as np
import datetime as dt

#import funcs
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


# In[3]:


#Establish connection using python-wrapper and config file
socket = fxcmpy.fxcmpy(config_file = 'fxcm.cfg')
print (socket.get_instruments_for_candles())


# In[5]:


data = socket.get_candles(instrument = 'GBP/USD', period = 'D1', start = dt.datetime(2016,1,1), end = dt.datetime(2018, 6, 10))


# In[6]:


#Define useful variables


data['upper_band'] = ubb(data['askclose'], period = 20)
data['mid_band'] = mbb(data['askclose'], period = 20 )
data['lower_band'] = lbb(data['askclose'], period = 20 )
data['percent_b'] = percent_b(data['askclose'], period =20)
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


#For reference
#%B Above 1 = Price is Above the Upper Band
#%B Equal to 1 = Price is at the Upper Band
#%B Above .50 = Price is Above the Middle Line
#%B Below .50 = Price is Below the Middle Line
#%B Equal to 0 = Price is at the Lower Band
#%B Below 0 = Price is Below the Lower Band
#%B Above .80 = Price is Nearing the Upper Band
#%B Below .20 = Price is Nearing the Lower Band


# In[10]:


#Define the strategy
buy_prices = []
sell_prices = []

order = False
for i, row in data.iterrows():
    #buy
    if row['percent_b'] <= .2 and order == False:
        print("Create buy order since percent_b under 20%")
        print("Price bought: " +str(float(row['askopen'])))
        buy_prices.append(float(row['askopen']))
        order = True
    if row['percent_b'] >= .75 and order == True:
        print("Create sell order since percent_b over 80%")
        print("Price sold: " +str(float(row['askopen'])))
        sell_prices.append(float(row['askopen']))
        order = False


# In[11]:


data


# In[12]:



buy_prices


# In[13]:



sell_prices


# In[16]:


pip_cost = 1
lot_size = 10
profits = 0
for i in range(len(buy_prices)-1):
    profit = (sell_prices[i] - buy_prices[i]) * 100 * pip_cost * lot_size
    
    profits += profit
    print("The return for trade " + str(i + 1) + " is: " + str(round(profit,2)))
    
print("The return for the period is: " + str(round(profits,2)))

