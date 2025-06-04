import requests
import json

class TTAPI:
    def __init__(self, url, login, password):
        self.url = url
        self.login = login
        self.password = password
    
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
        headers = {
            "Content-Type": "application/json"
        }

        login_response = requests.post(self.url + '/sessions', json=credentials, headers=headers)
        login_data = login_response.json()

        if 'data' not in login_data or 'session-token' not in login_data['data']:
            print("Login failed:", login_data)
            exit()

        token = login_data['data']['session-token']
        user = login_data['data']['user']
        print("Logged in. Token acquired.")

