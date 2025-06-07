import os
from dotenv import load_dotenv
from api import TTAPI
load_dotenv()

# Constants
CERT_URL: str = "https://api.cert.tastyworks.com"
PROD_URL: str = "https://api.tastyworks.com"
CERT_WSS: str = "wss://streamer.tastyworks.com"
LOGIN: str = os.getenv("LOGIN")
PASSWORD: str = os.getenv("PASSWORD")
TOKEN: str = os.getenv("TOKEN")
EXP: float = float(os.getenv("EXP") or 0)


tastytrade = TTAPI(PROD_URL, LOGIN, PASSWORD, TOKEN, EXP)

if not tastytrade.login():
    exit()

if not tastytrade.validate():
    exit()

symbol: str = input("Ticker: ")

chains = tastytrade.get_chains(symbol)

tastytrade.see_chains(chains, 10)

options = tastytrade.sort_chain(chains, 0, 0, 100000, "C")

tastytrade.see_chains(options, len(options))


