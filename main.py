import os
from dotenv import load_dotenv
from api import TTAPI
from order import TTOption, TTOptionSide, TTOrder
import asyncio
from tastytrade import Session, DXLinkStreamer
from tastytrade.dxfeed import Greeks

load_dotenv()

# Constants
CERT_URL: str = "https://api.cert.tastyworks.com"
PROD_URL: str = "https://api.tastyworks.com"
CERT_WSS: str = "wss://streamer.tastyworks.com"
LOGIN: str = str(os.getenv("LOGIN"))
PASSWORD: str = "kyfnuq-6dahqo-bIhzim" # str(os.getenv("PASSWORD"))

TOKEN: str = str(os.getenv("TOKEN"))
EXP: float = float(os.getenv("EXP") or 0)

tastytrade = TTAPI(PROD_URL, LOGIN, PASSWORD, TOKEN, EXP)

if not tastytrade.login():
    exit()

if not tastytrade.validate():
    exit()

root_symbol: str = input("Ticker: ")

chains = tastytrade.get_chains(root_symbol)

option = chains[0]
symbol = option['symbol']
date = option['expiration-date']
side = TTOptionSide.CALL if option['option-type'] == 'C' else TTOptionSide.PUT
strike = float(option['strike-price'])

# option = TTOption(symbol, date, side, strike)
print(symbol)

order = TTOrder



# tastytrade.see_chains(chains, 10)

# options = tastytrade.sort_chain(chains, 0, 0, 100000, "C")

# tastytrade.see_chains(options, len(options))


