"""
Modelos de dados para o sistema ARBOSOCIAL
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from geoalchemy2 import Geometry

db = SQLAlchemy()

class User(db.Model):
    """Modelo para usuários do sistema"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(200))
    role = db.Column(db.String(50), default='user')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'institution': self.institution,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Municipality(db.Model):
    """Modelo para municípios brasileiros"""
    __tablename__ = 'municipalities'
    
    id = db.Column(db.Integer, primary_key=True)
    ibge_code = db.Column(db.String(7), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    region = db.Column(db.String(20), nullable=False)
    population = db.Column(db.Integer)
    area_km2 = db.Column(db.Float)
    geometry = db.Column(Geometry('POLYGON'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    cases = db.relationship('ArbovirusCase', backref='municipality', lazy=True)
    social_indicators = db.relationship('SocialIndicator', backref='municipality', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'ibge_code': self.ibge_code,
            'name': self.name,
            'state': self.state,
            'region': self.region,
            'population': self.population,
            'area_km2': self.area_km2
        }

class ArbovirusCase(db.Model):
    """Modelo para casos de arboviroses"""
    __tablename__ = 'arbovirus_cases'
    
    id = db.Column(db.Integer, primary_key=True)
    municipality_id = db.Column(db.Integer, db.ForeignKey('municipalities.id'), nullable=False)
    disease = db.Column(db.String(20), nullable=False)  # dengue, zika, chikungunya
    epidemiological_week = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    confirmed_cases = db.Column(db.Integer, default=0)
    probable_cases = db.Column(db.Integer, default=0)
    deaths = db.Column(db.Integer, default=0)
    incidence_rate = db.Column(db.Float)
    notification_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'municipality_id': self.municipality_id,
            'disease': self.disease,
            'epidemiological_week': self.epidemiological_week,
            'year': self.year,
            'confirmed_cases': self.confirmed_cases,
            'probable_cases': self.probable_cases,
            'deaths': self.deaths,
            'incidence_rate': self.incidence_rate,
            'notification_date': self.notification_date.isoformat() if self.notification_date else None
        }

class SocialIndicator(db.Model):
    """Modelo para indicadores sociais"""
    __tablename__ = 'social_indicators'
    
    id = db.Column(db.Integer, primary_key=True)
    municipality_id = db.Column(db.Integer, db.ForeignKey('municipalities.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    
    # Indicadores demográficos
    population_density = db.Column(db.Float)
    urban_population_pct = db.Column(db.Float)
    
    # Indicadores socioeconômicos
    gdp_per_capita = db.Column(db.Float)
    gini_index = db.Column(db.Float)
    poverty_rate = db.Column(db.Float)
    unemployment_rate = db.Column(db.Float)
    
    # Indicadores de educação
    literacy_rate = db.Column(db.Float)
    education_index = db.Column(db.Float)
    
    # Indicadores de saúde
    infant_mortality_rate = db.Column(db.Float)
    life_expectancy = db.Column(db.Float)
    health_coverage_pct = db.Column(db.Float)
    
    # Indicadores de infraestrutura
    water_supply_pct = db.Column(db.Float)
    sewage_treatment_pct = db.Column(db.Float)
    garbage_collection_pct = db.Column(db.Float)
    electricity_access_pct = db.Column(db.Float)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'municipality_id': self.municipality_id,
            'year': self.year,
            'population_density': self.population_density,
            'urban_population_pct': self.urban_population_pct,
            'gdp_per_capita': self.gdp_per_capita,
            'gini_index': self.gini_index,
            'poverty_rate': self.poverty_rate,
            'unemployment_rate': self.unemployment_rate,
            'literacy_rate': self.literacy_rate,
            'education_index': self.education_index,
            'infant_mortality_rate': self.infant_mortality_rate,
            'life_expectancy': self.life_expectancy,
            'health_coverage_pct': self.health_coverage_pct,
            'water_supply_pct': self.water_supply_pct,
            'sewage_treatment_pct': self.sewage_treatment_pct,
            'garbage_collection_pct': self.garbage_collection_pct,
            'electricity_access_pct': self.electricity_access_pct
        }

class Prediction(db.Model):
    """Modelo para predições de casos"""
    __tablename__ = 'predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    municipality_id = db.Column(db.Integer, db.ForeignKey('municipalities.id'), nullable=False)
    disease = db.Column(db.String(20), nullable=False)
    model_name = db.Column(db.String(50), nullable=False)  # arima, lstm, prophet, ensemble
    prediction_date = db.Column(db.Date, nullable=False)
    target_week = db.Column(db.Integer, nullable=False)
    target_year = db.Column(db.Integer, nullable=False)
    predicted_cases = db.Column(db.Float, nullable=False)
    confidence_interval_lower = db.Column(db.Float)
    confidence_interval_upper = db.Column(db.Float)
    model_accuracy = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'municipality_id': self.municipality_id,
            'disease': self.disease,
            'model_name': self.model_name,
            'prediction_date': self.prediction_date.isoformat(),
            'target_week': self.target_week,
            'target_year': self.target_year,
            'predicted_cases': self.predicted_cases,
            'confidence_interval_lower': self.confidence_interval_lower,
            'confidence_interval_upper': self.confidence_interval_upper,
            'model_accuracy': self.model_accuracy
        }

class Alert(db.Model):
    """Modelo para alertas do sistema"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    municipality_id = db.Column(db.Integer, db.ForeignKey('municipalities.id'), nullable=False)
    disease = db.Column(db.String(20), nullable=False)
    alert_level = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    alert_type = db.Column(db.String(50), nullable=False)  # outbreak_prediction, threshold_exceeded
    message = db.Column(db.Text)
    predicted_cases = db.Column(db.Float)
    confidence_score = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'municipality_id': self.municipality_id,
            'disease': self.disease,
            'alert_level': self.alert_level,
            'alert_type': self.alert_type,
            'message': self.message,
            'predicted_cases': self.predicted_cases,
            'confidence_score': self.confidence_score,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None
        }

