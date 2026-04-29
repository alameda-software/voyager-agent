.PHONY: up down restart db logs migrate shell

# Docker Compose
up:
	cd docker && docker compose up -d

down:
	cd docker && docker compose down

restart:
	cd docker && docker compose restart

logs:
	cd docker && docker compose logs -f api

# Database
migrate:
	cd services/api && alembic upgrade head

makemigration:
	cd services/api && alembic revision --autogenerate -m "$(m)"

db-shell:
	cd docker && docker compose exec postgres psql -U postgres -d voyager

# Backend
shell:
	cd docker && docker compose exec api bash

api-docs:
	@echo "Open http://localhost:8000/docs"

# Mobile
mobile:
	@echo "Run: cd apps/mobile && npm install && npx expo start"

# Full reset
reset:
	cd docker && docker compose down -v
	rm -rf services/api/.mypy_cache services/api/.pytest_cache services/api/__pycache__
	@echo "Run 'make up' to start fresh"
