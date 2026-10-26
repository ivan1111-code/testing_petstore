import sys, os, time
import pytest

sys.path.insert(0, os.path.dirname(__file__))
from base_request import BaseRequest

BASE_URL = "https://petstore3.swagger.io/api/v3"


@pytest.fixture(scope="session")
def api():
    return BaseRequest(BASE_URL)


@pytest.fixture(scope="session", autouse=True)
def _allure_env():
    results_dir = os.path.join(os.path.dirname(__file__), "allure-results")
    os.makedirs(results_dir, exist_ok=True)
    with open(os.path.join(results_dir, "environment.properties"), "w") as f:
        f.write(f"API.Base.URL={BASE_URL}\n")
        f.write("Python.Version=3.x\n")
        f.write("Framework=pytest + allure-pytest\n")
        f.write("Allure.CLI=3.x\n")
    yield


@pytest.fixture(autouse=True)
def _polite_delay():
    time.sleep(0.7)
    yield
