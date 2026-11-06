# Accommodation Service

## Требования

- `Python 3.12+`
- `PostgreSQL 16+`
- `venv` или другое виртуальное окружение

## Переменные окружения

Сервис читает настройки из `.env`. Для локального запуска достаточно следующих переменных:

```env
DB_ACCOMMODATION_SERVICE_HOST=127.0.0.1
DB_ACCOMMODATION_SERVICE_PORT=5432
DB_ACCOMMODATION_SERVICE_NAME=accommodation_db
DB_ACCOMMODATION_SERVICE_USER=platform
DB_ACCOMMODATION_SERVICE_PASS=12345
DEBUG=false
```

Дополнительные переменные окружения будут добавляться по мере реализации функциональности сервиса.

## Локальный запуск

1. Клонируйте репозиторий и перейдите в директорию проекта:

```bash
cd accommodation-service
```

2. Создайте и активируйте виртуальное окружение:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корне проекта и укажите необходимые настройки.

5. Запустите сервис:

```bash
uvicorn main:app --reload
```

## Проверка

После запуска сервис доступен по адресам:

- `http://127.0.0.1:8000/api/accommodation/docs` — документация Swagger UI.
- `http://127.0.0.1:8000/api/accommodation/openapi.json` — схема OpenAPI.
- `http://127.0.0.1:8000/api/accommodation/health` — проверка состояния сервиса.

## Миграции базы данных

Для управления миграциями используется Alembic.

### Создание миграции

После изменения моделей SQLAlchemy создайте миграцию:

```bash
alembic revision --autogenerate -m "описание изменений"
```

### Применение миграций

Применить все миграции к базе данных:

```bash
alembic upgrade head
```

### Откат последней миграции

```bash
alembic downgrade -1
```

### Просмотр текущей версии

```bash
alembic current
```

### Просмотр истории миграций

```bash
alembic history
```

Перед созданием миграций убедитесь, что база данных доступна, а переменные окружения для подключения настроены.

## Тесты

Установка тестовых зависимостей:

```bash
pip install -r requirements.test.txt
```

Запуск тестов:

```bash
pytest
```


## API Endpoints

API-ручки для поиска отелей, получения информации о размещении, предложениях и справочных данных.

### `accommodation`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/accommodation/health` | Проверка состояния сервиса |
| GET | `/api/accommodation/suggest` | Подсказки по регионам и отелям |
| GET | `/api/accommodation/search` | Поиск отелей с предложениями |
| GET | `/api/accommodation/{hotel_id}` | Получение информации об отеле |
| GET | `/api/accommodation/{hotel_id}/images` | Получение фотографий отеля |
| GET | `/api/accommodation/{hotel_id}/offers` | Получение номеров и цен |
| GET | `/api/accommodation/{hotel_id}/reviews` | Получение отзывов |
| GET | `/api/accommodation/top-offers` | Получение лучших предложений по списку `hotel_id` |
| GET | `/api/accommodation/filters` | Получение доступных фильтров и их значений |

### `references`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/accommodation/references/meal-types` | Справочник типов питания |
| GET | `/api/accommodation/references/accomm-types` | Справочник типов размещения |
| GET | `/api/accommodation/references/amenities` | Справочник удобств |

### `admin`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/admin/accommodation/feed/sync` | Запуск синхронизации фида отелей |
| GET | `/api/admin/accommodation/feed/status` | Получение статуса синхронизации фида |
| GET | `/api/admin/accommodation/cache/stats` | Получение статистики кэша |
