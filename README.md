# YaCut

YaCut — это сервис укорачивания ссылок на Flask. Его задача — ассоциировать длинный URL с коротким кодом, который может предложить сам пользователь или сгенерировать сервис.

## Возможности

- Создание короткой ссылки для любого валидного URL.
- Использование собственного кастомного короткого идентификатора (если он свободен).
- Автоматическая генерация короткого кода при его отсутствии.
- Перенаправление по короткой ссылке на исходный адрес.
- Работа через веб‑интерфейс и REST API (описание в `openapi.yml`).

## Стек технологий

- Python 3.9.
- Flask.
- SQLAlchemy.
- Jinja2.
- SQLite.

## Установка и запуск проекта

Клонируйте репозиторий и перейдите в директорию проекта:

```bash
git clone git@github.com:ssavboy/yacut.git
cd yacut
```

Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
source venv/scripts/activate
```

Установите зависимости:

```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Примените миграции базы данных:

```bash
flask db upgrade
```

Запустите приложение:

```bash
flask run
```

По умолчанию сервис будет доступен по адресу `http://127.0.0.1:5000/`.

## Структура проекта

```text
yacut/
├── yacut/                 # Пакет приложения
│   ├── static/            # Статика (CSS, JS, изображения)
│   ├── templates/         # HTML-шаблоны Jinja2
│   ├── __init__.py        # фабрика приложения Flask
│   ├── api_views.py       # API-эндпоинты
│   ├── error_handlers.py  # обработчики ошибок
│   ├── exceptions.py      # пользовательские исключения
│   ├── form.py            # веб-формы
│   ├── models.py          # модели SQLAlchemy
│   └── views.py           # веб-вьюхи
├── openapi.yml            # спецификация API
├── requirements.txt       # зависимости
├── settings.py            # настройки проекта
├── pytest.ini             # конфигурация тестов
└── README.md
```

## API

Спецификация REST API описана в файле `openapi.yml`.  
Её можно использовать для генерации клиента или просмотра доступных эндпоинтов в Swagger / Redoc
