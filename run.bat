@echo off
title WomenHealth AI
color 0D
cls

echo.
echo  ============================================
echo      WomenHealth AI - Final Year Project
echo  ============================================
echo.
echo  Starting server... Please wait...
echo.

:: Go to project folder
cd /d "%~dp0"

:: Create venv if not exists
if not exist "venv" (
    echo  Setting up environment for first time...
    python -m venv venv
    call venv\Scripts\activate
    pip install flask flask-sqlalchemy werkzeug scikit-learn numpy --quiet
) else (
    call venv\Scripts\activate
)

echo  Launching WomenHealth AI in your browser...
echo.
echo  URL: http://127.0.0.1:5000
echo.
echo  Press CTRL+C to stop the server
echo  ============================================
echo.

python app.py
pause
