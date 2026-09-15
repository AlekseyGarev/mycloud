# My Cloud — дипломное облачное хранилище

Fullstack SPA по ТЗ Netology: Django + Django REST Framework + PostgreSQL на сервере, React + Redux + React Router на клиенте. Пользователь может регистрироваться, входить по сессии, загружать, просматривать список, переименовывать, комментировать, скачивать, удалять и делиться файлами. Администратор управляет пользователями и любым пользовательским хранилищем.

## Структура

- `backend/config/` — настройки Django, маршрутизация, WSGI/ASGI.
- `backend/users/` — пользователь, регистрация/вход/выход, административные API, миграции.
- `backend/storage/` — модель файлов, API загрузки/редактирования/скачивания/публичных ссылок, удаление физических файлов.
- `backend/media/` — пользовательские файлы (в Git не публикуются).
- `frontend/src/` — React SPA, Redux store, страницы и API-клиент.
- `frontend/vite.config.js` — dev proxy и production build в `backend/frontend_dist`.

## Требования

- Python 3.10+
- PostgreSQL
- Node.js 18+
- npm

## Локальный запуск

### 1. PostgreSQL

Создайте БД и пользователя, например:

```sql
CREATE DATABASE mycloud_db;
CREATE USER mycloud_user WITH PASSWORD 'change-me';
GRANT ALL PRIVILEGES ON DATABASE mycloud_db TO mycloud_user;
```

### 2. Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Отредактируйте `.env`. Обязательно задайте `SECRET_KEY`, `DB_PASSWORD` и `ADMIN_INITIAL_PASSWORD`. Затем:

```bash
python manage.py migrate
python manage.py runserver
```

Миграция создаёт запись администратора `admin`. Если при первой миграции `ADMIN_INITIAL_PASSWORD` не был задан, пароль специально остаётся непригодным; задайте переменную и выполните:

```bash
python manage.py init_admin
```

### 3. Frontend в dev-режиме

```bash
cd frontend
npm ci
npm run dev
```

Vite работает на `http://127.0.0.1:5173` и проксирует `/api` на Django `:8000`.

## Production: один сервер для SPA и API

ТЗ требует, чтобы статические файлы фронтенда и API обслуживались единым сервером. Сборка Vite помещается в Django:

```bash
cd frontend
npm ci
npm run build
cd ../backend
python manage.py collectstatic --noinput
python manage.py migrate
```

После сборки Django отдаёт `frontend_dist/index.html`, а WhiteNoise — JS/CSS по `/static/`. Все SPA-маршруты (`/login`, `/storage`, `/admin`, `/share/<uuid>`) возвращают `index.html`, API остаётся под `/api/`.

Для production в `.env`:

```env
DEBUG=False
ALLOWED_HOSTS=your-domain.ru
CSRF_TRUSTED_ORIGINS=https://your-domain.ru
CORS_ALLOWED_ORIGINS=https://your-domain.ru
```

Запускайте WSGI-приложение `config.wsgi:application` через поддерживаемый reg.ru WSGI/Passenger/Gunicorn-вариант вашего тарифа. Рабочий каталог — `backend`, переменные окружения должны соответствовать `.env.example`. Настройте домен на HTTPS; при `DEBUG=False` cookies помечаются Secure.

## API

- `GET /api/auth/csrf/` — CSRF token.
- `POST /api/auth/register/` — регистрация.
- `POST /api/auth/login/`, `POST /api/auth/logout/`, `GET /api/auth/me/` — сессионная аутентификация.
- `GET/POST /api/files/` — список/загрузка файлов; администратор может передать `user_id`.
- `PATCH/DELETE /api/files/<id>/` — переименование/комментарий и удаление.
- `GET /api/files/<id>/download/` — скачивание с обновлением даты последнего скачивания.
- `POST /api/files/<id>/share/` — специальная обезличенная UUID-ссылка.
- `GET /api/public/files/<uuid>/` и `/download/` — публичная информация/скачивание.
- `/api/admin/users/` — список пользователей, объём/число файлов и управление правами.

Все приватные API проверяют сессию и права на хранилище. Изменяющие запросы защищены CSRF. Файлы на диске получают уникальные UUID-имена, независимо от исходных имён.

## Проверка

Backend-тесты можно запустить без PostgreSQL в локальном SQLite только для тестового прогона:

```bash
cd backend
DB_ENGINE=sqlite python manage.py test
```

Проверка frontend:

```bash
cd frontend
npm run lint
npm run build
```

## Важное перед публикацией

Не публикуйте `.env`, пользовательские файлы из `backend/media`, локальную БД, `node_modules` и `staticfiles`. `.gitignore` уже исключает их. Пароли и `SECRET_KEY` должны задаваться только через окружение.
