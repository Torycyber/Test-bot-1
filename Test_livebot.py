import ccxt
import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta
import pytz
import tulipy
import time
import os

Apikey=os.getenv('money_printer1_Apikeys')
Apisecret=os.getenv('money_printer1_Apikey')

exchange=ccxt.binance({
'apikey':'Apikey',
'secret':'Apisecret',
'enableRateLimit:True,
'options':{
'defaultType':'futures'}
})
exchange.loadMarkets()

symbol=BTCUSDT
leverage=75
exchange.setLeverage(leverage,symbol)



def create_since(days,mins):
	timezone=pytz.utc()
	Now=dt.now(timezone)
	since=Now-timedelta(days=1*days,minutes=1*mins)
	starttime=int(since.timestamp()*1000)
	return starttime

def create_endtime():
	timezone=pytz.utc()
	Now=dt.now(timezone)
	end=Now
	endtime=int(end.timestamp()*1000)
	return endttime
	
def fetch_data(symbol,timeframe,days,mins):
	since=create_since(days,mins)
	endtime=create_endtime()
	all_candles=[]
	while since<endtime:
		try:
			candles=exchange.fetchOHLCV(symbol,timeframe,since)
			if not candles:
				break
			all_candles.extend(candles)
			since=int(candles[-1][0]+1)
			if since>=endtime:
				break
			except ccxt.NetworkError as e:
				return []
			timesleep(1)
	df=pd.Dataframe(all_candles,columns=['timestamp','open','high','low','close','volume'])
	data=np.array(df)
	return data

def calculate_mins(timeframe,periods):
			units=timeframe[-1]
			value=float(timeframe[:-1])
			if units== 'm':
				return value *period
			if units== 'h':
				return value * period* 60
			if units== 'd':
				return value * period * 60 *24

def calculate_indicators(symbol,timeframe,days,indicators,**kwargs):
			period=kwargs.get('period')
			stddev=kwargs.get('stddev')
			mins=calculate_mins(timeframe,period)
			Data=fetch_data(symbol,timeframe,days,mins)
			
			if indicators=='sma':
				ma= ti.sma(Data[:,4],period)
				return ma
			elif indicators='bbands':
				bbands=ti.bbands(Data[:,4],period,stddev)
				return bbands
				
Data=fetch_data(symbol,timeframe='3m',days=1,mins=0)
print(Data)

type=market # OCO
side=buy
amount=0.1
param={
'stopLoss':{
	'price':'SL',
    'triggerprice':'SL_TG',
},
'takeprofit':{
	 'price': 'Tp',
	 'triggerprice':'Tp_Tg'
},
{'timeInForce':'GTC'}
}
#order=exchange.createOrders(symbol,type,side,amount,param)
#order=exchange.createOrderWithTakeProfitAndStopLoss(symbol,type,side,amount,param)

#order=createMarketBuyOrder(symbol,amount)
#order=createMarketSellOrder(symbol,amount)


def check_for_open_orders(symbol):
			try:
				open_orders=exchange.fetchOpenOrders(symbol)
				if len(open_orders)==0:
					return 0
				if len(open_orders)>0:
					return 1
				except ccxt.NetworkError:
					print('network')
check_opens=check_for_orders(symbol)
print(check_opens)

def check_positions(symbol):
	try:
		positions=exchange.fetchPositions(symbol)
		if len(positions)>0:
			return positions
		else:
			return []
	except ccxt.NetworkError:
		return []
positions=check_positions(symbol)

print(positions)
#close_order = createOrder(symbol,amount,side=sell)
print(close_order)
positions=check_positions(symbol)
