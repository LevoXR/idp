# Aditya Setu Desktop Application

A fully Python-based desktop application for health assessment and COVID-19 risk evaluation. This is the desktop version of the Aditya Setu web application, built using tkinter for the GUI.

## Features

- **User Registration & Authentication**: Secure user registration and login with password hashing
- **Health Assessment**: Comprehensive 12-question health questionnaire
- **Risk Calculation**: Automated risk scoring (Low/Moderate/High) based on symptoms and exposure
- **COVID-19 Statistics**: Display of COVID cases by state (from statw.txt)
- **Assessment History**: View past assessments and results
- **Personalized Recommendations**: Tailored health recommendations based on risk level
- **Alerts System**: View active health alerts and announcements

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Install Dependencies

```bash
cd desktop_app
pip install -r requirements.txt
```

### Step 2: Copy COVID Data File

Copy the `statw.txt` file from the parent directory to the desktop_app directory:

```bash
# On Windows (PowerShell)
Copy-Item ..\statw.txt .\statw.txt

# On Linux/Mac
cp ../statw.txt ./statw.txt
```

### Step 3: Run the Application

```bash
python main.py
```

## Building Windows Installer

To create a Windows installer (.exe), you can use PyInstaller:

```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed --name "AdityaSetu" --icon=icon.ico main.py

# The executable will be in the dist/ folder
```

## Application Structure

```
desktop_app/
├── main.py              # Application entry point
├── models/              # Database models
│   ├── __init__.py
│   └── database.py      # SQLAlchemy models and database setup
├── gui/                 # GUI components
│   ├── __init__.py
│   ├── main_window.py   # Main window controller
│   ├── login_frame.py   # Login screen
│   ├── register_frame.py # Registration screen
│   ├── dashboard_frame.py # User dashboard
│   ├── assessment_frame.py # Health assessment form
│   └── result_frame.py  # Assessment results screen
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── covid_data.py    # COVID data loader
│   ├── risk_calculator.py # Risk scoring logic
│   └── questions.py     # Assessment questions
├── requirements.txt     # Python dependencies
├── setup.py            # Setup script for installation
└── README.md           # This file
```

## Database

The application uses SQLite database stored in:
- **Windows**: `%APPDATA%\AdityaSetu\aditya_setu.db`
- **Linux/Mac**: `~/.adityasetu/aditya_setu.db`

## Default Admin Credentials

- **Email**: admin@adityasetu.com
- **Password**: admin123

⚠️ **Important**: Change these credentials in production!

## Usage

1. **Launch the Application**: Run `python main.py`
2. **Register a New Account**: Click "Register here" on the login screen
3. **Login**: Use your email and password to login
4. **View Dashboard**: See your profile, latest assessment, and alerts
5. **Take Assessment**: Click "Take New Assessment" and answer all 12 questions
6. **View Results**: See your risk level and personalized recommendations

## Risk Scoring

- **Score 0-2**: Low Risk
- **Score 3-5**: Moderate Risk
- **Score 6+**: High Risk

## Development

### Running in Development Mode

```bash
# Install in development mode
pip install -e .

# Run the application
python main.py
```

### Adding New Features

1. Database models: Edit `models/database.py`
2. GUI components: Add new frames in `gui/`
3. Business logic: Add utilities in `utils/`

## Troubleshooting

### Database Errors
- Ensure you have write permissions in the AppData/user directory
- Delete the database file and restart to recreate it

### COVID Data Not Showing
- Ensure `statw.txt` exists in the desktop_app directory or parent directory
- Check file format matches the expected markdown table format

### Import Errors
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.7+)

## License

MIT License - See LICENSE file for details

## Support

For issues and questions, please contact the development team or create an issue in the repository.


