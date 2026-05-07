.PHONY: up down restart logs migrate makemigration db-shell shell api-docs mobile reset dev-db dev-api-setup dev-api dev-web dev-mobile export-web

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
	cd services/api && ./.venv/bin/alembic upgrade head

makemigration:
	cd services/api && ./.venv/bin/alembic revision --autogenerate -m "$(m)"

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

dev-db:
	cd docker && docker compose up -d postgres redis

dev-api-setup:
	cd services/api && python3.11 -m venv .venv
	cd services/api && ./.venv/bin/python -m ensurepip --upgrade
	cd services/api && ./.venv/bin/python -m pip install --upgrade pip setuptools wheel
	cd services/api && ./.venv/bin/python -m pip install -e ".[dev]"

dev-api:
	cd services/api && ./.venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-web:
	cd apps/mobile && npx expo start --web --clear

dev-mobile:
	cd apps/mobile && npx expo start

export-web:
	cd apps/mobile && npx expo export --platform web

# Full reset
reset:
	cd docker && docker compose down -v
	rm -rf services/api/.mypy_cache services/api/.pytest_cache services/api/__pycache__
	@echo "Run 'make up' to start fresh"
