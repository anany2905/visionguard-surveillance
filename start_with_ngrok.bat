@echo off
echo ==========================================
echo    VisionGuard - Start with Public URL
echo ==========================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install from https://python.org
    pause
    exit /b 1
)

:: Check ngrok
ngrok version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ==========================================
    echo    NGROK NOT FOUND
    echo ==========================================
    echo.
    echo Please install ngrok:
    echo 1. Go to https://ngrok.com/download
    echo 2. Download for Windows
    echo 3. Extract and add to PATH
    echo    OR copy ngrok.exe to this folder
    echo.
    echo Alternative: Use start.bat for local-only access
    echo.
    pause
    exit /b 1
)

:: Setup venv
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat

:: Install deps
echo Installing dependencies...
pip install -q -r requirements.txt

:: Start Flask server in background
echo.
echo Starting Flask server...
start /b python backend/app.py > server.log 2>&1

:: Wait for server
echo Waiting for server...
timeout /t 5 /nobreak >nul

:: Start ngrok
echo.
echo Starting ngrok tunnel...
echo ==========================================
start "ngrok" cmd /k "ngrok http 5000"

:: Wait for ngrok to initialize
timeout /t 5 /nobreak >nul

:: Get public URL
echo.
echo ==========================================
echo    FETCHING PUBLIC URL...
echo ==========================================
echo.
curl -s http://localhost:4040/api/tunnels | findstr "public_url"
echo.
echo ==========================================
echo    ^^ Copy the https:// URL above
echo    Share with your professor!
echo ==========================================
echo.

:: Open local browser too
start http://localhost:5000

echo Press any key to stop server...
pause >nul

:: Cleanup
taskkill /f /im ngrok.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1
echo Server stopped.
