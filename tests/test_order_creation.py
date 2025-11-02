import pytest
import allure
from ..helpers import get_ingredients, create_order, register_new_user, delete_user, login_user, BASE_URL


class TestOrderCreation:
    @allure.title("Тест  создания заказа с авторизацией и ингредиентами")
    @allure.description("Проверка успешного создания заказа авторизованным пользователем с игнредиентами")
    def test_create_order_with_auth_and_ingredients_success(self):
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
        response_data = response.json()

        assert response_data["success"] == True
        assert "order" in response_data
        assert "number" in response_data["order"]

        delete_user(auth_token)

    @allure.title("Тест  создания заказа без авторизации м ингредиентами")
    @allure.description("Проверка успешного создания заказа неавторизованным пользователем с игнредиентами")
    def test_create_order_without_auth_with_ingredients_success(self):

        ingredients = get_ingredients()
        assert ingredients is not None
        assert len(ingredients) > 0

        ingredients_ids = [ingredients[0]["_id"]]
        response = create_order(ingredients_ids)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] == True
        assert "order" in response_data
        assert "number" in response_data["order"]

    @allure.title("Тест  создания заказа с авторизацией без ингредиентов")
    @allure.description("Проверка ошибки создания заказа авторизованным пользователем без игнредиентов")
    def test_create_order_with_auth_without_ingredients_fails(self):
        email, password, name = register_new_user()
        login_response = login_user(email, password)
        assert login_response.status_code == 200
        auth_token = login_response.json()["accessToken"]

        response = create_order([], auth_token)

        assert response.status_code == 400
        response_data = response.json()
        assert response_data["success"] == False
        assert "Ingredient ids must be provided" in response_data["message"]

        delete_user(auth_token)

    @allure.title("Тест  создания заказа без авторизации и без ингредиентов")
    @allure.description("Проверка ошибки создания заказа неавторизованным пользователем без игнредиентов")
    def test_create_order_without_auth_without_ingredients_fails(self):

        response = create_order([])

        assert response.status_code == 400
        response_data = response.json()
        assert response_data["success"] == False
        assert "Ingredient ids must be provided" in response_data["message"]


    @allure.title("Тест  создания заказа с неверным хешем ингредиентов")
    @allure.description("Проверка ошибки создания заказа с несуществующими игнредиентами")
    def test_create_order_with_invalid_ingredients_hash_fails(self):
        email, password, name = register_new_user()
        login_response = login_user(email, password)
        assert login_response.status_code == 200
        auth_token = login_response.json()["accessToken"]

        invalid_ingredients = ["invalid_ingreident_hash_2025"]
        response = create_order(invalid_ingredients, auth_token)

        assert response.status_code == 500
        assert "Internal Server Error" in response.text

        delete_user(auth_token)