@echo off
REM Script per compilare l'applicazione in EXE con PyInstaller
REM Uso: build.bat

echo ============================================================
echo   Google Reviews Scraper - Build Script
echo ============================================================
echo.

REM Controlla se Python è installato
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRORE] Python non trovato. Installa Python 3.10+ da python.org
    pause
    exit /b 1
)

echo [1/5] Installazione dipendenze...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERRORE] Installazione dipendenze fallita
    pause
    exit /b 1
)

echo.
echo [2/5] Installazione PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo [ERRORE] Installazione PyInstaller fallita
    pause
    exit /b 1
)

echo.
echo [3/5] Installazione browser Playwright...
python -m playwright install chromium
if errorlevel 1 (
    echo [ERRORE] Installazione browser fallita
    pause
    exit /b 1
)

echo.
echo [4/5] Compilazione EXE con PyInstaller...
pyinstaller --onefile --name scraper --icon=NONE ^
    --add-data "src;src" ^
    --hidden-import playwright ^
    --hidden-import dbf ^
    --collect-all playwright ^
    src/main.py

if errorlevel 1 (
    echo [ERRORE] Compilazione fallita
    pause
    exit /b 1
)

echo.
echo [5/5] Pulizia file temporanei...
if exist build rmdir /s /q build
if exist scraper.spec del scraper.spec

echo.
echo ============================================================
echo   BUILD COMPLETATO CON SUCCESSO!
echo   File EXE: dist\scraper.exe
echo ============================================================
echo.
pause
