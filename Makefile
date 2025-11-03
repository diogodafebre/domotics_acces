.PHONY: help up down logs clean test migrate seed lint format

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start all services (dev)
	docker compose -f deploy/docker-compose.dev.yml up -d

up-build: ## Build and start all services (dev)
	docker compose -f deploy/docker-compose.dev.yml up --build -d

down: ## Stop all services
	docker compose -f deploy/docker-compose.dev.yml down

logs: ## Tail logs from all services
	docker compose -f deploy/docker-compose.dev.yml logs -f

clean: ## Clean docker containers, volumes, and images
	docker compose -f deploy/docker-compose.dev.yml down -v --rmi local

migrate: ## Run database migrations
	docker compose -f deploy/docker-compose.dev.yml exec api alembic upgrade head

seed: ## Seed database with test data
	docker compose -f deploy/docker-compose.dev.yml exec api python ops/scripts/seed.py

test-backend: ## Run backend tests
	docker compose -f deploy/docker-compose.dev.yml exec api pytest -v

test-mobile: ## Run mobile tests
	cd mobile && flutter test

lint-backend: ## Lint backend code
	cd backend && ruff check . && black --check . && isort --check-only .

lint-mobile: ## Lint mobile code
	cd mobile && flutter analyze

format-backend: ## Format backend code
	cd backend && black . && isort .

format-mobile: ## Format mobile code
	cd mobile && dart format .

prod-up: ## Start production stack
	docker compose -f deploy/docker-compose.prod.yml up -d

prod-down: ## Stop production stack
	docker compose -f deploy/docker-compose.prod.yml down
