# <img src="https://s8d5.turboimg.net/sp/5109159e6d4a480e1e2ad2e631178759/logo.png" width="24" height="24"> Блогикум

Блогикум — это веб-приложение для публикации личных историй и дневников, а так же для комментирования чужих историй.

## Используемые технологии

[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![HTML5](https://img.shields.io/badge/-HTML5-464646?style=flat&logo=HTML5&logoColor=56C0C0&color=008080&)](https://html.com/)



### Как запустить проект:

* Клонировать репозиторий и перейти в его директорию
    ```bash
    git clone git@github.com:Deyterriy/django_sprint4.git
    ```

* Cоздать и активировать виртуальное окружение:

    * Windows
    ```bash
    python -m venv venv
    ```
    ```bash
    source venv/Scripts/activate
    ```

    * Linux/macOS
    ```bash
    python3 -m venv venv
    ```
    ```bash
    source venv/bin/activate
    ```


* Обновить PIP

    ```bash
    python -m pip install --upgrade pip
    ```

* Установить зависимости из файла requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```

* Выполнить миграции:

    ```bash
    python manage.py makemigrations
    ```
    ```bash
    python manage.py migrate
    ```


* Запустить проект:

    ```bash
    python manage.py runserver
    ```

### Автор:  
_Козлов Кирилл_<br>
**email**: _d3yterriy@yandex.ru_<br>