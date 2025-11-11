# Quick Start Guide

## Installation Steps

### Windows

1. **Double-click `install.bat`** - This will install all dependencies automatically
   - If you get an error, make sure Python 3.7+ is installed from [python.org](https://www.python.org/)

2. **Run the application**:
   - Double-click `run_app.bat`, OR
   - Open Command Prompt in this folder and run: `python main.py`

### Linux/Mac

1. **Open Terminal** in the `desktop_app` folder

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## First Time Setup

1. **Launch the application** - You'll see the login screen

2. **Create an account**:
   - Click "Register here"
   - Fill in your details (name, email, mobile, password are required)
   - State is optional but recommended for COVID statistics

3. **Login** with your new account

4. **Take your first assessment**:
   - Click "Take New Assessment" from the dashboard
   - Answer all 12 questions honestly
   - Click "Submit Assessment"
   - View your risk level and recommendations

## Features Overview

### Dashboard
- View your profile information
- See COVID cases for your state (if state is set)
- View your latest assessment results
- Check assessment history
- View active health alerts

### Health Assessment
- 12 comprehensive questions covering:
  - Symptoms (fever, cough, breathing issues, etc.)
  - Exposure history
  - Travel history
  - Medical conditions
  - Protective measures (vaccination, mask usage)

### Results
- Risk Level: Low / Moderate / High
- Risk Score: Numerical score (0-2 = Low, 3-5 = Moderate, 6+ = High)
- Personalized Recommendations based on your responses

## Default Admin Account

- **Email**: admin@adityasetu.com
- **Password**: admin123

⚠️ **Security Note**: Change this password in production environments!

## Troubleshooting

### "Python not found" error
- Install Python 3.7+ from [python.org](https://www.python.org/)
- Make sure to check "Add Python to PATH" during installation

### "Module not found" errors
- Run `pip install -r requirements.txt` again
- Make sure you're in the `desktop_app` directory

### COVID data not showing
- Ensure `statw.txt` file exists in the desktop_app folder
- The state name must match exactly (case-insensitive) with the states in statw.txt

### Database errors
- The database is stored in:
  - Windows: `%APPDATA%\AdityaSetu\aditya_setu.db`
  - Linux/Mac: `~/.adityasetu/aditya_setu.db`
- Delete the database file and restart the app to reset

## Building a Windows Executable

To create a standalone .exe file that doesn't require Python:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "AdityaSetu" main.py
```

The executable will be in the `dist/` folder.

## Support

For issues or questions, refer to the main README.md file or contact the development team.


