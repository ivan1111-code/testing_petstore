import allure
import pytest

PET_ID = 987654321


@allure.epic("Petstore API")
@allure.feature("Pet")
class TestPet:

    @pytest.fixture
    def pet_payload(self):
        return {
            "id": PET_ID,
            "name": "Barsic",
            "status": "available",
            "category": {"id": 1, "name": "dogs"},
            "photoUrls": ["https://example.com/barsic.jpg"],
            "tags": [{"id": 1, "name": "cute"}],
        }


    @allure.story("Create pet")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("POST /pet — создание питомца")
    def test_create_pet(self, api, pet_payload):
        with allure.step("Отправить POST /pet"):
            r = api.post("pet", json=pet_payload)
        with allure.step("Проверить 200 и тело ответа"):
            assert r.status_code == 200
            body = r.json()
            assert body["id"] == PET_ID
            assert body["name"] == "Barsic"

    @allure.story("Read pet")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("GET /pet/{petId} — чтение питомца")
    def test_get_pet(self, api):
        with allure.step("GET /pet/{petId}"):
            r = api.get(f"pet/{PET_ID}")
        with allure.step("Проверить 200 и поля"):
            assert r.status_code == 200
            body = r.json()
            assert body["id"] == PET_ID
            assert body["name"] == "Barsic"

    @allure.story("Update pet")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("PUT /pet — обновление питомца")
    def test_update_pet(self, api):
        updated = {
            "id": PET_ID, "name": "BarsicUpdated", "status": "sold",
            "category": {"id": 1, "name": "dogs"},
            "photoUrls": ["https://example.com/barsic.jpg"],
            "tags": [{"id": 1, "name": "cute"}],
        }
        with allure.step("PUT /pet"):
            r = api.put("pet", json=updated)
        with allure.step("Проверить 200 и изменения"):
            assert r.status_code == 200
            assert r.json()["name"] == "BarsicUpdated"
            assert r.json()["status"] == "sold"

    @allure.story("Delete pet")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("DELETE /pet/{petId} — удаление питомца")
    def test_delete_pet(self, api):
        with allure.step("DELETE /pet/{petId}"):
            r = api.delete(f"pet/{PET_ID}")
        with allure.step("Проверить 200"):
            assert r.status_code == 200
        with allure.step("Контрольное GET → 404"):
            g = api.get(f"pet/{PET_ID}", expected_error=True)
            assert g.status_code == 404


    @allure.story("Read pet — negative")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("NEG: GET /pet/{petId} несуществующего → 404")
    def test_get_pet_not_found(self, api):
        with allure.step("GET несуществующего питомца"):
            r = api.get("pet/000000000000", expected_error=True)
        with allure.step("Ожидаем 404"):
            assert r.status_code == 404

    @allure.story("Create pet — negative")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("NEG: POST /pet с некорректным JSON → 4xx")
    def test_create_pet_invalid_json(self, api):
        with allure.step("POST /pet с битым JSON через data="):
            r = api.post("pet", data="{not-a-json", expected_error=True)
        with allure.step("Ожидаем 4xx"):
            assert 400 <= r.status_code < 500

    @allure.story("Update pet — negative")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("NEG: PUT /pet без обязательного id → 4xx")
    def test_update_pet_no_id(self, api):
        bad = {"name": "NoId", "status": "available", "photoUrls": []}
        with allure.step("PUT /pet без поля id"):
            r = api.put("pet", json=bad, expected_error=True)
        with allure.step("Ожидаем 4xx"):
            assert 400 <= r.status_code < 500

    @allure.story("Delete pet — negative")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("NEG: DELETE /pet/{petId} несуществующего → 404")
    def test_delete_pet_not_found(self, api):
        with allure.step("DELETE несуществующего питомца"):
            r = api.delete("pet/000000000000", expected_error=True)
        with allure.step("Ожидаем 404"):
            assert r.status_code == 404
