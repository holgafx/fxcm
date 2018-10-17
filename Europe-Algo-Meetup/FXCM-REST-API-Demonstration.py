#!/usr/bin/env python
# coding: utf-8

# <h1>FXCM REST API Demonstration</h1>

# <h3>Connecting to FXCM REST API</h3>

# In[1]:


#import fxcmpy and check the imported version
import fxcmpy
import datetime as dt
fxcmpy.__version__

token = '50307dd4193e97c620b80984acbb5cfa6b489a77'

#Use the config file to connect to the API. 
con = fxcmpy.fxcmpy(access_token = token, log_level='error',log_file=None)

#The server is demo by default. THe options below are also available for usage.
#con = fxcmpy.fxcmpy(config_file='fxcm.cfg', server='demo')

#Connect to the API with a real account. Do not forget to change the access token in the config file.
#con = fxcmpy.fxcmpy(config_file='fxcm.cfg', server='real')


# <h3>Getting Instruments</h3>

# In[2]:


# All Tradable Instruments

con.get_instruments()


# In[3]:


# Instruments that your account is subscribed to

con.get_instruments_for_candles()


# <h3>Pulling Historical Prices</h3>
# 
# Available periods : 'm1', 'm5', 'm15', 'm30', 'H1', 'H2', 'H3', 'H4', 'H6', 'H8','D1', 'W1', or 'M1'.

# In[4]:


#Getting historical prices by specifying only the period.  

con.get_candles('EUR/JPY', period='m1')


# In[5]:


#Getting historical prices by specifying the number of results you would like to see.

con.get_candles('EUR/USD', period='m1', number=100)


# In[6]:


#Getting historical Prices by Specifying the start and the end date.

start = dt.datetime(2018, 1, 14)
stop = dt.datetime(2018, 5, 1)

con.get_candles('EUR/USD', period='D1',
                start=start, stop=stop)


# <h3>Streaming Real-time Prices</h3>

# In[7]:


# Subscribe To Market Data

con.subscribe_market_data('EUR/USD')


# In[8]:


# Once you are subscribed the fxcm.py collects the data in a pandas DataFrame. 

con.get_prices('EUR/USD')


# In[9]:


#To stop the stream and delete the dataframe

con.unsubscribe_market_data('EUR/USD')


# <h3>Executing Orders</h3>

# In[10]:


# Check whether you have an open positions already.

con.get_open_positions()


# In[11]:


# Create a market order

order = con.create_market_buy_order('USD/JPY', 10)


# In[12]:


#Checking The New Oen Position Table

con.get_open_positions().T


# In[13]:


# Place an order with more control over parameters

order2 = con.open_trade(symbol='EUR/JPY', is_buy=True,
                       rate=105, is_in_pips=False,
                       amount='10', time_in_force='GTC',
                       order_type='AtMarket', limit=150)


# <h3>Closing Orders</h3>

# In[15]:


# Close position by specifying the tradeId

pos = con.get_open_position(114496084)
pos.close()


# In[16]:


# Close positions by specifying the currency pair

con.close_all_for_symbol('USD/JPY')


# In[17]:


# CLose all the positions at once

con.close_all()


# In[ ]:




