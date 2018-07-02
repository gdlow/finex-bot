#for BitFinex
#botstrategy.py
import FinexAPI
from botindicators import BotIndicators
from botlog import BotLog 
import datetime, time
import pandas as pd
from db import TradeDatabase

class BotStrategy(object):
	def __init__(self):
		#connect; read and write to db
		self.TradeDatabase = TradeDatabase()
		self.TradeDatabase.connect()
		#amount to trade (capital):
		self.amountInUSD = 300
		#prices information
		self.prices = []
		self.currentPrice = ""
		#graph and indicators
		self.output = BotLog()
		self.indicators = BotIndicators()
		#self.graphdataPoints = []
		self.dataDate = ""
		self.SMA = ""
		self.CResistance = 0.0
		self.EMA9 = []
		self.MACD = []
		#trade details
		self.tradePlaced = []
		self.typeOfTrade = []
		self.cumulatedProfits = 0.0
		#wins and loses
		self.numofwins = 0
		self.numofloses = 0

	def tick(self):
		#only call API once
		try:
			self.APIlist = FinexAPI.ticker()
		except:
			try:
				time.sleep(10)
				self.APIlist = FinexAPI.ticker()
			except:
				try:
					time.sleep(10)
					self.APIlist = FinexAPI.ticker()
				except:
					pass

		#date
		self.dataDate = datetime.datetime.fromtimestamp(int(float(self.APIlist["timestamp"]))).strftime('%Y-%m-%d %H:%M:%S')
		#prices
		self.currentPrice = float(self.APIlist["last_price"])
		#insert into SQL db
		self.TradeDatabase.insertStatement01(self.dataDate, self.currentPrice)
		#load datelist, prices from db
		self.datelist, self.prices = self.TradeDatabase.readtolist01()

		#indicators
		self.SMA = self.indicators.movingAverage(self.prices,200)
		self.CResistance = self.indicators.trendline(self.prices)
		self.RSI = self.indicators.RSI(self.prices)

		#macd indicators & insert into DB
		if len(self.prices) > 26: #get macd indicators
			emaslow, emafast, self.MACD = self.indicators.MACD(self.prices)
			self.EMA9 = self.indicators.EMA(self.MACD,9)

		#Insert all to DB (no need for macd and ema9 - they are self generated and contained lists)
		self.TradeDatabase.insertStatement02(self.dataDate, self.CResistance, self.SMA, self.RSI)

		#graph
		#archaic : self.graphdataPoints.append({'date':self.dataDate, 'price': self.currentPrice, 'trend': self.CResistance, 'SMA': self.SMA, 'RSI':self.RSI, 'short': np.nan, 'long':np.nan,'closedLong':np.nan,'closedShort':np.nan})

		#graph with pdDataFrame obj
		self.graphdataPoints = self.TradeDatabase.frameit()

		#if/else indicators
		self.tradePlaced, self.typeOfTrade, self.cryptoAmount = self.TradeDatabase.readtolist02()
		self.tradePlaced = [i for i in self.tradePlaced if i*0 == 0] #only get the numbers 
		self.typeOfTrade = [i for i in self.typeOfTrade if i != None] #only get the strings
		self.cryptoAmount = [i for i in self.cryptoAmount if i*0 == 0] #only get the numbers

		#print timestamp and price to cmd line for logging purposes
		self.output.log(self.dataDate +"\tPrice: "+str(self.currentPrice)+"\tMoving Average: "+str(self.SMA))
		#print numofwins, numofloses and cumulated profits to cmd line
		self.cumulatedProfits, self.numofwins, self.numofloses = self.TradeDatabase.cumwinloss()
		self.output.log("No. of Wins: {}, No. of Loses: {}, Cumulated Profits: {}".format(self.numofwins, self.numofloses, self.cumulatedProfits))

	#decide when to buy and when to sell - MACD strat + 200 period SMA  - maybe can implement stops (?) GOLDEN GRAIL!!!
	def evaluatePositions(self):
		try:
			if len(self.tradePlaced) == 0 or self.tradePlaced[-1] == 0:
				#if market is bullish - only take buy signals
				if self.currentPrice > self.SMA:
					#MACD indicator - when EMA9 crosses higher than the MACD curve - buy
					if (len(self.MACD) > 1) and (self.EMA9[-2] < self.MACD[-2]) and (self.EMA9[-1] > self.MACD[-1]):
						self.buyposition()
				#elif market is bearish - only take sell signals
				elif self.currentPrice < self.SMA:
					#MACD indicator - when EMA9 crosses lower than the MACD curve - sell
					if (len(self.MACD) > 1) and (self.EMA9[-2] > self.MACD[-2]) and (self.EMA9[-1] < self.MACD[-1]):
						self.sellposition()
			elif self.typeOfTrade[-1] == "long":
				#MACD indicator - when EMA9 crosses lower than the MACD curve - sell
				if ( (self.EMA9[-2] > self.MACD[-2]) and (self.EMA9[-1] < self.MACD[-1]) and (self.cryptoAmount[-1] * self.currentPrice > 0.95 * self.amountInUSD)):
					self.closeLong()
				#if bullish trend ends and you are stuck, immediately sell to recoup loss
				elif self.currentPrice < self.SMA:
					self.closeLong()
			elif self.typeOfTrade[-1] == "short": 
				#MACD indicator - when EMA9 crosses higher than the MACD curve - buy
				if ( (self.EMA9[-2] < self.MACD[-2]) and (self.EMA9[-1] > self.MACD[-1]) and (0.996 * self.amountInUSD) > 0.95 * (self.currentPrice * self.cryptoAmount[-1])):
					self.closeShort()
				#if bearish trend ends and you are stuck, immediately buy to recoup loss
				elif self.currentPrice > self.SMA:
					self.closeShort()
		except TypeError:
			pass

	#buy and sell positions
	def buyposition(self):
		amountincryptos = 0.996 * float(self.amountInUSD) / self.currentPrice
		self.output.log("BUY {} Cryptos at {}USD".format(amountincryptos,self.amountInUSD))
		self.TradeDatabase.insertStatement03(self.dataDate, amountincryptos,self.currentPrice,1,"long")

	def sellposition(self):
		amountincryptos = float(self.amountInUSD) / self.currentPrice
		self.output.log("SELL {} Cryptos at {}USD".format(amountincryptos,self.amountInUSD))
		self.TradeDatabase.insertStatement04(self.dataDate, amountincryptos,self.currentPrice,1,"short")

	def closeLong(self):
		netProfit = self.cryptoAmount[-1] * self.currentPrice - self.amountInUSD
		self.TradeDatabase.insertStatement05(self.dataDate, netProfit)
		self.cumulatedProfits, self.numofwins, self.numofloses = self.TradeDatabase.cumwinloss()
		self.TradeDatabase.insertStatement06(self.dataDate, self.currentPrice,0)
		if netProfit >= 0:
			self.output.log("Closed LONG ORDER at {}".format(self.currentPrice) + self.output.color("\tNet Profit: {}".format(netProfit),'green') + "\tCumulated Profits: {}".format(self.cumulatedProfits))
			self.output.log("No. of Wins: {}, No. of Loses: {}, Win Rate: {}".format(self.numofwins, self.numofloses,  round(self.numofwins/(self.numofwins + self.numofloses),2)))
		else:
			self.output.log("Closed LONG ORDER at {}".format(self.currentPrice) + self.output.color("\tNet Profit: {}".format(netProfit),'red') + "\tCumulated Profits: {}".format(self.cumulatedProfits))
			self.output.log("No. of Wins: {}, No. of Loses: {}, Win Rate: {}".format(self.numofwins,self.numofloses, round(self.numofwins/(self.numofwins + self.numofloses),2)))

	def closeShort(self):
		netProfit = (0.996 * self.amountInUSD) - (self.currentPrice * self.cryptoAmount[-1])
		self.TradeDatabase.insertStatement05(self.dataDate, netProfit)
		self.cumulatedProfits, self.numofwins, self.numofloses = self.TradeDatabase.cumwinloss()
		self.TradeDatabase.insertStatement07(self.dataDate, self.currentPrice,0)
		if netProfit >= 0:
			self.output.log("Closed SHORT ORDER at {}".format(self.currentPrice) + self.output.color("\tNet Profit: {}".format(netProfit),'green') + "\tCumulated Profits: {}".format(self.cumulatedProfits))
			self.output.log("No. of Wins: {}, No. of Loses: {}, Win Rate: {}".format(self.numofwins,self.numofloses,  round(self.numofwins/(self.numofwins + self.numofloses),2)))
		else:
			self.output.log("Closed SHORT ORDER at {}".format(self.currentPrice) + self.output.color("\tNet Profit: {}".format(netProfit),'red') + "\tCumulated Profits: {}".format(self.cumulatedProfits))
			self.output.log("No. of Wins: {}, No. of Loses: {}, Win Rate: {}".format(self.numofwins,self.numofloses,  round(self.numofwins/(self.numofwins + self.numofloses),2)))


