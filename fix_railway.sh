#!/bin/bash

# Script de Correção Automática - CRM Railway
# Execute na raiz do projeto: bash fix_railway.sh

echo "========================================"
echo "🔧 CORRIGINDO CONFIGURAÇÃO RAILWAY"
echo "========================================"

# Verificar se está no diretório correto
if [ ! -f "requirements.txt" ]; then
    echo "❌ Erro: Execute este script na raiz do projeto (onde está o requirements.txt)"
    exit 1
fi

echo ""
echo "1. Atualizando requirements.txt..."
cat > requirements.txt << 'EOF'
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
WTForms==3.1.1
email-validator==2.1.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
phonenumbers==8.13.27
Werkzeug==3.0.1
gunicorn==21.2.0
EOF
echo "   ✅ requirements.txt atualizado"

echo ""
echo "2. Verificando/Criando Procfile..."
cat > Procfile << 'EOF'
web: python run.py
EOF
echo "   ✅ Procfile criado"

echo ""
echo "3. Verificando/Criando railway.json..."
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r requirements.txt"
  },
  "deploy": {
    "startCommand": "python run.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
EOF
echo "   ✅ railway.json criado"

echo ""
echo "4. Atualizando app/__init__.py..."
cat > app/__init__.py << 'EOF'
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
EOF
echo "   ✅ app/__init__.py atualizado"

echo ""
echo "5. Atualizando run.py..."
cat > run.py << 'EOF'
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app, db
    print("✅ Módulo app importado com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao importar módulo app: {e}")
    sys.exit(1)

if __name__ == '__main__':
    # Obter porta do ambiente (Railway define PORT automaticamente)
    port = int(os.environ.get('PORT', 8080))
    
    print(f"\n{'='*50}")
    print(f"🚀 INICIANDO CRM")
    print(f"{'='*50}")
    print(f"Porta: {port}")
    print(f"Ambiente: {os.environ.get('FLASK_ENV', 'development')}")
    print(f"DATABASE_URL configurada: {'Sim' if os.environ.get('DATABASE_URL') else 'Não'}")
    print(f"{'='*50}\n")
    
    # Criar tabelas se não existirem
    with app.app_context():
        try:
            db.create_all()
            print("✅ Banco de dados inicializado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            # Não sair aqui, deixar o app tentar rodar mesmo assim
    
    # Iniciar aplicação
    print(f"🚀 Iniciando aplicação na porta {port}...")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False  # NUNCA use debug=True em produção
    )
EOF
chmod +x run.py
echo "   ✅ run.py atualizado e tornado executável"

echo ""
echo "========================================"
echo "✅ CORREÇÕES APLICADAS COM SUCESSO!"
echo "========================================"
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo ""
echo "1. Fazer commit das mudanças:"
echo "   git add ."
echo "   git commit -m 'Corrigir configuração DATABASE_URL para Railway'"
echo "   git push origin main"
echo ""
echo "2. No Railway, configure as variáveis:"
echo "   • DATABASE_URL=\${{Postgres.DATABASE_URL}}"
echo "   • SECRET_KEY=sua-chave-secreta"
echo "   • FLASK_ENV=production"
echo ""
echo "3. Aguarde o deploy e verifique os logs"
echo ""
echo "========================================"