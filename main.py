import os
from dotenv import load_dotenv

load_dotenv()

# Constants
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")
CERT_URL = "https://api.cert.tastyworks.com"
CERT_WSS = "wss://streamer.tastyworks.com"