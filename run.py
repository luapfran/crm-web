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
