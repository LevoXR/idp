@echo off
echo ========================================
echo Aditya Setu Desktop - Installation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/3] Checking COVID data file...
if not exist "statw.txt" (
    if exist "..\statw.txt" (
        echo Copying statw.txt from parent directory...
        copy "..\statw.txt" "statw.txt" >nul
    ) else (
        echo WARNING: statw.txt not found. COVID data may not work.
    )
) else (
    echo statw.txt found.
)

echo.
echo [3/3] Installation complete!
echo.
echo To run the application, use:
echo   python main.py
echo.
echo Or double-click run_app.bat
echo.
pause


