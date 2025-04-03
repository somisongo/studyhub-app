@echo off
echo ======================================
echo Configuration de StudyHub pour Windows
echo ======================================
echo.

:: Copier le fichier .env.local vers .env
echo Copie du fichier .env.local vers .env...
copy .env.local .env
echo.

:: Configuration du backend
echo Configuration du backend...
cd backend
echo Création de l'environnement virtuel Python...
python -m venv venv
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo Installation des outils de base...
pip install --upgrade pip setuptools wheel

echo.
echo Plusieurs options d'installation sont disponibles:
echo 1. Installer uniquement les dépendances minimales (recommandé)
echo 2. Installer toutes les dépendances avec des versions flexibles
echo 3. Quitter

set /p option=Entrez votre choix (1, 2 ou 3): 

if "%option%"=="1" (
    echo Installation des dépendances minimales...
    pip install -r requirements-minimal.txt
) else if "%option%"=="2" (
    echo Installation de toutes les dépendances...
    pip install -r requirements.txt
) else (
    echo Installation annulée.
    goto end_backend
)

:end_backend
cd ..
echo.

:: Configuration du frontend
echo Configuration du frontend...
cd frontend
echo Installation des dépendances Node.js...
npm install
cd ..
echo.

echo ======================================
echo Configuration terminée !
echo ======================================
echo.
echo Pour lancer le backend:
echo   cd backend
echo   venv\Scripts\activate
echo   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo.
echo Pour lancer le frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Pour plus d'informations, consultez le fichier README-LOCAL.md

pause
