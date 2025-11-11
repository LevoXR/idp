# Aditya Setu

A simple Python-based public health self-assessment tool - a lightweight clone of Aarogya Setu focused on basic threat detection via user self-reporting.

## Features

- **User Registration & Authentication**: Simple email + password authentication
- **Health Self-Assessment**: Interactive questionnaire with 12 questions about symptoms and exposure
- **Risk Scoring**: Rule-based scoring engine that computes Low/Moderate/High risk levels
- **Personalized Recommendations**: Tailored health recommendations based on risk level
- **Assessment History**: Users can view their past assessments and track changes
- **Health Alerts**: Admin can create and manage public health alerts
- **Admin Dashboard**: Comprehensive dashboard with analytics and user management

## Technology Stack

- **Backend**: Python 3.10+ with built-in http.server
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML templates with Bootstrap 5
- **Authentication**: Session-based authentication
- **Security**: bcrypt for password hashing

## Project Structure

```
aditya_setu/
├── backend/
│   ├── server.py           # Main HTTP server
│   ├── models.py           # SQLAlchemy models (User, Assessment, Alert)
│   ├── templates/          # HTML templates
│   ├── requirements.txt    # Python dependencies
│   └── instance/           # Database storage
├── docker/
│   └── Dockerfile          # Docker configuration
├── run.py                  # Application entry point
└── README.md
```

## Installation

### Local Development

1. **Clone the repository** (or create the project structure)

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set environment variables** (optional):
   ```bash
   export SECRET_KEY=your-secret-key-here
   export ADMIN_EMAIL=admin@adityasetu.com
   export ADMIN_PASSWORD=your-admin-password
   export PORT=8000
   ```

5. **Run the application**:
   ```bash
   python run.py
   ```

   The application will be available at `http://localhost:8000`

6. **Default admin credentials**:
   - Email: `admin@adityasetu.com`
   - Password: `admin123`

   (Change these via environment variables in production!)

### Docker Deployment

1. **Build the Docker image**:
   ```bash
   docker build -t aditya-setu -f docker/Dockerfile .
   ```

2. **Run the container**:
   ```bash
   docker run -d -p 8000:8000 \
     -e SECRET_KEY=your-secret-key \
     -e ADMIN_EMAIL=admin@adityasetu.com \
     -e ADMIN_PASSWORD=your-password \
     -v $(pwd)/data:/app/data \
     --name aditya-setu \
     aditya-setu
   ```

## Usage

### User Flow

1. **Register**: Create an account with email, mobile, and password
2. **Login**: Access your dashboard
3. **Take Assessment**: Complete the health questionnaire
4. **View Results**: Get risk level and personalized recommendations
5. **Track History**: View past assessments in your dashboard
6. **Check Alerts**: Stay informed with official health alerts

### Admin Flow

1. **Login** as admin user
2. **View Dashboard**: See analytics and recent assessments
3. **Manage Alerts**: Create, edit, or deactivate health alerts
4. **Filter Assessments**: View assessments by risk level and time period

## API Endpoints

The application provides both web UI and REST API endpoints:

### Authentication
- `POST /api/register` - Register new user
- `POST /api/login` - User login
- `POST /api/logout` - User logout
- `GET /api/profile` - Get current user profile

### Assessments
- `GET /api/questions` - Get questionnaire questions
- `POST /api/assessments` - Submit assessment
- `GET /api/assessments` - Get user's assessment history

### Alerts
- `GET /api/alerts` - Get active alerts (public)
- `GET /api/alerts?location=<state>` - Filter alerts by location

### Admin API
- `GET /api/admin/assessments` - Get all assessments (admin only)
- `POST /api/admin/alerts` - Create alert (admin only)

All API endpoints return JSON. Web routes return HTML templates.

## Questionnaire & Scoring

The assessment includes 12 questions covering:
- Fever and temperature
- Respiratory symptoms (cough, shortness of breath)
- Other symptoms (fatigue, body aches, loss of taste/smell)
- Exposure history (contact with confirmed cases)
- Travel history
- Medical conditions
- Age and household factors

**Risk Scoring**:
- Score 0-2: **Low Risk**
- Score 3-5: **Moderate Risk**
- Score 6+: **High Risk**

## Database Schema

### User
- id, name, email, mobile, password_hash
- age, gender, location (optional)
- is_admin, created_at, updated_at

### Assessment
- id, user_id, answers (JSON)
- risk_score, risk_level
- recommendations, created_at

### Alert
- id, title, message
- target_location (optional)
- created_by, is_active, created_at

## Security Considerations

- Passwords are hashed using bcrypt
- SQL injection protection via SQLAlchemy ORM
- Session-based authentication
- Admin routes protected with decorator

**For Production**:
- Change default SECRET_KEY
- Use PostgreSQL instead of SQLite
- Enable HTTPS
- Set secure cookie flags
- Implement rate limiting
- Add input validation and sanitization
- Regular security updates

## Configuration

Environment variables:
- `SECRET_KEY`: Secret key for session management
- `DATABASE_URL`: Database connection string (default: `sqlite:///aditya_setu.db`)
- `ADMIN_EMAIL`: Default admin email
- `ADMIN_PASSWORD`: Default admin password
- `PORT`: Server port (default: 8000)

## Development

### Running Tests
(Test suite can be added later)

### Code Structure
- **server.py**: Main HTTP server handling all routes and requests
- **models.py**: Database models using SQLAlchemy
- **run.py**: Application entry point and initialization

## License

This project is for educational/demonstration purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues or questions, please open an issue on the repository.

---

**Note**: This is an MVP implementation. For production use, additional security measures, testing, and optimizations should be implemented.

