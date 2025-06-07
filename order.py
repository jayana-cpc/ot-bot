import json
from enum import Enum
from typing import Any

class TTOrderType(Enum):
	LIMIT = 'Limit'
	MARKET = 'Market'
	STOP = 'Stop'

class TTPriceEffect(Enum):
	CREDIT = 'Credit'
	DEBIT = 'Debit'

class TTOrderStats(Enum):
	RECEIVED = 'Received'
	CANCELLED = 'Cancelled'
	FILLED = 'Filled'
	EXPIRED = 'Expired'
	LIVE = 'Live'
	REJECTED = 'Rejected'

class TTTimeInForce(Enum):
	DAY = 'Day'
	GTC = 'GTC'
	GTD = 'GTD'

class TTInstrumentType(Enum):
	EQUITY = 'Equity'
	EQUITY_OPTION = 'Equity Option'
	FUTURE = 'Future'
	FUTURE_OPTION = 'Future Option'
	NOTIONAL_MARKET = 'Notional Market'

class TTLegAction(Enum):
	STO = 'Sell to Open'
	STC = 'Sell to Close'
	BTO = 'Buy to Open'
	BTC = 'Buy to Close'

class TTOptionSide(Enum):
	PUT = 'P'
	CALL = 'C'

class TTOption:

	def __init__(self, symbol: str, exp: str, side: TTOptionSide, strike: float) -> None:
		symbol = symbol + (' ' * (6 - len(symbol)))
		strike = float(('0'* (8 - len(str(strike * 1000)))) + str(strike * 1000))
		exp = exp.split('-')[0][2:] + exp.split('-')[1] + exp.split('-')[2]
		self.symbol = symbol + exp + side.value + str(strike)


    

class TTOrder:
   
	def __init__(self, tif: TTTimeInForce, price: float, price_effect: TTPriceEffect, order_type: TTOrderType) -> None:
		self.tif = tif
		self.order_type = order_type
		self.price = '{:2f}'.format(price)
		self.price_effect = price_effect
		self.legs = []
	
	def add_leg(self, instrument_type: TTInstrumentType, symbol: str, quantity: int, action: TTLegAction):
		if len(self.legs) >= 4:
			print('Error: cannot have more than 4 legs per order.')
			return 
	
		if instrument_type is None or symbol == None or quantity == 0 or action is None:
			print(f'Invalid parameters')
			print(f'instrument_type: {instrument_type}')
			print(f'symbol: {symbol}')
			print(f'quantity')
		
		self.legs.append({
			'instrument-type': instrument_type.value,
			'symbol': symbol,
			'quantity': quantity,
			'action': action.value
			})
	def build_order(self) -> dict:
		self.body = {
		'time-in-force': self.tif.value,
		'price': self.price,
		'price-effect': self.price_effect.value,
		'order-type': self.order_type.value,
		'legs': self.legs
		}
		print(json.dumps(self.body))
		return self.body


