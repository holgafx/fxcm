import fxcmpy
import time
import datetime as dt

###### USER PARAMETERS ######
token = 'INSERT-TOKEN-HERE'
symbol = 'BTC/USD'
timeframe = "H1"	        # (m1,m5,m15,m30,H1,H2,H3,H4,H6,H8,D1,W1,M1)
channel_periods = 24
amount = 1
limitmultiplier = 1.5
#############################

# Global Variables
pricedata = None
numberofcandles = 300
channel_high = 0
channel_low = 0

# Connect to FXCM API
con = fxcmpy.fxcmpy(access_token=token, log_level="error")
	
# This function runs once at the beginning of the strategy to run initial one-time processes/computations
def Prepare():
	global pricedata
	global channel_high
	global channel_low
	
	print("Requesting Initial Price Data...")
	pricedata = con.get_candles(symbol, period=timeframe, number=numberofcandles)
	print(pricedata)	
	print("Initial Price Data Received...")
	
	# Calculate Initial Channel High/Low
	channel_high = max(pricedata['bidhigh'][-channel_periods:])
	channel_low = min(pricedata['bidlow'][-channel_periods:])
	print("	  Calculating Channel High/Low Values.")
	print("	  Channel High: " + str(channel_high))
	print("	  Channel Low: " + str(channel_low))

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
def Update(tickdata=None, tickdataframe=None):
	global channel_high
	global channel_low
	
	# Close of Bar Actions
	if tickdata == None:
		print(str(dt.datetime.now()) + "	 " + timeframe + " Bar Closed - Running Update Function...")
		
		# Update Channel High/Low
		channel_high = max(pricedata['bidhigh'][-channel_periods:])
		channel_low = min(pricedata['bidlow'][-channel_periods:])
		print("	  Calculating Channel High/Low Values.")
		print("	  Channel High: " + str(channel_high))
		print("	  Channel Low: " + str(channel_low))

		print(str(dt.datetime.now()) + "	 " + timeframe + " Update Function Completed.\n")
		
	# Tick Actions
	else:
	
		# Buy Logic - If price crosses over channel_high and we have no Buy trades open, Buy
		if crossesOver(tickdataframe['Bid'], channel_high) and countOpenTrades("B") == 0:
			print(str(dt.datetime.now()) + "	 Price Broke Above Channel. BUY SIGNAL!")
			print(str(dt.datetime.now()) + "	 Opening Buy Trade...")
			# Limit is distance between Channel High & Low mulitpled by limitmultiplier
			limit = channel_high + (channel_high - channel_low) * limitmultiplier
			enter("B",limit)
			if countOpenTrades("S") > 0:
				exit("S")
			
		# Sell Logic - If price crosses under channel_low and we have no Sell trades open, Sell
		if crossesUnder(tickdataframe['Bid'], channel_low) and countOpenTrades("S") == 0:
			print(str(dt.datetime.now()) + "	 Price Broke Below Channel. SELL SIGNAL!")
			print(str(dt.datetime.now()) + "	 Opening Sell Trade...")
			# Limit is distance between Channel High & Low mulitpled by limitmultiplier
			limit = channel_low - (channel_high - channel_low) * limitmultiplier
			enter("S",limit)
			if countOpenTrades("B") > 0:
				exit("B")

# This custom function places a market order in the direction BuySell, "B" = Buy, "S" = Sell, with a take profit set to limitprice, uses symbol, amount
def enter(BuySell,limitprice):
	direction = True;
	if BuySell == "S":
		direction = False;
	try:
		opentrade = con.open_trade(symbol=symbol, is_buy=direction,amount=amount, time_in_force='GTC',order_type='AtMarket',is_in_pips=False,limit=limitprice)
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
con.subscribe_market_data(symbol, (Update,)) # Subscribe to Tick Data
con.set_max_prices(100) # Set maximum number of most recent Ticks to store inside of dataframe
StrategyHeartBeat() # Run strategy