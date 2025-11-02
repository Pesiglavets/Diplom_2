import requests
from faker import Faker

fake = Faker()

BASE_URL = "https://stellarburgers.education-services.ru/api"

def generate_random_email():
    return fake.email()

def generate_random_password():
    return fake.password(length=8)

def generate_random_name():
    return fake.first_name()

def generate_user_data():
    email = generate_random_email()
    password = generate_random_password()
    name = generate_random_name()
    
    return email, password, name

def register_new_user():
    email, password, name = generate_user_data()
    payload = {"email": email, "password": password, "name": name}
    response = requests.post(f'{BASE_URL}/auth/register', data=payload)
    
    if response.status_code == 200:
        return email, password, name
    elif response.status_code == 403:
        email, password, name = generate_user_data()
        payload = {"email": email, "password": password, "name": name}
        response = requests.post(f'{BASE_URL}/auth/register', data=payload)
        
        if response.status_code == 200:
            return email, password, name 
    return None

def login_user(email, password):
    payload = {"email": email, "password": password}
    response = requests.post(f'{BASE_URL}/auth/login', data=payload)
    return response

def delete_user(auth_token):
    if auth_token:
        headers = {'Authorization': auth_token}
        response = requests.delete(f'{BASE_URL}/auth/user', headers=headers)
        return response
    return None

def get_ingredients():
    response = requests.get(f'{BASE_URL}/ingredients')
    if response.status_code == 200:
        return response.json()["data"]
    return None

def create_order(ingredients=None, auth_token=None):
    payload = {}
    if ingredients is not None: 
        payload["ingredients"] = ingredients
    headers = {}
    if auth_token:
        headers['Authorization'] = auth_token
    response = requests.post(f'{BASE_URL}/orders', data=payload, headers=headers)
    return response

