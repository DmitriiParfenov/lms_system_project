# lms_system_project

Lms_system_project — это SPA-приложение для реализации LMS-системы. Пользователи могут размещать свои полезные материалы или курсы.
Сайт написан на Python с использованием Django для запросов пользователя. Для обмена данными между приложениями по сети используется Django REST-Framework. 
Работа с изображениями — pillow. База данных — PostgreSQL.

# Дополнительная информация

- Для создания суперпользователя из директории `lms_system_project` выполните в консоли: </br>
```
python manage.py csu
```

# Клонирование репозитория

В проекте для управления зависимостями используется [poetry](https://python-poetry.org/). </br>
Выполните в консоли: </br>

Для Windows: </br>
```
git clone git@github.com:DmitriiParfenov/lms_system_project.git
python -m venv venv
venv\Scripts\activate
pip install poetry
poetry install
```

Для Linux: </br>
```
git clone git@github.com:DmitriiParfenov/lms_system_project.git
python3 -m venv venv
source venv/bin/activate
curl -sSL https://install.python-poetry.org | python3
poetry install
```
# Установка и настройка Redis

- Установите Redis, если он не установлен. Для этого выполните в консоли:
```
sudo apt install redis-server
``` 
- Запустите Redis, выполнив в консоли:
```
sudo service redis-server start
``` 
- Произойдет запуск Redis сервера на порту 6379. Для того, чтобы убедиться, что сервер запущен, необходимо выполнить
в консоли команду, ответом которой должен быть `PONG`.
```
redis-cli ping
```

# Работа с базой данной PostgreSQL

- Установите PostgreSQL, если он не установлен. Для этого, например для Ubuntu, выполните в консоли:
```
sudo apt install postgresql
```
- Выполните вход в интерактивную оболочку PostgreSQL от имени `postgresql`, выполнив в консоли:
```
sudo -i -u postgres psql
```
- Создайте базу данный для проекта, выполнив в консоли:
```
CREATE DATABASE lms_system_project;
```
- Закройте интерактивную оболочку PostgreSQL:
```
\q
```
# Работа с переменными окружения

- В директории `lms_system_project` создайте файл `.env`. Пример содержимого файла:
```
password=пароль для пользователя postgresql
```
# Работа с миграциями

Из директории `sender_project` выполните в консоли: </br>

```
python manage.py migrate
```

# Запуск сервера Django

- Активируйте виртуальное окружение согласно п. `Клонирование репозитория` </br>

- Из  директории `lms_system_project` выполните в консоли: </br>
```
python manage.py runserver
```  
или 
```
python3 manage.py runserver
```
