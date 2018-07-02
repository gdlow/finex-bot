#main.py
import time
from botstrategy import BotStrategy

def main():
	strategy = BotStrategy()
	#implementation starts
	while True:
		strategy.tick()
		strategy.evaluatePositions()
		#graphing EMAs and MACD indicator:
		strategy.output.macdrsiplot(strategy.graphdataPoints, strategy.EMA9, strategy.MACD, strategy.cumulatedProfits)
		time.sleep(60) #define timestamp period


if __name__ == "__main__":
	main()