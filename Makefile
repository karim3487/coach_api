build:
	docker-compose build

up:
	docker-compose up --remove-orphans -d

down:
	docker-compose down

migrate:
	docker-compose exec web uv run manage.py migrate

load_exercises:
	docker-compose exec web uv run manage.py import_exercises
	docker-compose exec web uv run manage.py migrate_exercises

createsuperuser:
	docker-compose exec web uv run python manage.py createsuperuser
