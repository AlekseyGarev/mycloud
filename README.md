# My Cloud — дипломное облачное хранилище

**My Cloud** — fullstack SPA-приложение для облачного хранения файлов, разработанное в рамках дипломного проекта.

Приложение позволяет пользователям регистрироваться, авторизовываться, загружать и хранить файлы, переименовывать их, добавлять комментарии, скачивать, удалять и создавать специальные публичные ссылки.

Администратор может управлять пользователями приложения и работать с их файловыми хранилищами.

---

## Технологии

### Backend

- Python
- Django
- Django REST Framework
- PostgreSQL
- Gunicorn
- WhiteNoise

### Frontend

- React
- Redux Toolkit
- React Router
- Axios
- Vite

### Deployment

- Docker
- Docker Compose
- PostgreSQL в отдельном контейнере
- Git
- GitHub

---

## Возможности приложения

### Пользователь

Пользователь может:

- зарегистрироваться;
- войти и выйти из системы;
- просматривать собственное файловое хранилище;
- загружать один или несколько файлов;
- задавать имя файла;
- добавлять комментарий;
- переименовывать файл;
- изменять комментарий;
- скачивать файл;
- удалять файл;
- создавать специальную публичную ссылку;
- копировать публичную ссылку;
- открывать публичную ссылку без авторизации;
- просматривать дату загрузки;
- просматривать дату последнего скачивания;
- просматривать размер файла.

Обычный пользователь имеет доступ только к собственному файловому хранилищу.

### Администратор

Администратор может:

- просматривать список пользователей;
- просматривать количество файлов каждого пользователя;
- просматривать общий объём файлов пользователя;
- открывать хранилище любого пользователя;
- загружать файлы в хранилище выбранного пользователя;
- переименовывать файлы пользователя;
- изменять комментарии к файлам пользователя;
- скачивать файлы;
- удалять файлы;
- назначать пользователя администратором;
- снимать права администратора;
- удалять пользователей.

---

## Структура проекта

```text
mycloud/
├── backend/
│   ├── config/                 # Настройки Django
│   ├── storage/                # Работа с файлами
│   ├── users/                  # Пользователи и авторизация
│   ├── media/                  # Каталог пользовательских файлов
│   ├── manage.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   └── api/
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Переменные окружения

Реальные настройки приложения хранятся в файле `.env`.

Файл `.env` содержит секретные данные и **не должен добавляться в Git**.

Пример переменных окружения находится в:

```text
backend/.env.example
```

Для Docker-развёртывания необходимо создать файл:

```text
.env
```

в корневой директории проекта рядом с `docker-compose.yml`.

Пример:

```env
DEBUG=False

SECRET_KEY=your-secret-key

DB_NAME=mycloud
DB_USER=mycloud
DB_PASSWORD=your-strong-database-password
DB_HOST=db
DB_PORT=5432

ALLOWED_HOSTS=your-server-ip,127.0.0.1,localhost

ADMIN_USERNAME=cloudadmin
ADMIN_EMAIL=admin@example.com
ADMIN_INITIAL_PASSWORD=

SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

> Не публикуйте реальные значения `SECRET_KEY`, `DB_PASSWORD`, `ADMIN_INITIAL_PASSWORD` и пароли пользователей в GitHub.

### Настройки для HTTP

При работе приложения через обычный HTTP:

```env
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

### Настройки для HTTPS

После настройки HTTPS необходимо использовать:

```env
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

# Запуск проекта через Docker

## 1. Клонирование репозитория

```bash
git clone git@github.com:AlekseyGarev/mycloud.git
cd mycloud
```

---

## 2. Создание `.env`

Создайте `.env` в корневой директории проекта рядом с `docker-compose.yml`.

Заполните параметры PostgreSQL, Django и адрес сервера.

Для генерации `SECRET_KEY` на Linux можно использовать:

```bash
openssl rand -hex 32
```

Для генерации пароля PostgreSQL:

```bash
openssl rand -hex 24
```

---

## 3. Сборка и запуск контейнеров

```bash
docker compose up -d --build
```

Во время сборки Docker выполняет:

1. установку frontend-зависимостей;
2. production-сборку React;
3. установку Python-зависимостей;
4. копирование собранного frontend в Django;
5. выполнение `collectstatic`;
6. подготовку Django-приложения;
7. запуск Django через Gunicorn;
8. запуск PostgreSQL в отдельном контейнере.

---

## 4. Применение миграций

После первого запуска необходимо применить миграции:

```bash
docker compose exec web python manage.py migrate
```

---

## 5. Создание администратора

Администратора можно создать стандартной командой Django:

```bash
docker compose exec web python manage.py createsuperuser
```

Пользователь с правами Django superuser имеет доступ к административным возможностям My Cloud.

В проекте также предусмотрена команда:

```bash
docker compose exec web python manage.py init_admin
```

Она использует переменные окружения:

```env
ADMIN_USERNAME=cloudadmin
ADMIN_EMAIL=admin@example.com
ADMIN_INITIAL_PASSWORD=your-password
```

`ADMIN_INITIAL_PASSWORD` должен быть задан только в окружении и не должен храниться в Git.

---

## 6. Проверка контейнеров

Проверить состояние контейнеров:

```bash
docker compose ps
```

Контейнеры `web` и `db` должны находиться в состоянии `Up`.

Логи Django/Gunicorn:

```bash
docker compose logs web --tail=100
```

Логи PostgreSQL:

```bash
docker compose logs db --tail=100
```

---

## Открытие приложения

При текущем HTTP-развёртывании приложение доступно по адресу:

```text
http://SERVER_IP:8000
```

Необходимо заменить `SERVER_IP` на публичный IP-адрес сервера.

---

# Обновление проекта на сервере

Основная версия исходного кода хранится в GitHub.

Рабочий процесс разработки:

```text
VS Code
   ↓
Git commit
   ↓
GitHub
   ↓
Server: git pull
   ↓
Docker rebuild
```

После изменения проекта локально:

```bash
git add .
git commit -m "Описание изменения"
git push origin main
```

На сервере:

```bash
cd /opt/mycloud/mycloud

git fetch origin
git pull origin main

docker compose up -d --build
```

`collectstatic` выполняется автоматически во время Docker-сборки.

Данные PostgreSQL и пользовательские файлы хранятся в Docker volumes, поэтому обычная пересборка контейнеров их не удаляет.

Не используйте:

```bash
docker compose down -v
```

если необходимо сохранить данные.

Параметр `-v` удаляет Docker volumes, что может привести к удалению базы данных и пользовательских файлов.

---

# API

## Авторизация

```text
GET  /api/auth/csrf/
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
GET  /api/auth/me/
```

Авторизация реализована через Django Session Authentication.

Изменяющие запросы защищены CSRF.

---

## Файлы

```text
GET    /api/files/
POST   /api/files/
PATCH  /api/files/<id>/
DELETE /api/files/<id>/
GET    /api/files/<id>/download/
POST   /api/files/<id>/share/
```

Обычный пользователь может работать только со своими файлами.

Администратор может работать с хранилищем выбранного пользователя.

---

## Публичные ссылки

```text
GET /api/public/files/<uuid>/
GET /api/public/files/<uuid>/download/
```

Публичная ссылка позволяет получить информацию о файле и скачать его без авторизации.

Для ссылки используется UUID, поэтому внутренний путь хранения файла не раскрывается.

---

## Администрирование

```text
GET    /api/admin/users/
PATCH  /api/admin/users/<id>/
DELETE /api/admin/users/<id>/
GET    /api/admin/users/<id>/files/
```

Доступ к административным API разрешён только пользователям с соответствующими правами.

---

# Хранение файлов

Физические пользовательские файлы находятся в каталоге `media`.

Для хранения на диске используется уникальное имя файла. Это предотвращает конфликт файлов с одинаковыми исходными названиями.

Для каждого пользователя используется отдельное файловое хранилище.

В базе данных сохраняется информация о файле, включая:

- исходное имя;
- размер;
- дату загрузки;
- дату последнего скачивания;
- комментарий;
- путь хранения;
- специальную публичную ссылку;
- владельца файла.

При удалении записи о файле физический файл также удаляется с диска.

При удалении пользователя связанные с ним файлы также удаляются.

---

# Безопасность

В проекте используются:

- Django Session Authentication;
- CSRF-защита;
- проверка прав доступа;
- разграничение пользовательских хранилищ;
- ограничения административных API;
- UUID для публичных ссылок;
- переменные окружения для секретных данных;
- исключение `.env` из Git;
- ограничения частоты запросов для регистрации и авторизации;
- отдельные настройки secure cookies для HTTP/HTTPS.

Обычный пользователь не может получить доступ к файлам другого пользователя через API.

Реальные пароли, `SECRET_KEY` и другие секретные данные не должны попадать в GitHub.

---

# Логирование

Django и приложение записывают информацию о важных событиях, включая действия пользователей и операции с файлами.

При Docker-развёртывании логи приложения можно просмотреть командой:

```bash
docker compose logs web --tail=100
```

Для просмотра логов в реальном времени:

```bash
docker compose logs -f web
```

В логах фиксируются, в частности, операции авторизации и действия с пользовательскими файлами.

---

# Локальная разработка

## Backend

Перейдите в каталог backend:

```bash
cd backend
```

Создайте виртуальное окружение:

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

Создайте `.env` на основе `.env.example`.

Затем выполните:

```bash
python manage.py migrate
python manage.py runserver
```

---

## Frontend

Перейдите в каталог frontend:

```bash
cd frontend
```

Установите зависимости:

```bash
npm ci
```

Запустите frontend в режиме разработки:

```bash
npm run dev
```

Vite запускает frontend в dev-режиме и проксирует `/api` на Django.

---

# Проверка проекта

## Backend

### Проверка конфигурации Django

В Docker:

```bash
docker compose exec web python manage.py check
```

При корректной конфигурации Django выводит:

```text
System check identified no issues (0 silenced).
```

### Автоматические тесты

В Docker:

```bash
docker compose exec web python manage.py test
```

В текущей версии проекта реализовано 6 backend-тестов.

При успешном прохождении:

```text
Ran 6 tests in ...
OK
```

При локальной разработке также можно использовать тестовую конфигурацию с SQLite, если она предусмотрена настройками проекта:

```bash
cd backend
DB_ENGINE=sqlite python manage.py test
```

---

## Frontend

Установите зависимости:

```bash
cd frontend
npm ci
```

Проверка ESLint:

```bash
npm run lint
```

Проверка production-сборки:

```bash
npm run build
```

Успешная production-сборка завершается сообщением вида:

```text
✓ built in ...
```

---

# Production и HTTPS

Текущий вариант приложения может работать непосредственно через:

```text
http://SERVER_IP:8000
```

Для полноценного production-развёртывания рекомендуется использовать:

- доменное имя;
- reverse proxy;
- HTTPS.

После настройки HTTPS необходимо установить:

```env
DEBUG=False

SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

Также необходимо указать домен:

```env
ALLOWED_HOSTS=your-domain.ru
CSRF_TRUSTED_ORIGINS=https://your-domain.ru
```

После изменения `.env` web-контейнер необходимо пересоздать:

```bash
docker compose up -d --force-recreate web
```

---

# Сохранность данных

PostgreSQL и пользовательские файлы хранятся в Docker volumes.

Поэтому команды:

```bash
docker compose up -d
docker compose up -d --build
```

не должны удалять пользовательские данные.

Для просмотра volumes:

```bash
docker volume ls
```

Не выполняйте:

```bash
docker compose down -v
```

если необходимо сохранить базу данных и загруженные файлы.

---

# Важные файлы, которые не должны попадать в Git

Не должны публиковаться:

```text
.env
node_modules/
backend/media/*
backend/staticfiles/
__pycache__/
*.pyc
```

Правила исключения находятся в `.gitignore`.

Файл `.env.example` содержит только пример конфигурации и может храниться в репозитории.

---

# Проверенный функционал

В ходе проверки проекта были протестированы:

- регистрация пользователя;
- вход и выход из системы;
- загрузка файлов;
- скачивание файлов;
- отображение даты последнего скачивания;
- переименование файлов;
- добавление и изменение комментариев;
- удаление файлов;
- создание публичных ссылок;
- копирование публичных ссылок;
- скачивание файла по публичной ссылке без авторизации;
- изоляция файлов разных пользователей;
- просмотр пользовательских хранилищ администратором;
- назначение прав администратора;
- снятие прав администратора;
- удаление пользователей;
- физическое удаление файлов;
- сохранность данных после пересборки Docker;
- логирование;
- Django system check;
- backend-тесты;
- ESLint;
- production-сборка React.

---

# Репозиторий

Проект разработан в качестве дипломной работы — облачного файлового хранилища **My Cloud**.

Исходный код проекта хранится в публичном GitHub-репозитории.