# ПЛОВ

[![pipeline status](https://gitlab.crja72.ru/django/2025/spring/course/projects/team-4/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2025/spring/course/projects/team-4/commits/main)

---

## Инструкция по запуску проекта в dev-режиме

## Общие требования

Перед тем как запустить проект, убедитесь, что у вас установлены следующие компоненты:

- **Python** (рекомендуется версия 3.10 и выше)
- **PostgreSQL** (База данных)
- **Git** (для клонирования репозитория)

## Клонирование проекта

1. Откройте терминал.
2. Перейдите в директорию, где хотите разместить проект.
3. Выполните команду для клонирования репозитория:
   - **Через SSH**:

     ```bash
     git clone git@gitlab.crja72.ru:django/2025/spring/course/projects/team-4.git
     ```

   - **Через HTTPS**:

     ```bash
     git clone https://gitlab.crja72.ru/django/2025/spring/course/projects/team-4.git
     ```

4. Перейдите в директорию проекта:

   ```bash
   cd team-4
   ```

## Установка зависимостей

1. Установите poetry:
   - **Linux/MacOS**:

     ```bash
     pip install poetry
     ```

2. Установите необходимые зависимости:

   ```bash
   poetry install --no-root
   ```

3. Активируйте виртуальное окружение:

   ```bash
     source .venv/bin/activate
   ```

## Заполните переменные окружения

1. Скопируйте образцовый файл с переменными окружения:
   - **Linux/MacOS**:

     ```bash
     cp .env-example .env
     ```

   - **Windows**:

     ```bash
     copy .env-example .env
     ```

2. Заполните файл `.env` своими значениями.


## База данных

1. Перейдите в директорию Django проекта:

   ```bash
   cd plov
   ```

2. Выполните миграции:

   ```bash
   python manage.py migrate
   ```

## Зарегистрировать админа

Для создания админа выполните эту команду и введите логин и пароль:

```bash
python manage.py createsuperuser
```

## Запуск проекта

1. Запустите сервер с помощью команды (вы должны находится в директории Django проекта):

   ```bash
   python manage.py runserver
   ```

2. Перейдите в браузер и откройте [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   или [http://localhost:8000/](http://localhost:8000/).
