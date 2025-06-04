import requests
import json

class TTAPI:
    def __init__(self, url, login, password):
        self.url = url
        self.login = login
        self.password = password
        self.header = {
                "Content-Type": "application/json"
            }
    
    def __post(self, endpoint, body, headers):
        response = requests.post(self.url + endpoint, data=json.dumps(body), headers=headers)
        if response.status_code == "201":
            return response.json()
        print(f"Error {response.status_code}")
        print(f"Endpoint: {endpoint}")
        print(f"Body: {body}")
        print(f"Headers: {headers}")
        print(f"Response: {response.text}")
        return None
    
    def __get(self, endpoint, body, headers):
        response = requests.get(self.url + endpoint, data=json.dumps(body), headers=headers)
        if response.status_code == "200":
            return response.json()
        print(f"Error {response.status_code}")
        print(f"Endpoint: {endpoint}")
        print(f"Body: {body}")
        print(f"Headers: {headers}")
        print(f"Response: {response.text}")
        return None
    
    def login(self, remember_me):
        credentials = {
            "login": self.login,
            "password": self.password,
            "remember-me": remember_me
        }

        login_data = self.__post('/sessions', credentials, self.header)

        if 'data' not in login_data or 'session-token' not in login_data['data']:
            print("Login failed:", login_data)
            
        self.token = login_data['data']['session-token']
        self.user = login_data['data']['user']
        print("Logged in. Token acquired.")

    def validate(self):
        headers = {
            "Authorization": self.token
        }
        validation_data = self.__post('/sessions/validate', headers)

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

        chain_data = self.__get('/option-chains/' + symbol, self.header)

        if not chain_data:
            print(f"Getting Option Chains for {symbol} failed!")
        else:
            items = chain_data.get("data", {}).get("items", [])
            print(f"\n{len(items)} option contracts for {symbol.upper()}")
            return items

    def see_chains(self, chains):
        for option in chains:
            print(f"Symbol:        {option.get('symbol')}")
            print(f"Type:          {option.get('option-type')}")
            print(f"Strike Price:  {option.get('strike-price')}")
            print(f"Expiration:    {option.get('expiration-date')}")
            print(f"ExerciseStyle: {option.get('exercise-style')}")
            print(f"Settlement:    {option.get('settlement-type')}")
            print("-" * 40)
        


