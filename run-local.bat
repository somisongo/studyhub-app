@echo off
echo ======================================
echo Lancement de StudyHub en mode local
echo ======================================
echo.

echo Plusieurs options sont disponibles:
echo 1. Lancer le backend uniquement
echo 2. Lancer le frontend uniquement
echo 3. Lancer le backend et le frontend (dans deux fenêtres)
echo 4. Quitter

set /p option=Entrez votre choix (1, 2, 3 ou 4): 

if "%option%"=="1" (
    echo Lancement du backend...
    cd backend
    call venv\Scripts\activate.bat
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
) else if "%option%"=="2" (
    echo Lancement du frontend...
    cd frontend
    npm run dev
) else if "%option%"=="3" (
    echo Lancement du backend et du frontend...
    
    echo Lancement du backend dans une nouvelle fenêtre...
    start cmd /k "cd backend && call venv\Scripts\activate.bat && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
    
    echo Lancement du frontend dans cette fenêtre...
    cd frontend
    npm run dev
) else (
    echo Lancement annulé.
    goto end
)

:end
echo.
echo Pour plus d'informations, consultez le fichier README-LOCAL.md
pause
