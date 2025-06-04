import requests
import json
import time
import datetime

class TTAPI:
    def __init__(self, url, login, password, token, expiration):
        self.url = url
        self.username = login
        self.password = password
        self.token = token
        self.expiration = expiration
        self.user = {}
        self.header = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }

    
    def __post(self, endpoint, body, headers):
        response = requests.post(self.url + endpoint, data=json.dumps(body), headers=headers)
        if response.status_code == 201:
            return response.json()
        print(f"Error {response.status_code}")
        print(f"Endpoint: {endpoint}")
        print(f"Body: {body}")
        print(f"Headers: {headers}")
        print(f"Response: {response.text}")
        return None
    
    def __get(self, endpoint, body, headers):
        response = requests.get(self.url + endpoint, data=json.dumps(body), headers=headers)
        if response.status_code == 200:
            return response.json()
        print(f"Error {response.status_code}")
        print(f"Endpoint: {endpoint}")
        print(f"Body: {body}")
        print(f"Headers: {headers}")
        print(f"Response: {response.text}")
        return None
    
    def login(self):
        if not self.token or time.time() > self.expiration:
            credentials = {
                "login": self.username,
                "password": self.password,
                "remember-me": True
            }
            login_data = self.__post('/sessions', credentials, self.header)

            if 'data' not in login_data or 'session-token' not in login_data['data']:
                print("Login failed:", login_data)
                return

            self.token = login_data['data']['session-token']
            self.expiration = time.time() + 86400
            self.header["Authorization"] = self.token

            self.update_env_variable("TOKEN", self.token)
            self.update_env_variable("EXP", str(self.expiration))

            print("Logged in. Token saved.")
        else:
            readable_time = datetime.datetime.fromtimestamp(self.expiration).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Using existing token (valid until {readable_time})")


    def validate(self):
        headers = {
            "Authorization": self.token,
            "Content-Type": "application/json"
        }
        validation_data = self.__post('/sessions/validate', body={}, headers=headers)

        if not validation_data:
            print("Validation Failed")
        else:
            self.user ['external-id'] = validation_data['data']['external-id']
            self.user ['id'] = validation_data['data']['id']
            print("Validation Successful")
    
    def get_accounts(self):
        accounts_data = self.__get('customers/me/accounts', self.header)

        if not accounts_data:
            print("Account Retrieval Failed")
        else:
            self.user['accounts'] = []
            for account in accounts_data['data']['items']:
                self.user['accounts'].append(account)
    
    def get_chains(self, ticker):
        symbol = ticker

        chain_data = self.__get('/option-chains/' + symbol, {}, self.header)

        if not chain_data:
            print(f"Getting Option Chains for {symbol} failed!")
        else:
            items = chain_data.get("data", {}).get("items", [])
            print(f"\n{len(items)} option contracts for {symbol.upper()}")
            return items

    def see_chains(self, chains, length):
        print(f"First {length} contracts displayed.")
        for option in chains[:length]:
            print(f"Symbol:        {option.get('symbol')}")
            print(f"Type:          {option.get('option-type')}")
            print(f"Strike Price:  {option.get('strike-price')}")
            print(f"Expiration:    {option.get('expiration-date')}")
            print(f"ExerciseStyle: {option.get('exercise-style')}")
            print(f"Settlement:    {option.get('settlement-type')}")
            print("-" * 40)
    
    def update_env_variable(self, key, value):
        lines = []
        with open(".env", "r") as f:
            lines = f.readlines()
        with open(".env", "w") as f:
            for line in lines:
                if line.startswith(f"{key}="):
                    f.write(f"{key}={value}\n")
                else:
                    f.write(line)



