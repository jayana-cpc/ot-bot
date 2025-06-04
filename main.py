import os
from dotenv import load_dotenv
import api
load_dotenv()

# Constants
CERT_URL = "https://api.cert.tastyworks.com"
CERT_WSS = "wss://streamer.tastyworks.com"
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
TOKEN = os.getenv("TOKEN")
EXP = float(os.getenv("EXP") or 0)


tastytrade = api.TTAPI(CERT_URL, LOGIN, PASSWORD, TOKEN, EXP)

tastytrade.login()

tastytrade.validate()

symbol = input("Ticker: ")

chains = tastytrade.get_chains(symbol)

tastytrade.see_chains(chains, 10)

