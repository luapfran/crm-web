#!/bin/bash
# Script para criar todos os arquivos necessários
# Execute na raiz do projeto: bash setup_railway.sh

echo "Criando arquivos para Railway..."

# 1. Procfile
cat > Procfile << 'EOF'
web: python run.py
EOF
echo "✓ Procfile criado"

# 2. railway.json
cat > railway.json << 'EOF'
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python run.py",
    "restartPolicyType": "ON_FAILURE"
  }
}
EOF
echo "✓ railway.json criado"

# 3. runtime.txt
cat > runtime.txt << 'EOF'
python-3.11.x
EOF
echo "✓ runtime.txt criado"

# 4. Atualizar requirements.txt
cat > requirements.txt << 'EOF'
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.1
WTForms==3.1.1
email-validator==2.1.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
phonenumbers==8.13.27
EOF
echo "✓ requirements.txt atualizado"

# 5. Criar/Atualizar run.py
cat > run.py << 'EOF'
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app import app, db

if __name__ == '__main__':
    # Configurar porta
    port = int(os.environ.get('PORT', 5000))
    
    # Criar tabelas no banco
    with app.app_context():
        try:
            db.create_all()
            print("✅ Banco de dados inicializado com sucesso!")
        except Exception as e:
            print(f"⚠️ Erro ao criar tabelas: {e}")
    
    # Rodar aplicação
    print(f"🚀 Iniciando aplicação na porta {port}...")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
EOF
echo "✓ run.py atualizado"

echo ""
echo "✅ Todos os arquivos criados!"
echo ""
echo "Agora faça:"
echo "1. git add ."
echo "2. git commit -m 'Configurar para Railway'"
echo "3. git push origin main"