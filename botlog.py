from termcolor import colored
import colorama
import plotly
plotly.plotly.sign_in(username='geraldlow7', api_key='GNOcmxGffCMYyzHXZJuB')
stream_tokens = ['u89ukk5e8r','kn4zw6qccw','hkfoxrwzsz','4r8nh5203d','48s4a4nvxu','6lvg791a6u','qmlh3dpj39','k5xydfxair','sathxv0gi8','lafx97wb97','uxuhh7cuxf']
import numpy as np
import pandas as pd
colorama.init()

class BotLog(object):
	def __init__(self):
		pass

	def log(self, message):
		print (message)

	def color(self,message,color):
		return (colored(message,color))

	def macdrsiplot(self,dataPoints, EMA9, MACD, cumulatedProfits):
		#instantiate stream_ids
		token_1 = stream_tokens[-1]
		token_2 = stream_tokens[-2]
		token_3 = stream_tokens[-3]
		token_4 = stream_tokens[-4]
		token_5 = stream_tokens[-5]
		token_6 = stream_tokens[-6]
		token_7 = stream_tokens[-7]
		token_8 = stream_tokens[-8]
		token_9 = stream_tokens[-9]
		token_10 = stream_tokens[-10]
		token_11 = stream_tokens[-11]
		stream_id1 = dict(token=token_1, maxpoints=200)
		stream_id2 = dict(token=token_2, maxpoints=200)
		stream_id3 = dict(token=token_3, maxpoints=200)
		stream_id4 = dict(token=token_4, maxpoints=200)
		stream_id5 = dict(token=token_5, maxpoints=200)
		stream_id6 = dict(token=token_6, maxpoints=200)
		stream_id7 = dict(token=token_7, maxpoints=200)
		stream_id8 = dict(token=token_8, maxpoints=200)
		stream_id9 = dict(token=token_9, maxpoints=200)
		stream_id10 = dict(token=token_10, maxpoints=200)
		stream_id11 = dict(token=token_11, maxpoints=200)

		trace0 = plotly.graph_objs.Scatter(
			x = dataPoints['date'],
			y = dataPoints['price'],
			name = 'price',
			stream = stream_id1
			)
		trace1 = plotly.graph_objs.Scatter(
			x = dataPoints['date'],
			y = dataPoints['long'],
			mode = 'markers+text',
			name = 'LONG positions',
			text = 'LONG',
			textposition = 'bottom',
			stream = stream_id2
			)
		trace2 = plotly.graph_objs.Scatter(
			x = dataPoints['date'],
			y = dataPoints['closedlong'],
			mode = 'markers+text',
			name = 'CLOSED LONG positions',
			text = 'CLOSE LONG',
			textposition = 'bottom',
			stream = stream_id3
			)
		trace3 = plotly.graph_objs.Scatter(
			x = dataPoints['date'],
			y = dataPoints['short'],
			mode = 'markers+text',
			name = 'SHORT positions',
			text = 'SHORT',
			textposition = 'bottom',
			stream = stream_id4
			)
		trace4 = plotly.graph_objs.Scatter(
			x = dataPoints['date'],
			y = dataPoints['closedshort'],
			mode = 'markers+text',
			name = 'CLOSED SHORT positions',
			text = 'CLOSE SHORT',
			textposition = 'bottom',
			stream = stream_id5
			)
		trace5 = plotly.graph_objs.Scatter(
			x = dataPoints['date'],
			y = MACD,
			name = 'MACD indicator',
			stream = stream_id6
			)
		trace6 = plotly.graph_objs.Scatter(
			x = dataPoints['date'],
			y = EMA9,
			name = 'EMA9 indicator',
			stream = stream_id7
			)
		trace7 = plotly.graph_objs.Scatter(
			x = dataPoints['date'],
			y = dataPoints['sma'],
			name = '200 SMA',
			stream = stream_id8
			)
		trace8 = plotly.graph_objs.Scatter(
			x = dataPoints['date'],
			y = dataPoints['rsi'],
			name = 'RSI',
			stream = stream_id9
			)
		trace9 = plotly.graph_objs.Scatter(
			x = dataPoints['date'],
			y = [70 for i in np.arange(len(dataPoints['date']))],
			name = 'RSImax',
			stream = stream_id10
			)
		trace10 = plotly.graph_objs.Scatter(
			x = dataPoints['date'],
			y = [30 for i in np.arange(len(dataPoints['date']))],
			name = 'RSImin',
			stream = stream_id11
			)
		fig = plotly.tools.make_subplots(rows=3, cols=1, specs=[[{}], [{}], [{}]],
		                          shared_xaxes=True, shared_yaxes=True,
		                          vertical_spacing=0.001)
		fig.append_trace(trace0, 1, 1)
		fig.append_trace(trace1, 1, 1)
		fig.append_trace(trace2, 1, 1)
		fig.append_trace(trace3, 1, 1)
		fig.append_trace(trace4, 1, 1)
		fig.append_trace(trace7, 1, 1)
		fig.append_trace(trace5, 2, 1)
		fig.append_trace(trace6, 2, 1)
		fig.append_trace(trace8, 3, 1)
		fig.append_trace(trace9, 3, 1)
		fig.append_trace(trace10, 3, 1)

		fig['layout'].update(title="Cumulated Profits: {}".format(round(cumulatedProfits,2)))
		plotly.plotly.plot(fig, filename='crypto-macd-rsi')
		plotly.plotly.Stream(stream_id=token_1).open()
		plotly.plotly.Stream(stream_id=token_2).open()
		plotly.plotly.Stream(stream_id=token_3).open()
		plotly.plotly.Stream(stream_id=token_4).open()
		plotly.plotly.Stream(stream_id=token_5).open()
		plotly.plotly.Stream(stream_id=token_6).open()
		plotly.plotly.Stream(stream_id=token_7).open()
		plotly.plotly.Stream(stream_id=token_8).open()
		plotly.plotly.Stream(stream_id=token_9).open()
		plotly.plotly.Stream(stream_id=token_10).open()
		plotly.plotly.Stream(stream_id=token_11).open()


