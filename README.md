# 🔗 URL Shortener API

Асинхронный сервис для сокращения URL-адресов, построенный на FastAPI с кешированием через Redis и хранением данных в PostgreSQL.

##  Стек технологий

- **FastAPI** — асинхронный веб-фреймворк
- **PostgreSQL** — основная база данных
- **SQLAlchemy** — ORM для работы с БД
- **Alembic** — миграции базы данных
- **Redis** — кеширование коротких ссылок
- **Docker / Docker Compose** — контейнеризация
- **Pydantic** — валидация данных

##  Функциональность

- Создание короткой ссылки из оригинального URL
- Перенаправление по короткой ссылке на оригинальный URL
- Кеширование переходов через Redis (Cache-Aside паттерн)
- Валидация входящих URL через Pydantic `HttpUrl`
- Пагинация списка ссылок
- Защита от коллизий коротких кодов

##  Структура проекта

```
url-shortener/
├── app/
│   ├── main.py              # Точка входа, lifespan
│   ├── config.py            # Настройки через pydantic-settings
│   ├── database.py          # Async подключение к БД
│   ├── redis_client.py      # Redis клиент
│   ├── models/
│   │   └── url.py           # SQLAlchemy модель
│   ├── repositories/
│   │   └── url.py           # Слой работы с БД
│   ├── services/
│   │   └── url.py           # Бизнес-логика
│   ├── routers/
│   │   └── url.py           # Эндпоинты
│   └── schemas/
│       └── url.py           # Pydantic схемы
├── migrations/              # Alembic миграции
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
```

##  Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone https://github.com/eternal-silence00/Url_Shortener.git
cd Url_Shortener
```

### 2. Создать `.env` файл

```properties
DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/urlshortener
REDIS_URL=redis://redis:6379
BASE_URL=http://localhost:8000
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=urlshortener
```

### 3. Запустить через Docker

```bash
docker-compose up --build
```

### 4. Применить миграции

```bash
docker-compose exec app alembic upgrade head
```

### 5. Открыть документацию

```
http://localhost:8000/docs
```

## 📮 API Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/url` | Создать короткую ссылку |
| `GET` | `/url` | Получить список ссылок |
| `GET` | `/{short_code}` | Перейти по короткой ссылке |

### POST /url

**Request:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "short_url": "http://localhost:8000/9EIxghlj"
}
```

### GET /{short_code}

Перенаправляет на оригинальный URL. Сначала проверяет кеш Redis, затем обращается к БД.

##  Архитектурные решения

**Cache-Aside паттерн** — при переходе по короткой ссылке сначала проверяется Redis. Если ссылка есть в кеше — редирект без обращения к БД. TTL кеша — 5 минут.

**Защита от коллизий** — при генерации короткого кода производится проверка его уникальности. В случае коллизии генерируется новый код (до 5 попыток).

**Идемпотентность** — повторный запрос с тем же URL вернёт уже существующую короткую ссылку без создания дубликата.