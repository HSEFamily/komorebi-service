# Komorebi
Сервис для поиска кино, проставления оценов и организации киноклубов.
Основную информацию можно найти по [ссылке](https://github.com/HSEFamily/komorebi/README.md).

### Для разработчиков:

Пакеты:

    1. domain (Роман) - работа с БД, анализ предпочтений
    2. emdb_search (Глеб) - сбор информации с Кинопоиска
    3. web_service (Тимур) - веб-сервис, авторизация пользователей и т.д.

Для начала работы:

    1. Склонить проект на компьютер: git clone https://github.com/HSEFamily/komorebi-service
    2. Установить virtualenv
    3. Установить в папке проекта virtualenv: virtualenv venv
    4. Активировать virtualenv: source /venv/bin/active
    5. Установить необходимые библиотеки: pip install requirements.txt
    6. Начать работу в dev ветке
    7. Написать тесты в своем пакете в папке komorebi-test



