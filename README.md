# Тестовое задание в компанию HALORT

## Выполнил Алексеев Лев

## Технологии:

Python 3.11, Django 4, Django Rest Framework 3.14, PostgreSQL.

## Доступные эндпоинты и методы:

    1. Продукты:
    GET, POST: http://127.0.0.1:8000/api/products/ - получение списка продуктов, добавление продукта;
    GET, PATCH, DELETE: http://127.0.0.1:8000/api/products/{id}/ - получение/изменение/удаление продукта, изменение тегов продукта;
    GET: http://127.0.0.1:8000/api/products/?sort=measurement_unit - получение списка продуктов отсортированных по полю measurement_unit;
    GET: http://127.0.0.1:8000/api/products/?sort=name - получение списка продуктов отсортированных по алфавиту (полю name);
    GET: http://127.0.0.1:8000/api/products/?tags={slug} - получение списка продуктов отфильтрованных по полю slug модели Тег;

    2. Теги:
    GET, POST: http://127.0.0.1:8000/api/tags/ - получение списка тегов, добавление тега;
    GET, PATCH, DELETE: http://127.0.0.1:8000/api/tags/{id}/ - получение/изменение/удаление тега;

    3. Список покупок:
    GET, POST: http://127.0.0.1:8000/api/shoping-cart/ - получение списков покупок, добавление списка покупок;
    GET, PATCH, DELETE: http://127.0.0.1:8000/api/shoping-cart/{id}/ - получение/изменение/удаление продукта, изменение тегов продукта;

    4. Админка: 
    http://127.0.0.1:8000/admin/


## Установка:

1. Разархивируйте проект, создайте и активируйте виртуальное окржение, установите зависимости;

    ```bash
    $ python -m venv venv
    $ source venv/Scripts/activate
    $ pip install poetry
    $ poetry shell
    $ poetry install
    ```

2. Заполните файл .env вашими данными;

3. Выполните миграции;

    ```bash
    $ python manage.py migrate
    ```

4. Создайте суперпользователя;

    ```bash
    $ python manage.py createsuperuser
    ```
5. Запустите сервер;

    ```bash
    $ python manage.py runserver
    ```

