# 🏋️‍♂️ Coach API

A Django + DRF-based backend for managing workout plans, exercise tracking, user progress, and Telegram bot integration. Includes Celery, PostgreSQL, MinIO, Redis, and uv for dependency management.

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-org/coach-api.git
cd coach-api
````

### 2. Create .env file

Copy the example environment file and customize it:

```bash
cp .env.prod.example .env.prod
```

You can edit .env and adjust variables as needed:

```dotenv
# App
ENV=prod
SECRET_KEY='123abc'

# PostgreSQL
POSTGRES_DB_NAME=coach_bot
POSTGRES_USER=django
POSTGRES_PASSWORD=secret
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Third party
RAPIDAPI_KEY='key'
```

This file is required by Django and services to work properly in production/dev.

### 3. Start Docker services

```bash
make build && make down && make up
```

This starts:

* web – Django + Uvicorn server
* db – PostgreSQL
* minio – object storage for media files
* redis – task broker
* celery – async task worker

### 4. Set up MinIO storage

1. Open [http://localhost:9001](http://localhost:9001)
2. Login with:

   * username: `minioadmin`
   * password: `minioadmin`
3. Click “Create a bucket”
4. Name it `coach-media` and click "Create"

### 5. Apply database migrations

```bash
make migrate
```

### 6. Load exercises

```bash
make load_exercises
```

---

## 📦 Common Commands

| Command                        | Description                  |
| ------------------------------ | ---------------------------- |
| `make migrate`                 | Run migrations               |
| `make createsuperuser`         | Create Django superuser      |
| `make load_exercises`          | Import initial exercise data |
| `docker-compose exec web bash` | Enter the web container      |

---

## 🔗 Useful URLs

* Admin Panel: [http://localhost:8000/admin/](http://localhost:8000/admin/)
* Swagger UI: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
* ReDoc: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)
* MinIO UI: [http://localhost:9001](http://localhost:9001)
