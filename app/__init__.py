from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.controllers import main_bp
    app.register_blueprint(main_bp)
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Cliente': Cliente,
            'Interacao': Interacao,
            'Cotacao': Cotacao,
            'Pedido': Pedido
        }
    
    from app import models
    return app

from app.models import Cliente, Interacao, Cotacao, Pedido
