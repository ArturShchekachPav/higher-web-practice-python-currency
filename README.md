# Currency Service

Сервис курсов валют с парсером данных ЦБ РФ.

## Стек

- **FastAPI** — REST API с JWT-авторизацией
- **SQLAlchemy 2.0** (async) + **asyncpg** — работа с PostgreSQL
- **Alembic** — миграции
- **Scrapy** — парсер сайта ЦБ РФ
- **APScheduler** — автозапуск парсера раз в сутки
- **Docker** + **Docker Compose** — контейнеризация

## Архитектура

```
api/          — HTTP-ручки (FastAPI)
domain/       — бизнес-логика (auth, users, currency)
core/         — конфиг, БД, security, зависимости, планировщик
parser/       — Scrapy spider + pipeline
alembic/      — миграции
```

## Запуск

### Шаги

1. Клонировать репозиторий:
   ```bash
   git clone <url>
   cd higher-web-practice-python-currency
   ```

2. Установить зависимости:
   ```bash
   uv sync
   ```

3. Создать `.env`:
   ```bash
   cp .env.example .env
   ```

4. Запустить всё через Docker:
   ```bash
   docker compose up -d --build
   ```

5. Открыть Swagger:
   http://127.0.0.1:8000/docs

## Ручки API

### Auth

- `POST /auth/login` — логин, возвращает access + refresh
- `POST /auth/refresh` — обновление токена

### Users

- `POST /users/register` — регистрация
- `GET /users/{user_id}` — получить пользователя (защищено)
- `GET /users/email/{email}` — получить по email (защищено)
- `PUT /users` — обновить профиль (защищено)

### Currencies

- `GET /currencies` — список валют (защищено)
- `GET /currencies/{code}` — последний курс (защищено)
- `GET /currencies/{code}/history?startdate=...&enddate=...` — история (защищено)
- `GET /currencies/{code}/all` — вся история (защищено)

## Парсер

Запускается автоматически раз в 24 часа через APScheduler.

Ручной запуск:
```bash
docker compose exec app sh -c "cd parser && scrapy crawl cbr -a days=30"
```

## Автор

**Артур Щекач**
- GitHub: [@ArturShchekachPav](https://github.com/ArturShchekachPav)
- Email: ashhekach@gmail.com

## Лицензия

Учебный проект.