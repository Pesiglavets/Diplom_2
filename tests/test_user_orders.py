import pytest
import allure
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import get_ingredients, create_order, register_new_user, delete_user, login_user, get_user_orders


class TestUserOrders:
    @allure.title("Тест получения заназов авторизованного пользователя")
    @allure.description("Проверка успешного получения заказов авторизованного пользователя")
    def test_get_orders_with_auth_success(self):
        email, password, name = register_new_user()
        login_response = login_user(email, password)
        assert login_response.status_code == 200
        auth_token = login_response.json()["accessToken"]
        
        ingredients = get_ingredients()
        assert ingredients is not None
        assert len(ingredients) > 0

        ingredients_ids = [ingredients[0]["_id"]]
        response = create_order(ingredients_ids, auth_token)
        assert response.status_code == 200

        response = get_user_orders(auth_token)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True
        assert "orders" in response_data
        assert isinstance(response_data["orders"], list)

        assert len(response_data["orders"]) > 0

        delete_user(auth_token)

    @allure.title("Тест получения заназов неавторизованного пользователя")
    @allure.description("Проверка ошибки получения заказов неавторизованного пользователя")
    def test_get_orders_without_auth_fails(self):

        response = get_user_orders()

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] == False
        assert "You should be authorised" in response_data["message"]