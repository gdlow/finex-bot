#db.py
import sqlalchemy
import pandas as pd

class TradeDatabase(object):
	def __init__(self):
		pass

	def connect(self):
		'''Returns a connection and a metadata object'''
		# We connect with the help of the PostgreSQL URL
		self.url = 'postgres://lpzqiiuvnsltmv:5cb622f61b28fff5acc5345387355c923babd9d846afbd02e6bacc54ec32b694@ec2-107-22-211-182.compute-1.amazonaws.com:5432/did369bmda40b'

		# The return value of create_engine() is our connection object
		self.con = sqlalchemy.create_engine(self.url, client_encoding='utf8')

		# We then bind the connection to MetaData()
		self.meta = sqlalchemy.MetaData(bind=self.con, reflect=True)
		#table
		self.db = self.meta.tables['tick']

	def insertStatement01(self, date, price):
		insert_statement = self.db.insert().values(date=date,price=price)
		self.con.connect().execute(insert_statement)

	def insertStatement02(self, date, trend, SMA, RSI):
		update_statement = self.db.update().where(self.db.c.date==date).values(trend=trend,sma=SMA,rsi=RSI)
		self.con.connect().execute(update_statement)

	def insertStatement03(self, date, cryptoamount, long, tradePlaced, typeOfTrade):
		update_statement = self.db.update().where(self.db.c.date==date).values(cryptoamount=cryptoamount,long=long,tradeplaced=tradePlaced,typeoftrade=typeOfTrade)
		self.con.connect().execute(update_statement)

	def insertStatement04(self, date, cryptoamount, short, tradePlaced, typeOfTrade):
		update_statement = self.db.update().where(self.db.c.date==date).values(cryptoamount=cryptoamount,short=short,tradeplaced=tradePlaced,typeoftrade=typeOfTrade)
		self.con.connect().execute(update_statement)

	def insertStatement05(self, date, netProfit):
		update_statement = self.db.update().where(self.db.c.date==date).values(netprofits=netProfit)
		self.con.connect().execute(update_statement)

	def insertStatement06(self, date, closedLong, tradePlaced):
		update_statement = self.db.update().where(self.db.c.date==date).values(closedlong=closedLong,tradeplaced=tradePlaced)
		self.con.connect().execute(update_statement)

	def insertStatement07(self, date, closedShort, tradePlaced):
		update_statement = self.db.update().where(self.db.c.date==date).values(closedshort=closedShort,tradeplaced=tradePlaced)
		self.con.connect().execute(update_statement)

	def frameit(self):
		self.df = pd.read_sql_table('tick', self.con)
		self.df = self.df.sort_values(by='date')
		return self.df

	def readtolist01(self):
		self.df = pd.read_sql_table('tick', self.con)
		self.df = self.df.sort_values(by='date')
		self.datelist = self.df['date'].tolist()
		self.pricelist = self.df['price'].tolist()
		return self.datelist, self.pricelist

	def readtolist02(self):
		self.df = pd.read_sql_table('tick', self.con)
		self.df = self.df.sort_values(by='date')
		self.typeoftradelist = self.df['typeoftrade'].tolist()
		self.tradeplacedlist = self.df['tradeplaced'].tolist()
		self.cryptoamountlist = self.df['cryptoamount'].tolist()
		return self.tradeplacedlist, self.typeoftradelist, self.cryptoamountlist

	def cumwinloss(self):
		self.df = pd.read_sql_table('tick', self.con)
		self.netprofitslist = self.df['netprofits'].tolist()
		self.netprofitslist = [i for i in self.netprofitslist if i*0 == 0]
		self.cumulatedprofits = sum(self.netprofitslist)
		self.numofwins = len([i for i in self.netprofitslist if i > 0])
		self.numofloses = len([i for i in self.netprofitslist if i < 0])
		return self.cumulatedprofits, self.numofwins, self.numofloses

	def closecon(self):
		self.con.dispose()
