# Makefile for quick local development commands

.PHONY: help up up-build up-full down logs

help:
	@echo "Available commands:"
	@echo "  make up         - Start backend/frontend/db/redis with docker compose"
	@echo "  make up-build   - Rebuild images then start services"
	@echo "  make up-full    - Build + start + run frontend dev server (for local)")
	@echo "  make down       - Stop all services"
	@echo "  make logs       - Tail logs"

up:
	docker compose up -d

up-build:
	docker compose up --build -d

up-full:
	docker compose up --build -d
	@echo "Waiting a few seconds for services to become healthy..."
	sleep 5
	cd frontend && npm install && npm run dev

down:
	docker compose down

logs:
	docker compose logs -f
