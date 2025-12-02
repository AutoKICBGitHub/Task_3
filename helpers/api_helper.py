import requests
from data.test_data import TestData


class ApiHelper:
    
    def __init__(self):
        self.base_url = TestData.BASE_URL
        self.api_url = f"{self.base_url}api/"
    
    def register_user(self, email: str, password: str, name: str) -> dict:
        url = f"{self.api_url}auth/register"
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def login_user(self, email: str, password: str) -> dict:
        url = f"{self.api_url}auth/login"
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def delete_user(self, access_token: str) -> bool:
        url = f"{self.api_url}auth/user"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.delete(url, headers=headers)
        if response.status_code in [200, 202]:
            return True
        return False
    
    def create_user_and_get_token(self, email: str, password: str, name: str) -> str:
        register_response = self.register_user(email, password, name)
        if "accessToken" in register_response:
            return register_response["accessToken"]
        
        login_response = self.login_user(email, password)
        if "accessToken" in login_response:
            return login_response["accessToken"]
        
        return None
