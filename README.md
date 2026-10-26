# Petstore API Test Suite (pytest + Allure 3)

## Отчёт Allure
Готовый HTML-отчёт: [`result/index.html`](./result/index.html)

- Вариант single-file: весь отчёт — один файл `result/index.html`.
- Вариант folder: `result/index.html` + ассеты рядом (тоже открывается локально).

## Окружение
- Python 3, pytest 8.x
- allure-pytest (python адаптер)
- install allure global (`npm install -g allure`)

## Запуск (ubuntu bash)
pip install -r requirements.txt
npm install -g allure
pytest
allure generate allure-results -o result --clean
# отчёт в result/index.html
