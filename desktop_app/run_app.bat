@echo off
echo Starting Aditya Setu Desktop Application...
echo.
python main.py
if errorlevel 1 (
    echo.
    echo ERROR: Failed to start application
    echo Please make sure Python is installed and dependencies are installed.
    echo Run install.bat to install dependencies.
    echo.
    pause
)


