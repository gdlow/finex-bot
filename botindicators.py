import numpy

class BotIndicators(object):
	def __init__(self):
		 self.localMax = []
		 self.currentResistance = 0.0

	def movingAverage(self, dataPoints, period):
		if (len(dataPoints) > 1):
			return sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))

	def trendline(self, dataPoints):
		if (len(dataPoints) > 2):
			if ( (len(dataPoints) > 2) and (dataPoints[-2]> dataPoints[-1]) and (dataPoints[-2]> dataPoints[-3]) ): #local maxima
				self.localMax.append(dataPoints[-2])
				numberOfSimilarLocalMaxes = 0
				for oldMax in self.localMax[-7:]: #checking for localmax list to see if any are around the same maxima
					if ( (float(oldMax) > (float(dataPoints[-2]) - 5) ) and (float(oldMax) < (float(dataPoints[-2]) + 5) ) ):
						numberOfSimilarLocalMaxes += 1
				if (numberOfSimilarLocalMaxes > 3): #if more than 3 (inclusive) (i.e. 2 others) maxima around the area, establish trendline
					self.currentResistance = dataPoints[-2]
					return self.currentResistance
			else:
				return self.currentResistance #return previous resistance value
		else:
			self.currentResistance = dataPoints[-1] #starting trendline point; for graphing purposes
			return self.currentResistance

	def momentum(self, dataPoints, period=14):
		if (len(dataPoints) > period -1):
			return dataPoints[-1] * 100 / dataPoints[-period]

	def EMA(self, prices, period):
		x = numpy.asarray(prices)
		weights = None
		weights = numpy.exp(numpy.linspace(-1., 0., period))
		weights /= weights.sum() #calculates average

		a = numpy.convolve(x, weights, mode='full')[:len(x)]
		a[:period] = a[period]
		return a

	def MACD(self, prices, nslow=26, nfast=12):
		emaslow = self.EMA(prices, nslow)
		emafast = self.EMA(prices, nfast)
		return emaslow, emafast, emafast - emaslow		

	def RSI (self, prices, period=14):
		deltas = numpy.diff(prices)
		seed = deltas[:period+1]
		up = seed[seed >= 0].sum()/period
		down = -seed[seed < 0].sum()/period
		rs = up/down
		rsi = numpy.zeros_like(prices)
		rsi[:period] = 100. - 100./(1. + rs)
 
		for i in range(period, len(prices)):
 			delta = deltas[i - 1]  # cause the diff is 1 shorter
 			if delta > 0:
 				upval = delta
 				downval = 0.
 			else:
 				upval = 0.
 				downval = -delta
 
 			up = (up*(period - 1) + upval)/period
 			down = (down*(period - 1) + downval)/period
 			rs = up/down
 			rsi[i] = 100. - 100./(1. + rs)

		if len(prices) > period:
 			return rsi[-1]
		else:
			return 50 # output a neutral amount until enough prices in list to calculate RSI
