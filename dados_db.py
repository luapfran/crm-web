#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script DEFINITIVO para popular o banco de dados
Usa ORM ao invés de SQL bruto
Execute: python dados_db.py
"""

import os
import sys
from datetime import datetime

# CRÍTICO: Adicionar path ANTES de importar app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("="*70)
print("🗃️  INICIANDO POPULAÇÃO DO BANCO DE DADOS")
print("="*70)

# Importar app e db
print("\n1️⃣ Importando aplicação...")
from app import app, db

# CRÍTICO: Importar models EXPLICITAMENTE
print("2️⃣ Importando models...")
from app.models import Cliente, Cotacao, Pedido

print("✅ Imports realizados com sucesso!")

def criar_tabelas_force():
    """Força a criação das tabelas usando SQLAlchemy"""
    print("\n3️⃣ Criando estrutura do banco de dados...")
    
    try:
        # Método 1: drop_all + create_all (mais confiável)
        print("   Dropando tabelas antigas (se existirem)...")
        db.drop_all()
        print("   Criando novas tabelas...")
        db.create_all()
        
        # Verificar se foram criadas
        inspector = db.inspect(db.engine)
        tabelas = inspector.get_table_names()
        
        print(f"   Tabelas criadas: {', '.join(tabelas)}")
        
        if 'cliente' not in tabelas:
            print("   ❌ ERRO: Tabela 'cliente' não foi criada!")
            return False
        
        print("✅ Estrutura do banco criada com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        import traceback
        traceback.print_exc()
        return False

def popular_clientes():
    """Popula clientes usando ORM"""
    print("\n4️⃣ Criando clientes...")
    
    clientes_data = [
        {
            'nome': 'Tech Solutions Ltda',
            'telefone': '(11) 98765-4321',
            'email': 'contato@techsolutions.com.br',
            'empresa': 'Tech Solutions',
            'segmento': 'Tecnologia da Informação',
            'observacoes': 'Limite: R$ 15.000 - Indústria - Av. Paulista, São Paulo - SP'
        },
        {
            'nome': 'Supermercado Bom Preço',
            'telefone': '(21) 97654-3210',
            'email': 'compras@bompreco.com.br',
            'empresa': 'Bom Preço',
            'segmento': 'Varejo Alimentício',
            'observacoes': 'Limite: R$ 25.000 - Revenda - Rio de Janeiro - RJ'
        },
        {
            'nome': 'Construtora Alicerce S/A',
            'telefone': '(85) 96543-2109',
            'email': 'obras@alicerce.com.br',
            'empresa': 'Alicerce',
            'segmento': 'Construção Civil',
            'observacoes': 'Limite: R$ 50.000 - Indústria - Fortaleza - CE'
        },
        {
            'nome': 'Clínica Saúde Total',
            'telefone': '(11) 95432-1098',
            'email': 'administrativo@saudetotal.com.br',
            'empresa': 'Saúde Total',
            'segmento': 'Saúde',
            'observacoes': 'Limite: R$ 10.000 - Consumidor - São Paulo - SP'
        },
        {
            'nome': 'Escola Futuro Brilhante',
            'telefone': '(81) 94321-0987',
            'email': 'diretoria@futurobrilhante.edu.br',
            'empresa': 'Futuro Brilhante',
            'segmento': 'Educação',
            'observacoes': 'Limite: R$ 8.000 - Consumidor - Recife - PE'
        },
        {
            'nome': 'Restaurante Sabor & Arte',
            'telefone': '(11) 93210-9876',
            'email': 'gerencia@saborarte.com.br',
            'empresa': 'Sabor & Arte',
            'segmento': 'Alimentação',
            'observacoes': 'Limite: R$ 12.000 - Revenda - São Paulo - SP'
        },
        {
            'nome': 'Indústria Metal Forte',
            'telefone': '(48) 92109-8765',
            'email': 'suprimentos@metalforte.ind.br',
            'empresa': 'Metal Forte',
            'segmento': 'Indústria Metalúrgica',
            'observacoes': 'Limite: R$ 80.000 - Indústria - Joinville - SC'
        },
        {
            'nome': 'Farmácia Popular',
            'telefone': '(21) 91098-7654',
            'email': 'comercial@farmaciapopular.com.br',
            'empresa': 'Farmácia Popular',
            'segmento': 'Farmacêutico',
            'observacoes': 'Limite: R$ 18.000 - Revenda - Rio de Janeiro - RJ'
        },
        {
            'nome': 'Academia Corpo e Mente',
            'telefone': '(85) 90987-6543',
            'email': 'recepcao@corpoeamente.com.br',
            'empresa': 'Corpo e Mente',
            'segmento': 'Fitness e Bem-estar',
            'observacoes': 'Limite: R$ 6.000 - Consumidor - Fortaleza - CE'
        },
        {
            'nome': 'Escritório Advocacia & Cia',
            'telefone': '(11) 89876-5432',
            'email': 'contato@advocaciaecia.adv.br',
            'empresa': 'Advocacia & Cia',
            'segmento': 'Serviços Jurídicos',
            'observacoes': 'Limite: R$ 5.000 - Consumidor - São Paulo - SP'
        }
    ]
    
    try:
        clientes = []
        for data in clientes_data:
            cliente = Cliente(**data)
            db.session.add(cliente)
            clientes.append(cliente)
        
        db.session.commit()
        print(f"✅ {len(clientes)} clientes criados com sucesso!")
        return clientes
        
    except Exception as e:
        print(f"❌ Erro ao criar clientes: {e}")
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return []

def popular_cotacoes(clientes):
    """Popula cotações usando ORM"""
    print("\n5️⃣ Criando cotações...")
    
    if not clientes or len(clientes) < 10:
        print("❌ Clientes não foram criados. Pulando cotações.")
        return []
    
    cotacoes_data = [
        {
            'cliente_id': clientes[0].id,
            'produto': '5 Licenças Software + 10 Computadores + Servidor + Instalação + Treinamento (40h)',
            'valor': 45000.00,
            'status': 'Aprovada',
            'data_cotacao': datetime(2024, 1, 25),
            'observacoes': 'COT-001A - Pagamento em 3x sem juros. Garantia de 12 meses.'
        },
        {
            'cliente_id': clientes[1].id,
            'produto': '4 Checkouts + 2 Balanças + Sistema gestão + 3 Câmeras + Instalação',
            'valor': 32000.00,
            'status': 'Aprovada',
            'data_cotacao': datetime(2024, 2, 28),
            'observacoes': 'COT-002A - Frete incluso. Instalação em até 15 dias úteis.'
        },
        {
            'cliente_id': clientes[2].id,
            'produto': '500 sacos cimento + 200m³ areia + 150m³ brita + 50t ferro + Entrega parcelada',
            'valor': 85000.00,
            'status': 'Aprovada',
            'data_cotacao': datetime(2024, 3, 18),
            'observacoes': 'COT-003A - Entregas quinzenais. Pagamento 30 dias após cada entrega.'
        },
        {
            'cliente_id': clientes[3].id,
            'produto': '2 Macas elétricas + Autoclave 21L + 5 Cadeiras + Armário + Materiais consumo',
            'valor': 18500.00,
            'status': 'Em Análise',
            'data_cotacao': datetime(2024, 4, 15),
            'observacoes': 'COT-004E - Valores válidos por 30 dias. Frete grátis para SP.'
        },
        {
            'cliente_id': clientes[4].id,
            'produto': '30 Computadores + Projetor Full HD + 5 Impressoras + Software educacional + Instalação',
            'valor': 52000.00,
            'status': 'Aprovada',
            'data_cotacao': datetime(2024, 5, 20),
            'observacoes': 'COT-005A - Desconto especial educação. Garantia 24 meses.'
        },
        {
            'cliente_id': clientes[5].id,
            'produto': 'Forno industrial + Fogão 6 bocas + 2 Fritadeiras + Refrigerador 4 portas + Instalação',
            'valor': 28000.00,
            'status': 'Rejeitada',
            'data_cotacao': datetime(2024, 6, 22),
            'observacoes': 'COT-006R - Cliente optou por fornecedor concorrente.'
        },
        {
            'cliente_id': clientes[6].id,
            'produto': 'Contrato anual: 100t aço carbono/mês + 50t alumínio/mês + Entrega programada',
            'valor': 850000.00,
            'status': 'Aprovada',
            'data_cotacao': datetime(2024, 8, 1),
            'observacoes': 'COT-007A - Contrato 12 meses renováveis. Reajuste semestral IPCA.'
        },
        {
            'cliente_id': clientes[7].id,
            'produto': 'Fornecimento mensal medicamentos + Higiene/beleza + Suplementos + Equipamentos',
            'valor': 22000.00,
            'status': 'Aprovada',
            'data_cotacao': datetime(2024, 8, 25),
            'observacoes': 'COT-008A - Fornecimento mensal renovável. Primeira entrega em 10 dias.'
        },
        {
            'cliente_id': clientes[8].id,
            'produto': '10 Esteiras + 5 Bicicletas + Kit pesos + 3 Aparelhos musculação + Manutenção 6 meses',
            'valor': 42000.00,
            'status': 'Em Análise',
            'data_cotacao': datetime(2024, 9, 20),
            'observacoes': 'COT-009E - Parcelamento em até 10x. Garantia 18 meses.'
        },
        {
            'cliente_id': clientes[9].id,
            'produto': '8 Mesas executivas + 8 Cadeiras + 5 Armários + 5 Computadores + 2 Impressoras + Rede',
            'valor': 28500.00,
            'status': 'Aprovada',
            'data_cotacao': datetime(2024, 10, 5),
            'observacoes': 'COT-010A - Montagem incluída. Entrega em 20 dias úteis.'
        },
        {
            'cliente_id': clientes[0].id,
            'produto': 'Upgrade Enterprise + 5 Licenças adicionais + BI + Consultoria (80h)',
            'valor': 28000.00,
            'status': 'Em Análise',
            'data_cotacao': datetime(2025, 10, 1),
            'observacoes': 'COT-011E - Proposta de expansão do sistema atual.'
        }
    ]
    
    try:
        cotacoes = []
        for data in cotacoes_data:
            cotacao = Cotacao(**data)
            db.session.add(cotacao)
            cotacoes.append(cotacao)
        
        db.session.commit()
        print(f"✅ {len(cotacoes)} cotações criadas com sucesso!")
        return cotacoes
        
    except Exception as e:
        print(f"❌ Erro ao criar cotações: {e}")
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return []

def popular_pedidos(clientes):
    """Popula pedidos usando ORM"""
    print("\n6️⃣ Criando pedidos...")
    
    if not clientes or len(clientes) < 10:
        print("❌ Clientes não foram criados. Pulando pedidos.")
        return []
    
    pedidos_data = [
        {
            'cliente_id': clientes[0].id,
            'produto': '5 Licenças Software + 10 Computadores + Servidor + Instalação + Treinamento',
            'quantidade': 1,
            'valor_total': 45000.00,
            'status': 'Concluído',
            'data_pedido': datetime(2024, 2, 1),
            'observacoes': 'PED-001 - Cliente muito satisfeito. Entregue em 22/02/2024.'
        },
        {
            'cliente_id': clientes[1].id,
            'produto': '4 Checkouts + 2 Balanças + Sistema + 3 Câmeras + Instalação',
            'quantidade': 1,
            'valor_total': 32000.00,
            'status': 'Concluído',
            'data_pedido': datetime(2024, 3, 5),
            'observacoes': 'PED-002 - Instalação fora do horário comercial. Entregue 20/03/2024.'
        },
        {
            'cliente_id': clientes[2].id,
            'produto': 'Primeira entrega: 100 sacos cimento + 40m³ areia + 30m³ brita + 10t ferro',
            'quantidade': 1,
            'valor_total': 17000.00,
            'status': 'Concluído',
            'data_pedido': datetime(2024, 3, 25),
            'observacoes': 'PED-003A - Primeira de cinco entregas. Entregue 03/04/2024.'
        },
        {
            'cliente_id': clientes[2].id,
            'produto': 'Segunda entrega: 100 sacos cimento + 40m³ areia + 30m³ brita + 10t ferro',
            'quantidade': 1,
            'valor_total': 17000.00,
            'status': 'Em Processamento',
            'data_pedido': datetime(2024, 4, 10),
            'observacoes': 'PED-003B - Previsão de entrega: 20/04/2024.'
        },
        {
            'cliente_id': clientes[4].id,
            'produto': '30 Computadores + Projetor + 5 Impressoras + Software + Instalação',
            'quantidade': 1,
            'valor_total': 52000.00,
            'status': 'Em Processamento',
            'data_pedido': datetime(2024, 6, 25),
            'observacoes': 'PED-005 - Aguardando logística. Previsão: 20/07/2024.'
        },
        {
            'cliente_id': clientes[6].id,
            'produto': 'Fornecimento Agosto/2024: 100t aço carbono + 50t alumínio',
            'quantidade': 1,
            'valor_total': 70000.00,
            'status': 'Concluído',
            'data_pedido': datetime(2024, 8, 5),
            'observacoes': 'PED-007-08 - Entregue 28/08/2024. Qualidade mantida.'
        },
        {
            'cliente_id': clientes[6].id,
            'produto': 'Fornecimento Setembro/2024: 100t aço carbono + 50t alumínio',
            'quantidade': 1,
            'valor_total': 70000.00,
            'status': 'Concluído',
            'data_pedido': datetime(2024, 9, 5),
            'observacoes': 'PED-007-09 - Entregue 29/09/2024. Doc fiscal enviada.'
        },
        {
            'cliente_id': clientes[6].id,
            'produto': 'Fornecimento Outubro/2024: 100t aço carbono + 50t alumínio',
            'quantidade': 1,
            'valor_total': 70000.00,
            'status': 'Em Processamento',
            'data_pedido': datetime(2024, 10, 5),
            'observacoes': 'PED-007-10 - Carga despachada. Previsão: 30/10/2024.'
        },
        {
            'cliente_id': clientes[7].id,
            'produto': 'Fornecimento Set/2024: Medicamentos + Higiene + Suplementos + Equipamentos',
            'quantidade': 1,
            'valor_total': 22000.00,
            'status': 'Concluído',
            'data_pedido': datetime(2024, 9, 1),
            'observacoes': 'PED-008-09 - Primeira entrega contrato. Entregue 08/09/2024.'
        },
        {
            'cliente_id': clientes[7].id,
            'produto': 'Fornecimento Out/2024: Medicamentos + Higiene + Suplementos',
            'quantidade': 1,
            'valor_total': 22000.00,
            'status': 'Pendente',
            'data_pedido': datetime(2024, 10, 1),
            'observacoes': 'PED-008-10 - Separação em andamento. Previsão: 10/10/2024.'
        },
        {
            'cliente_id': clientes[9].id,
            'produto': '8 Mesas + 8 Cadeiras + 5 Armários + 5 PCs + 2 Impressoras + Rede',
            'quantidade': 1,
            'valor_total': 28500.00,
            'status': 'Em Processamento',
            'data_pedido': datetime(2024, 10, 8),
            'observacoes': 'PED-010 - Móveis em produção. Instalação: 28/10/2024.'
        }
    ]
    
    try:
        pedidos = []
        for data in pedidos_data:
            pedido = Pedido(**data)
            db.session.add(pedido)
            pedidos.append(pedido)
        
        db.session.commit()
        print(f"✅ {len(pedidos)} pedidos criados com sucesso!")
        return pedidos
        
    except Exception as e:
        print(f"❌ Erro ao criar pedidos: {e}")
        db.session.rollback()
        import traceback
        traceback.print_exc()
        return []

def main():
    """Função principal"""
    
    with app.app_context():
        try:
            # Passo 1: Criar estrutura
            if not criar_tabelas_force():
                print("\n❌ Falha ao criar estrutura do banco. Abortando...")
                sys.exit(1)
            
            # Passo 2: Popular dados
            clientes = popular_clientes()
            if not clientes:
                print("\n❌ Falha ao criar clientes. Abortando...")
                sys.exit(1)
            
            cotacoes = popular_cotacoes(clientes)
            pedidos = popular_pedidos(clientes)
            
            # Resumo final
            print("\n" + "="*70)
            print("✅ BANCO POPULADO COM SUCESSO!")
            print("="*70)
            print(f"\n📊 Resumo:")
            print(f"   • {len(clientes)} clientes")
            print(f"   • {len(cotacoes)} cotações")
            print(f"   • {len(pedidos)} pedidos")
            print(f"\n💡 Acesse: https://crm-web-production-0848.up.railway.app/")
            print()
            
        except Exception as e:
            print(f"\n❌ Erro fatal: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    main()