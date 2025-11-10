#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Criar instâncias das extensões
db = SQLAlchemy()
migrate = Migrate()

# Criar a aplicação Flask
app = Flask(__name__)

# Configurações
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuração do banco de dados
database_url = os.environ.get('DATABASE_URL', '')

# Railway usa postgres://, mas SQLAlchemy precisa postgresql://
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
    print(f"✅ DATABASE_URL configurada (PostgreSQL)")
elif database_url:
    print(f"✅ DATABASE_URL configurada")
else:
    # Fallback para SQLite em desenvolvimento
    database_url = 'sqlite:///crm.db'
    print("⚠️ Usando SQLite (desenvolvimento)")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões com app
db.init_app(app)
migrate.init_app(app, db)

# Importar models (DEPOIS de criar db)
from app import models

# Importar e registrar blueprint (DEPOIS de criar app)
from app.controllers import main_bp
app.register_blueprint(main_bp)

print("✅ App Flask inicializado com sucesso!")