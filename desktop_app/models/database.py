"""
Database models using SQLAlchemy for desktop application
"""
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, Text, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import bcrypt

Base = declarative_base()

# Database setup - store in user's AppData or local directory
if os.name == 'nt':  # Windows
    app_data = os.path.join(os.getenv('APPDATA', '.'), 'AdityaSetu')
    os.makedirs(app_data, exist_ok=True)
    db_path = os.path.join(app_data, 'aditya_setu.db')
else:
    db_path = os.path.join(os.path.expanduser('~'), '.adityasetu', 'aditya_setu.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

DATABASE_URL = f'sqlite:///{db_path}'
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)


class User(Base):
    """User model for registration and authentication"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    mobile = Column(String(20), nullable=False)
    password_hash = Column(String(255), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(20), nullable=True)
    location = Column(String(200), nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    assessments = relationship('Assessment', backref='user', lazy=True, cascade='all, delete-orphan')
    alerts_created = relationship('Alert', backref='creator')
    
    def set_password(self, password):
        """Hash and set password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        except:
            return False
    
    def __repr__(self):
        return f'<User {self.email}>'


class Assessment(Base):
    """Self-assessment report model"""
    __tablename__ = 'assessments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    answers = Column(JSON, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)  # Low, Moderate, High
    recommendations = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<Assessment {self.id} - {self.risk_level}>'


class Alert(Base):
    """Alert/announcement model"""
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    target_location = Column(String(200), nullable=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<Alert {self.title}>'


def init_database():
    """Initialize database and create tables"""
    Base.metadata.create_all(engine)
    
    # Create default admin user if it doesn't exist
    session = SessionLocal()
    try:
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@adityasetu.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        existing_admin = session.query(User).filter_by(email=admin_email).first()
        if not existing_admin:
            admin = User(
                name='Admin User',
                email=admin_email,
                mobile='0000000000',
                is_admin=True
            )
            admin.set_password(admin_password)
            session.add(admin)
            session.commit()
            print(f"Created default admin user: {admin_email} / {admin_password}")
    except Exception as e:
        session.rollback()
        print(f"Error initializing database: {e}")
    finally:
        session.close()


def get_db():
    """Get database session"""
    return SessionLocal()


