import requests
import json
import time
import datetime
from typing import Any

class TTAPI:
    def __init__(self, url: str, login: str, password: str, token: str, expiration: float):
        self.url: str = url
        self.username: str = login
        self.password: str = password
        self.token: str = token
        self.expiration: float = expiration
        self.user: dict[Any, Any] = {}
        self.header: dict[str, str] = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }
    
    def __post(self, endpoint: str, body: dict[str, str], headers: dict[str, str]) -> Any:
        response = requests.post(self.url + endpoint, data=json.dumps(body), headers=headers)
        if response.status_code == 201:
            return response.json()
        print(f"Error {response.status_code}")
        print(f"Endpoint: {endpoint}")
        print(f"Body: {body}")
        print(f"Headers: {headers}")
        print(f"Response: {response.text}")
        return None
    
    def __get(self, endpoint: str, body: dict[str, str], headers: dict[str, str]) -> Any:
        response = requests.get(self.url + endpoint, data=json.dumps(body), headers=headers)
        if response.status_code == 200:
            return response.json()
        print(f"Error {response.status_code}")
        print(f"Endpoint: {endpoint}")
        print(f"Body: {body}")
        print(f"Headers: {headers}")
        print(f"Response: {response.text}")
        return None
    
    def login(self) -> bool:
        if not self.token or time.time() > self.expiration:
            credentials: dict[str, Any] = {
                "login": self.username,
                "password": self.password,
                "remember-me": True
            }
            login_data = self.__post('/sessions', credentials, self.header)

            if 'data' not in login_data or 'session-token' not in login_data['data']:
                print("Login failed:", login_data)
                return False

            self.token = login_data['data']['session-token']
            self.expiration = time.time() + 86400
            self.header["Authorization"] = self.token

            self.update_env_variable("TOKEN", self.token)
            self.update_env_variable("EXP", str(self.expiration))

            print("Logged in. Token saved.")
            
        else:
            readable_time = datetime.datetime.fromtimestamp(self.expiration).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Using existing token (valid until {readable_time})")
        return True
            
    def validate(self) -> bool:
        validation_data = self.__post('/sessions/validate', body={}, headers=self.header)

        if not validation_data:
            print("Validation Failed")
            return False
        else:
            self.user ['external-id'] = validation_data['data']['external-id']
            self.user ['id'] = validation_data['data']['id']
            print("Validation Successful")
            return True
    
    def get_accounts(self) -> None:
        accounts_data = self.__get('/customers/me/accounts', body={}, headers=self.header)

        if not accounts_data:
            print("Account Retrieval Failed")
        else:
            self.user['accounts'] = []
            for account in accounts_data['data']['items']:
                self.user['accounts'].append(account)
    
    def get_chains(self, ticker: str) -> list[dict[str, Any]]:
        symbol = ticker

        chain_data = self.__get('/option-chains/' + symbol, {}, self.header)

        if not chain_data:
            print(f"Getting Option Chains for {symbol} failed!")
            return []
        else:
            items = chain_data.get("data", {}).get("items", [])
            print(f"\n{len(items)} option contracts for {symbol.upper()}")
            return items

    def see_chains(self, chains: list[dict[str, Any]], length: int):
        print(f"First {length} contracts displayed.")
        for option in chains[:length]:
            print(f"Symbol:        {option.get('symbol')}")
            print(f"Type:          {option.get('option-type')}")
            print(f"Strike Price:  {option.get('strike-price')}")
            print(f"DTE:    {option.get('days-to-expiration')}")
            print(f"ExerciseStyle: {option.get('exercise-style')}")
            print(f"Settlement:    {option.get('settlement-type')}")
            print("-" * 40)
    
    def sort_chain(self, chain: list[dict[str, Any]], dte: int, strike_low: float, strike_high: float, side: str) -> list[dict[str, Any]]:
        good_options: list[dict[str, Any]] = []
        # self.get_option("SPXW  250605P03000000")

        for option in chain[:5]:
            dte_val = option.get('days-to-expiration')
            strike = option.get('strike-price')
            opt_type = option.get('option-type')

            if dte_val is None or strike is None or opt_type is None:
                continue
            try:
                strike_float = float(strike)
            except (TypeError, ValueError):
                continue

            if (dte_val == dte and 
            strike_float > strike_low and 
            strike_float < strike_high and 
            opt_type.lower() == side.lower()):
                good_options.append(option)

        return good_options
                
    def get_option(self, ticker: str):
        option_endpoint = f"/instruments/equity-options/{ticker}"
        option_data = self.__get(option_endpoint, {}, self.header)
        
        if not option_data:
            print(f"Getting Option info for {ticker} failed!")
        else:
            print("Success!")
            return option_data
    
    def update_env_variable(self, key: str, value: str) -> None:
        lines = []
        with open(".env", "r") as f:
            lines = f.readlines()
        with open(".env", "w") as f:
            for line in lines:
                if line.startswith(f"{key}="):
                    f.write(f"{key}={value}\n")
                else:
                    f.write(line)



