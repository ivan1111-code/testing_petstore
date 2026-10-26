import allure
import pytest

ORDER_ID = 555


@allure.epic("Petstore API")
@allure.feature("Store")
class TestStore:

    @pytest.fixture
    def order_payload(self):
        return {
            "id": ORDER_ID,
            "petId": 987654321,
            "quantity": 2,
            "shipDate": "2026-01-01T12:00:00.000Z",
            "status": "placed",
            "complete": False,
        }

    @allure.story("Inventory")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("GET /store/inventory — инвентарь")
    def test_get_inventory(self, api):
        with allure.step("GET /store/inventory"):
            r = api.get("store/inventory")
        with allure.step("Ответ — словарь, код 200"):
            assert r.status_code == 200
            assert isinstance(r.json(), dict)

    @allure.story("Create order")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("POST /store/order — создание заказа")
    def test_create_order(self, api, order_payload):
        with allure.step("POST /store/order"):
            r = api.post("store/order", json=order_payload)
        with allure.step("Проверить 200 и поля"):
            assert r.status_code == 200
            body = r.json()
            assert body["id"] == ORDER_ID
            assert body["status"] == "placed"

    @allure.story("Read order")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("GET /store/order/{orderId} — чтение заказа")
    def test_get_order(self, api):
        with allure.step("GET /store/order/{orderId}"):
            r = api.get(f"store/order/{ORDER_ID}")
        with allure.step("Проверить 200 и поля"):
            assert r.status_code == 200
            body = r.json()
            assert body["id"] == ORDER_ID
            assert body["petId"] == 987654321

    @allure.story("Delete order")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("DELETE /store/order/{orderId} — удаление заказа")
    def test_delete_order(self, api):
        with allure.step("DELETE /store/order/{orderId}"):
            r = api.delete(f"store/order/{ORDER_ID}")
        with allure.step("Проверить 200"):
            assert r.status_code == 200
        with allure.step("Контрольное GET → 404"):
            g = api.get(f"store/order/{ORDER_ID}", expected_error=True)
            assert g.status_code == 404

    @allure.story("Read order — negative")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("NEG: GET /store/order/{id} несуществующего → 404")
    def test_get_order_not_found(self, api):
        with allure.step("GET несуществующего заказа"):
            r = api.get("store/order/999999999", expected_error=True)
        with allure.step("Ожидаем 404"):
            assert r.status_code == 404

    @allure.story("Create order — negative")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("NEG: POST /store/order без id → 4xx")
    def test_create_order_invalid(self, api):
        bad = {"quantity": 1, "status": "placed", "complete": False}
        with allure.step("POST /store/order без id"):
            r = api.post("store/order", json=bad, expected_error=True)
        with allure.step("Ожидаем 4xx"):
            assert 400 <= r.status_code < 500

    @allure.story("Delete order — negative")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("NEG: DELETE /store/order/{id} несуществующего → 404")
    def test_delete_order_not_found(self, api):
        with allure.step("DELETE несуществующего заказа"):
            r = api.delete("store/order/999999999", expected_error=True)
        with allure.step("Ожидаем 404"):
            assert r.status_code == 404

    @allure.story("Read order — negative")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("NEG: GET /store/order/{id} с нечисловым id → 4xx")
    def test_get_order_bad_id(self, api):
        with allure.step("GET /store/order/abc"):
            r = api.get("store/order/abc", expected_error=True)
        with allure.step("Ожидаем 4xx"):
            assert 400 <= r.status_code < 500
