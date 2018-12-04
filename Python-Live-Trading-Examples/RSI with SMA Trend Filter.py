import fxcmpy
import time
import datetime as dt
from pyti.relative_strength_index import relative_strength_index as rsi
from pyti.simple_moving_average import simple_moving_average as sma

###### USER PARAMETERS ######
token = 'INSERT-TOKEN-HERE'
symbol = 'GBP/USD'
timeframe = "m1"	        # (m1,m5,m15,m30,H1,H2,H3,H4,H6,H8,D1,W1,M1)
rsi_periods = 14
upper_rsi = 70
lower_rsi = 30
sma_periods = 200
amount = 1
stop = -10
trailing_step = 1			# (1 = trailing stop, 0 = no trailing stop)
limit = 30
#############################

# Global Variables
pricedata = None
numberofcandles = 300

# Connect to FXCM API
con = fxcmpy.fxcmpy(access_token=token, log_level="error")
	
# This function runs once at the beginning of the strategy to run initial one-time processes/computations
def Prepare():
	global pricedata
	
	print("Requesting Initial Price Data...")
	pricedata = con.get_candles(symbol, period=timeframe, number=numberofcandles)
	print(pricedata)
	print("Initial Price Data Received...")

# Get latest close bar prices and run Update() function every close of bar/candle
def StrategyHeartBeat():
	while True:
		currenttime = dt.datetime.now()
		if timeframe == "m1" and currenttime.second == 0 and GetLatestPriceData():
			Update()
		elif timeframe == "m5" and currenttime.second == 0 and currenttime.minute % 5 == 0 and GetLatestPriceData(): 
			Update()
			time.sleep(240)
		elif timeframe == "m15" and currenttime.second == 0 and currenttime.minute % 15 == 0 and GetLatestPriceData(): 
			Update()
			time.sleep(840)
		elif timeframe == "m30" and currenttime.second == 0 and currenttime.minute % 30 == 0 and GetLatestPriceData():
			Update()
			time.sleep(1740)
		elif currenttime.second == 0 and currenttime.minute == 0 and GetLatestPriceData():
			Update()
			time.sleep(3540)
		time.sleep(1)

# Returns True when pricedata is properly updated			
def GetLatestPriceData():
	global pricedata
	
	# Normal operation will update pricedata on first attempt
	new_pricedata = con.get_candles(symbol, period=timeframe, number=numberofcandles)
	if new_pricedata.index.values[len(new_pricedata.index.values)-1] != pricedata.index.values[len(pricedata.index.values)-1]:
		pricedata= new_pricedata
		return True
		
	counter = 0
	# If data is not available on first attempt, try up to 3 times to update pricedata
	while new_pricedata.index.values[len(new_pricedata.index.values)-1] == pricedata.index.values[len(pricedata.index.values)-1] and counter < 3:
		print("No updated prices found, trying again in 10 seconds...")
		counter+=1
		time.sleep(10)
		new_pricedata = con.get_candles(symbol, period=timeframe, number=numberofcandles)
	if new_pricedata.index.values[len(new_pricedata.index.values)-1] != pricedata.index.values[len(pricedata.index.values)-1]:
		pricedata = new_pricedata
		return True
	else:
		return False		

# This function is run every time a candle closes
def Update():
	print(str(dt.datetime.now()) + "	 " + timeframe + " Bar Closed - Running Update Function...")
	
	# Calculate Indicators
	iRSI = rsi(pricedata['bidclose'], rsi_periods)
	iSMA = sma(pricedata['bidclose'], sma_periods)
	
	# Print Price/Indicators Data
	print("Close Price: " + str(pricedata['bidclose'][len(pricedata)-1]))
	print("RSI: " + str(iRSI[-1]))
	print("SMA: " + str(iSMA[-1]))
	
	# Trading Logic
	
	# Buy Logic, if RSI crosses above lower_rsi, and  close price is above SMA, then BUY
	if crossesOver(iRSI, lower_rsi) and pricedata['bidclose'][-1] > iSMA[-1]:
		# Buy Signal
		if countOpenTrades("B") == 0:
			enter("B")
		if countOpenTrades("S") != 0:
			exit("S")
		
	# Sell Logic, if RSI crosses under upper_rsi, and close price is below SMA, then SELL
	if crossesUnder(iRSI, upper_rsi) and pricedata['bidclose'][-1] < iSMA[-1]:
		# Sell Signal
		if countOpenTrades("S") == 0:
			enter("S")
		if countOpenTrades("B") != 0:
			exit("B")

	print(str(dt.datetime.now()) + "	 " + timeframe + " Update Function Completed.\n")

# Returns true if stream1 crossed over stream2 in most recent candle, stream2 can be integer/float or data array
def crossesOver(stream1, stream2):
	# If stream2 is an int or float, check if stream1 has crossed over that fixed number
	if isinstance(stream2, int) or isinstance(stream2, float):
		if stream1[len(stream1)-1] <= stream2:
			return False
		else:
			if stream1[len(stream1)-2] > stream2:
				return False
			elif stream1[len(stream1)-2] < stream2:
				return True
			else:
				x = 2
				while stream1[len(stream1)-x] == stream2:
					x = x + 1
				if stream1[len(stream1)-x] < stream2:
					return True
				else:
					return False
	# Check if stream1 has crossed over stream2
	else:
		if stream1[len(stream1)-1] <= stream2[len(stream2)-1]:
			return False
		else:
			if stream1[len(stream1)-2] > stream2[len(stream2)-2]:
				return False
			elif stream1[len(stream1)-2] < stream2[len(stream2)-2]:
				return True
			else:
				x = 2
				while stream1[len(stream1)-x] == stream2[len(stream2)-x]:
					x = x + 1
				if stream1[len(stream1)-x] < stream2[len(stream2)-x]:
					return True
				else:
					return False

# Returns true if stream1 crossed under stream2 in most recent candle, stream2 can be integer/float or data array
def crossesUnder(stream1, stream2):
	# If stream2 is an int or float, check if stream1 has crossed under that fixed number
	if isinstance(stream2, int) or isinstance(stream2, float):
		if stream1[len(stream1)-1] >= stream2:
			return False
		else:
			if stream1[len(stream1)-2] < stream2:
				return False
			elif stream1[len(stream1)-2] > stream2:
				return True
			else:
				x = 2
				while stream1[len(stream1)-x] == stream2:
					x = x + 1
				if stream1[len(stream1)-x] > stream2:
					return True
				else:
					return False
	# Check if stream1 has crossed under stream2
	else:
		if stream1[len(stream1)-1] >= stream2[len(stream2)-1]:
			return False
		else:
			if stream1[len(stream1)-2] < stream2[len(stream2)-2]:
				return False
			elif stream1[len(stream1)-2] > stream2[len(stream2)-2]:
				return True
			else:
				x = 2
				while stream1[len(stream1)-x] == stream2[len(stream2)-x]:
					x = x + 1
				if stream1[len(stream1)-x] > stream2[len(stream2)-x]:
					return True
				else:
					return False

# This function places a market order in the direction BuySell, "B" = Buy, "S" = Sell, uses symbol, amount, stop, limit
def enter(BuySell):
	direction = True;
	if BuySell == "S":
		direction = False;
	try:
		opentrade = con.open_trade(symbol=symbol, is_buy=direction,amount=amount, time_in_force='GTC',order_type='AtMarket',is_in_pips=True,limit=limit, stop=stop, trailing_step=trailing_step)
	except:
		print("	  Error Opening Trade.")
	else:
		print("	  Trade Opened Successfully.")


# This function closes all positions that are in the direction BuySell, "B" = Close All Buy Positions, "S" = Close All Sell Positions, uses symbol
def exit(BuySell=None):
	openpositions = con.get_open_positions(kind='list')
	isbuy = True
	if BuySell == "S":
		isbuy = False
	for position in openpositions:
		if position['currency'] == symbol:
			if BuySell is None or position['isBuy'] == isbuy:
				print("	  Closing tradeID: " + position['tradeId'])
				try:
					closetrade = con.close_trade(trade_id=position['tradeId'], amount=position['amountK'])
				except:
					print("	  Error Closing Trade.")
				else:
					print("	  Trade Closed Successfully.")


# Returns number of Open Positions for symbol in the direction BuySell, returns total number of both Buy and Sell positions if no direction is specified
def countOpenTrades(BuySell=None):		
	openpositions = con.get_open_positions(kind='list')
	isbuy = True
	counter = 0
	if BuySell == "S":
		isbuy = False
	for position in openpositions:
		if position['currency'] == symbol:
			if BuySell is None or position['isBuy'] == isbuy:
				counter+=1
	return counter








Prepare() # Initialize strategy
StrategyHeartBeat() # Run strategy
