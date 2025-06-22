"""
ARBOSOCIAL - Sistema Integrado de Análise e Predição de Arboviroses
Aplicação principal Flask
"""

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta

# Inicialização das extensões
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='development'):
    """Factory function para criar a aplicação Flask"""
    
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:password@localhost/arbosocial'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    # Inicialização das extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Registro dos blueprints
    from app.routes.auth import auth_bp
    from app.routes.data import data_bp
    from app.routes.predictions import predictions_bp
    from app.routes.alerts import alerts_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(data_bp, url_prefix='/api/data')
    app.register_blueprint(predictions_bp, url_prefix='/api/predictions')
    app.register_blueprint(alerts_bp, url_prefix='/api/alerts')
    
    # Rota de health check
    @app.route('/api/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'ARBOSOCIAL API',
            'version': '1.0.0'
        })
    
    # Rota raiz
    @app.route('/')
    def index():
        return jsonify({
            'message': 'ARBOSOCIAL - Sistema Integrado de Análise e Predição de Arboviroses',
            'version': '1.0.0',
            'author': 'Kelly Christine Alvarenga de Castro',
            'institution': 'UNINTER',
            'api_docs': '/api/docs'
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

