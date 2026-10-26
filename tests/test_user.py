import allure
import pytest

USERNAME = "shpatovich_allure3"


@allure.epic("Petstore API")
@allure.feature("User")
class TestUser:

    @pytest.fixture
    def user_payload(self):
        return {
            "id": 88,
            "username": USERNAME,
            "firstName": "Andrew",
            "lastName": "S",
            "email": "shpatovichad@ithub.ru",
            "password": "12345",
            "phone": "",
            "userStatus": 1,
        }

    @allure.story("Create user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("POST /user — создание пользователя")
    def test_create_user(self, api, user_payload):
        with allure.step("POST /user"):
            r = api.post("user", json=user_payload)
        with allure.step("Проверить 200"):
            assert r.status_code == 200

    @allure.story("Read user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("GET /user/{username} — чтение пользователя")
    def test_get_user(self, api, user_payload):
        with allure.step("GET /user/{username}"):
            r = api.get(f"user/{USERNAME}")
        with allure.step("Проверить 200 и поля"):
            assert r.status_code == 200
            body = r.json()
            assert body["username"] == USERNAME
            assert body["email"] == user_payload["email"]

    @allure.story("Update user")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("PUT /user/{username} — обновление")
    def test_update_user(self, api, user_payload):
        new = user_payload.copy()
        new["firstName"] = "Maomao"
        with allure.step("PUT /user/{username}"):
            r = api.put(f"user/{USERNAME}", json=new)
        with allure.step("Проверить 200 и контрольное GET"):
            assert r.status_code == 200
            g = api.get(f"user/{USERNAME}")
            assert g.json()["firstName"] == "Maomao"

    @allure.story("Delete user")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("DELETE /user/{username} — удаление")
    def test_delete_user(self, api):
        with allure.step("DELETE /user/{username}"):
            r = api.delete(f"user/{USERNAME}")
        with allure.step("Проверить 200"):
            assert r.status_code == 200
        with allure.step("Контрольное GET → 404"):
            g = api.get(f"user/{USERNAME}", expected_error=True)
            assert g.status_code == 404

    @allure.story("Read user — negative")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("NEG: GET /user/{username} несуществующего → 404")
    def test_get_user_not_found(self, api):
        with allure.step("GET несуществующего пользователя"):
            r = api.get("user/definitely_not_exists_xyz", expected_error=True)
        with allure.step("Ожидаем 404"):
            assert r.status_code == 404

    @allure.story("Create user — negative")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("NEG: POST /user с некорректным JSON → 4xx")
    def test_create_user_invalid_json(self, api):
        with allure.step("POST /user с битым JSON"):
            r = api.post("user", data="{broken", expected_error=True)
        with allure.step("Ожидаем 4xx"):
            assert 400 <= r.status_code < 500

    @allure.story("Update user — negative")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("NEG: PUT /user/{username} для несуществующего → 404")
    def test_update_user_not_found(self, api):
        with allure.step("PUT несуществующего пользователя"):
            r = api.put("user/no_such_user_qq",
                        json={"firstName": "X"}, expected_error=True)
        with allure.step("Ожидаем 404"):
            assert r.status_code == 404

    @allure.story("Delete user — negative")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title("NEG: DELETE /user/{username} несуществующего → 404")
    def test_delete_user_not_found(self, api):
        with allure.step("DELETE несуществующего пользователя"):
            r = api.delete("user/no_such_user_qq", expected_error=True)
        with allure.step("Ожидаем 404"):
            assert r.status_code == 404
