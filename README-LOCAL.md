# Guide de Développement Local pour StudyHub (Sans Docker)

Ce guide vous aide à configurer et lancer StudyHub en mode développement local sans utiliser Docker, ce qui peut être utile si Docker ralentit votre machine de développement.

## Prérequis

Avant de commencer, vous devez installer localement:

1. **Python 3.9+**
2. **Node.js 16+** et **npm**
3. **PostgreSQL** (pour la base de données relationnelle)
4. **MongoDB** (pour la base de données de documents)

> **Note**: Pour un développement initial, vous pouvez vous concentrer uniquement sur PostgreSQL et MongoDB. Les autres services (RabbitMQ, Redis, MinIO) ne sont pas strictement nécessaires pour commencer à développer.

## Configuration de l'environnement

### 1. Cloner le dépôt

```bash
git clone https://github.com/somisongo/studyhub-app.git
cd studyhub-app
```

### 2. Configuration des variables d'environnement

Nous fournissons un fichier `.env.local` spécialement configuré pour le développement sans Docker:

```bash
# Si vous utilisez Bash/Git Bash/Linux/MacOS
cp .env.local .env

# Si vous utilisez Windows CMD
copy .env.local .env
```

### 3. Installation des dépendances

Utilisez notre Makefile pour installer les dépendances:

```bash
# Linux/MacOS/Git Bash
make setup-local

# Windows (sans Make)
cd backend
python -m venv venv
venv\Scripts\activate
```

#### Installation des dépendances avec problèmes d'installation

Nous fournissons plusieurs options pour les dépendances:

```bash
# Option 1: Installer uniquement les dépendances minimales (recommandé pour démarrer)
pip install --upgrade pip setuptools wheel
pip install -r requirements-minimal.txt

# Option 2: Installer toutes les dépendances avec des versions flexibles
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Option 3: Installer les dépendances par groupes
pip install --upgrade pip setuptools wheel
pip install fastapi uvicorn pydantic python-multipart email-validator
pip install sqlalchemy alembic psycopg2-binary pymongo motor
pip install python-jose passlib bcrypt python-dotenv
pip install aiofiles aiohttp pika pillow tqdm loguru httpx tenacity
pip install pytest pytest-cov pytest-asyncio

# Installer les packages d'IA uniquement si nécessaire et un par un
pip install torch
pip install transformers
pip install numpy pandas scikit-learn
pip install nltk spacy gensim
pip install pytesseract opencv-python
```

Après l'installation du backend, installez les dépendances frontend:

```bash
cd ..
cd frontend
npm install
cd ..
```

## Configuration des bases de données

### PostgreSQL

1. Assurez-vous que PostgreSQL est installé et en cours d'exécution
2. Créez une base de données 'studyhub':
   ```sql
   CREATE DATABASE studyhub;
   ```
3. Les identifiants par défaut sont:
   - Utilisateur: postgres
   - Mot de passe: postgres
   - Vous pouvez les modifier dans le fichier `.env`

### MongoDB

1. Assurez-vous que MongoDB est installé et en cours d'exécution
2. La base de données 'studyhub' sera créée automatiquement lors de la première utilisation

## Lancement de l'application

### Option 1: Lancer l'application complète (backend + frontend)

```bash
# Avec Make
make dev-local

# Sans Make (lancer dans deux terminaux différents)
# Terminal 1 (Backend)
cd backend
venv\Scripts\activate  # Windows
# OU . venv/bin/activate  # Linux/MacOS
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 (Frontend)
cd frontend
npm run dev
```

### Option 2: Lancer uniquement le backend

```bash
# Avec Make
make dev-backend-local

# Sans Make
cd backend
venv\Scripts\activate  # Windows
# OU . venv/bin/activate  # Linux/MacOS
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Lancer uniquement le frontend

```bash
# Avec Make
make dev-frontend

# Sans Make
cd frontend
npm run dev
```

## Accès à l'application

- **Frontend**: http://localhost:3000
- **API Backend**: http://localhost:8000
- **Documentation API**: http://localhost:8000/docs

## Dépannage

### Erreurs d'installation des packages Python

- Si vous rencontrez des erreurs avec `torch`, `transformers` ou d'autres packages d'IA:
  1. Utilisez le fichier `requirements-minimal.txt` pour commencer
  2. Installez les packages problématiques séparément sans spécifier de version
  3. En cas d'erreur avec setuptools, exécutez `pip install --upgrade pip setuptools wheel` avant d'installer d'autres packages

### Erreur de connexion aux bases de données

- Vérifiez que PostgreSQL et MongoDB sont en cours d'exécution
- Vérifiez les identifiants dans le fichier `.env`
- Vérifiez les ports (PostgreSQL: 5432, MongoDB: 27017)

### Erreurs liées aux services manquants

Si vous rencontrez des erreurs concernant RabbitMQ, Redis ou MinIO, vous pouvez:

1. Commenter temporairement le code correspondant dans `backend/app/main.py`
2. OU installer ces services localement si vous avez besoin de fonctionnalités qui en dépendent

## Nettoyage

Pour nettoyer l'environnement de développement:

```bash
make clean

# Sans Make
cd backend
deactivate
rmdir /s /q venv
cd ..
cd frontend
rmdir /s /q node_modules
cd ..
```
