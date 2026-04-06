@echo off
echo ========================================
echo    TELEGRAM GROUP FORWARDER
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed.
    echo Please install it from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

:: Install telethon if not installed
echo Checking dependencies...
pip show telethon >nul 2>&1
if errorlevel 1 (
    echo Installing telethon...
    pip install telethon
)

echo.
echo Starting forwarder...
echo.
python forwarder.py %*
pause
