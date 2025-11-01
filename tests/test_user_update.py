import pytest
import requests
import allure
from ..helpers import generate_user_data, register_new_user, delete_user, login_user, BASE_URL


class TestUserUpdate:
    @allure.title("Тест изменения данных пользователя с авторизацией")
    @allure.description("Проверка, что авторизованный пользователь может изменить любое поле")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_update_user_field_with_auth_success(self, field):
        email, password, name = register_new_user()
        login_response = login_user(email, password)
        assert login_response.status_code == 200
        auth_token = login_response.json()["accessToken"]

        new_email, new_password, new_name = generate_user_data()
        field_values = {"email": new_email, "password": new_password, "name": new_name}
        update_data = {field: field_values[field]}
        excepted_value = field_values[field]

        headers = {'Authorization': auth_token}
        response = requests.patch(f'{BASE_URL}/auth/user', headers=headers, json=update_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True

        if field in ["email", "name"]:
            assert "user" in response_data
            user_info = response_data["user"]
            assert user_info[field] == excepted_value

        elif field == "password":
            new_login_response = login_user(email, new_password)
            assert new_login_response.status_code == 200
            auth_token = new_login_response.json()["accessToken"]

        delete_user(auth_token)


    @allure.title("Тест изменения данных пользователя без авторизации")
    @allure.description("Проверка ошибки при попытке изменить данные при авторизации")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_update_user_field_without_auth_fails(self, field):
        email, password, name = register_new_user()

        new_email, new_password, new_name = generate_user_data()
        field_values = {"email": new_email, "password": new_password, "name": new_name}
        update_data = {field: field_values[field]}

        response = requests.patch(f'{BASE_URL}/auth/user', json=update_data)

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] == False
        assert response_data["message"] == "You should be authorised"

        login_response = login_user(email, password)
        if login_response.status_code == 200:
            auth_token = login_response.json()["accessToken"]
            delete_user(auth_token)

