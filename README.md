# YaCut
Проект YaCut — это сервис укорачивания ссылок. Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.

## Клонирование и запуск проекта

Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:ssavboy/yacut.git
```
```
cd yacut
```
Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```
* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```
* Если у вас windows

    ```
    source venv/scripts/activate
    ```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```
Выполнить миграции
```
flask db upgrade
```
Запустить приложение
```
flask run
```
## Стек:
 - Python 3.9
 - Flask
 - SQLAlchemy
 - Jinja2
 - SQlite

## Автор [Kirill Molchanov](https://github.com/ssavboy)