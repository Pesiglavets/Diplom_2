import pytest
import allure
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import register_new_user, delete_user, login_user


class TestUserLogin:
    @allure.title("Тест успешной авторизации пользователя")
    @allure.description("Проверка, что пользователь может авторизоваться с валидными данными")
    def test_login_user_success(self):
        email, password, name = register_new_user()
        response = login_user(email, password)
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True
        assert "accessToken" in response_data
        assert "refreshToken" in response_data
        assert "user" in response_data

        user_info = response_data["user"]
        assert user_info["email"] == email
        assert user_info["name"] == name

        auth_token = response_data["accessToken"]
        delete_user(auth_token)

    @allure.title("Тест авторизации с неверным email")
    @allure.description("Проверка ошибки при неправильно указанном email")
    def test_login_with_wrong_email_fails(self):
        email, password, name = register_new_user()
        wrong_email = email + "_wrong"
        response = login_user(wrong_email, password)
        
        assert response.status_code == 401
        response_data = response.json()        
        assert response_data["success"] == False
        assert response_data["message"] == "email or password are incorrect"
        
        login_response = login_user(email, password)
        if login_response.status_code == 200:
            auth_token = login_response.json()["accessToken"]
            delete_user(auth_token)
    
    @allure.title("Тест авторизации с неверным паролем")
    @allure.description("Проверка ошибки при неправильно указанном пароле")
    def test_login_with_wrong_password_fails(self):
        email, password, name = register_new_user()
        wrong_password = password + "_wrong"
        response = login_user(email, wrong_password)
        
        assert response.status_code == 401
        response_data = response.json()        
        assert response_data["success"] == False
        assert response_data["message"] == "email or password are incorrect"
        
        login_response = login_user(email, password)
        if login_response.status_code == 200:
            auth_token = login_response.json()["accessToken"]
            delete_user(auth_token)


    