import pytest
import requests
import allure
from ..helpers import generate_user_data, register_new_user, delete_user, login_user, BASE_URL


class TestUserCreation:
    @allure.title("Тест создания пользователя")
    @allure.description("Проверка успешного создания пользователя")
    def test_create_user_success(self):
        email, password, name = generate_user_data()
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        
        response = requests.post(f'{BASE_URL}/auth/register', data=payload)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True
        assert "accessToken" in response_data
        assert "refreshToken" in response_data
        assert "user" in response_data

        user_info = response_data["user"]
        assert user_info["email"] == email
        assert user_info["name"] == name


        login_response = login_user(email, password)
        if login_response.status_code == 200:
            auth_token = login_response.json()["accessToken"]
            delete_user(auth_token)

    @allure.title("Тест создания дубликата пользователя")
    @allure.description("Проверка ошибки при создании пользователя с существующим email")
    def test_create_duplicate_user_fails(self):
        email, password, name = register_new_user()
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        
        response = requests.post(f'{BASE_URL}/auth/register', data=payload)
        
        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] == False
        assert response_data["message"] == "User already exists"

        login_response = login_user(email, password)
        if login_response.status_code == 200:
            auth_token = login_response.json()["accessToken"]
            delete_user(auth_token)

    @allure.title("Тест создания пользователя без обязательных полей")
    @allure.description("Проверка ошибки регистрации при отсутствии обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_fails(self, missing_field):
        email, password, name = generate_user_data()
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        
        del payload[missing_field]
        
        response = requests.post(f'{BASE_URL}/auth/register', data=payload)
        
        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] == False
        assert response_data["message"] == "Email, password and name are required fields"