@echo off
echo ======================================
echo Installation des dépendances manquantes
echo ======================================
echo.

cd backend

if exist venv (
    echo Activation de l'environnement virtuel...
    call venv\Scripts\activate.bat
) else (
    echo L'environnement virtuel n'existe pas. Veuillez exécuter setup-local.bat d'abord.
    goto end
)

echo Installation des packages manquants pour Pydantic v2...
pip install pydantic-settings pydantic-core typing-extensions

echo Vérification des autres dépendances essentielles...
pip install python-dotenv fastapi uvicorn

echo ======================================
echo Installation terminée !
echo ======================================
echo.
echo Pour lancer l'application, utilisez run-local.bat

:end
cd ..
pause
