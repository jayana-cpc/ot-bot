import json
from enum import Enum

class TTOrderType(Enum):
  LIMIT = 'Limit'
  MARKET = 'Market'

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
  ...

class TTOrder:
   ... 