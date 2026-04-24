@echo off
echo ==========================================
echo    VisionGuard - Starting Server...
echo ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

:: Check if virtual environment exists, create if not
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

:: Start the server in background
echo.
echo Starting Flask server...
echo.
start /b python backend/app.py > server.log 2>&1

:: Wait for server to start
echo Waiting for server to start...
timeout /t 3 /nobreak >nul

:: Open browser
echo Opening browser...
start http://localhost:5000

echo.
echo ==========================================
echo    Server running at http://localhost:5000
echo    Press Ctrl+C to stop
echo ==========================================
echo.

:: Keep window open
python backend/app.py

pause
