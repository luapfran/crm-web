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
