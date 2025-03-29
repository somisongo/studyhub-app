# Makefile for StudyHub Project

.PHONY: help setup dev dev-backend dev-frontend build test clean

# Variables
DOCKER_COMPOSE = docker-compose
FRONTEND_DIR = frontend
BACKEND_DIR = backend

# Instructions d'aide
help:
	@echo "StudyHub - Application Intelligente de Prise de Notes"
	@echo ""
	@echo "Commandes disponibles:"
	@echo "  make setup       - Prépare l'environnement de développement"
	@echo "  make dev         - Lance tous les services en mode développement"
	@echo "  make dev-backend - Lance uniquement le backend et ses dépendances"
	@echo "  make dev-frontend - Lance uniquement le frontend"
	@echo "  make build       - Construit les images Docker"
	@echo "  make test        - Exécute les tests"
	@echo "  make clean       - Nettoie l'environnement"
	@echo ""

# Configuration initiale
setup:
	@echo "Installation des dépendances et configuration de l'environnement..."
	cp -n .env.example .env || true
	cd $(BACKEND_DIR) && python -m venv venv && \
		. venv/bin/activate && \
		pip install -r requirements.txt
	cd $(FRONTEND_DIR) && npm install
	@echo "Configuration terminée!"

# Développement complet
dev:
	@echo "Lancement de tous les services..."
	$(DOCKER_COMPOSE) up -d postgres mongodb rabbitmq redis minio
	cd $(BACKEND_DIR) && . venv/bin/activate && \
		uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 & \
	cd $(FRONTEND_DIR) && npm run dev

# Développement backend uniquement
dev-backend:
	@echo "Lancement du backend et ses dépendances..."
	$(DOCKER_COMPOSE) up -d postgres mongodb rabbitmq redis minio
	cd $(BACKEND_DIR) && . venv/bin/activate && \
		uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Développement frontend uniquement
dev-frontend:
	@echo "Lancement du frontend..."
	cd $(FRONTEND_DIR) && npm run dev

# Construction des images Docker
build:
	@echo "Construction des images Docker..."
	$(DOCKER_COMPOSE) build

# Exécution des tests
test:
	@echo "Exécution des tests..."
	cd $(BACKEND_DIR) && . venv/bin/activate && pytest
	cd $(FRONTEND_DIR) && npm test

# Nettoyage
clean:
	@echo "Nettoyage de l'environnement..."
	$(DOCKER_COMPOSE) down -v
	rm -rf $(BACKEND_DIR)/venv
	rm -rf $(FRONTEND_DIR)/node_modules
	rm -rf $(FRONTEND_DIR)/build
	@echo "Nettoyage terminé!"
