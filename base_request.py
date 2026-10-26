import requests
import pprint
import time


class BaseRequest:
    def __init__(self, base_url, headers=None, timeout=10):
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _request(self, url, method, json=None, data=None, params=None,
                 expected_error=False, retries=3, delay=1):
        last_exc = None
        response = None
        for attempt in range(1, retries + 1):
            try:
                response = self.session.request(
                    method=method, url=url, json=json, data=data,
                    params=params, timeout=self.timeout,
                )
                if 200 <= response.status_code < 300:
                    break
                if expected_error:
                    break
                print(f"[retry {attempt}/{retries}] {method} {url} -> "
                      f"{response.status_code}")
            except requests.RequestException as e:
                last_exc = e
                print(f"[retry {attempt}/{retries}] {method} {url} EXC: {e}")
            time.sleep(delay)

        if response is None and last_exc is not None:
            raise last_exc

        self._log(method, response)
        return response

    @staticmethod
    def _log(method, response):
        print(f"=== {method} ===")
        print("URL:    ", response.url)
        print("STATUS: ", response.status_code)
        try:
            print("JSON:   ", pprint.pformat(response.json()))
        except ValueError:
            print("TEXT:   ", pprint.pformat(response.text))
        print("=" * 20)

    def get(self, endpoint, expected_error=False, **params):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._request(url, "GET", params=params or None,
                             expected_error=expected_error)

    def post(self, endpoint, json=None, data=None, expected_error=False):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._request(url, "POST", json=json, data=data,
                             expected_error=expected_error)

    def put(self, endpoint, json=None, expected_error=False):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._request(url, "PUT", json=json,
                             expected_error=expected_error)

    def delete(self, endpoint, expected_error=False):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return self._request(url, "DELETE", expected_error=expected_error)
