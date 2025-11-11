"""Utility functions for desktop application"""
from .covid_data import load_covid_data
from .risk_calculator import calculate_risk_score, generate_recommendations
from .questions import get_assessment_questions

__all__ = ['load_covid_data', 'calculate_risk_score', 'generate_recommendations', 'get_assessment_questions']


