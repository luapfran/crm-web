import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# Inicializar extensões
db = SQLAlchemy()
csrf = CSRFProtect()

def create_app():
    """Factory function para criar a aplicação"""
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database config - ISSO É CRUCIAL!
    database_url = os.environ.get('DATABASE_URL', '')
    
    # Verificar se DATABASE_URL existe
    if not database_url:
        print("⚠️ DATABASE_URL não encontrada! Usando SQLite (desenvolvimento)")
        database_url = 'sqlite:///crm.db'
    else:
        print(f"✅ DATABASE_URL encontrada: {database_url[:30]}...")
        # Railway/Heroku usam postgres://, mas SQLAlchemy precisa postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
            print("✅ URL convertida para postgresql://")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True
    
    # Inicializar extensões com app
    db.init_app(app)
    csrf.init_app(app)
    
    # Registrar blueprints
    try:
        from app.controllers import main_bp
        app.register_blueprint(main_bp)
        print("✅ Blueprint registrado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao registrar blueprint: {e}")
        sys.exit(1)
    
    return app

# Para compatibilidade com imports antigos
app = create_app()
