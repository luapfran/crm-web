#!/bin/bash

echo "🚀 Setup do Sistema CRM"
echo ""

# Verifica Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não instalado!"
    exit 1
fi

echo "✅ Docker OK"

# Cria .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Arquivo .env criado"
fi

# Cria diretórios
mkdir -p logs backups migrations
echo "✅ Diretórios criados"

# Inicia containers
echo "🐳 Iniciando containers..."
docker-compose up -d

echo "⏳ Aguardando banco inicializar..."
sleep 15

# Configura banco
echo "🗄️  Configurando banco..."
docker-compose exec -T web python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"

# Dados exemplo
docker-compose exec -T web flask seed-db

echo ""
echo "✅ Setup concluído!"
echo ""
echo "Acesse: http://localhost:5000"
echo "PgAdmin: http://localhost:5050"
