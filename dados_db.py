#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para popular o banco de dados com dados fictícios do arquivo SQL
Baseado em: dados_ficticios_crm.sql
Execute: python populate_db_from_sql.py
"""

import os
import sys
from datetime import datetime

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def limpar_banco():
    """Remove todos os dados existentes"""
    print("🗑️  Limpando banco de dados...")
    
    try:
        # Executar SQL diretamente para limpar com CASCADE
        db.session.execute(db.text('DELETE FROM pedido CASCADE'))
        db.session.execute(db.text('DELETE FROM cotacao CASCADE'))
        db.session.execute(db.text('DELETE FROM cliente CASCADE'))
        db.session.commit()
        print("✅ Banco limpo com sucesso!")
    except Exception as e:
        print(f"⚠️  Aviso ao limpar: {e}")
        db.session.rollback()

def criar_clientes():
    """Cria os 10 clientes do arquivo SQL"""
    print("\n👥 Criando clientes...")
    
    clientes_sql = """
INSERT INTO cliente (nome, telefone, email, limite_credito, area_atuacao, canal_vendas, endereco, data_cadastro, ultimo_contato, ativo) VALUES
('Tech Solutions Ltda', '(11) 98765-4321', 'contato@techsolutions.com.br', 15000.00, 'Tecnologia da Informação', 'Indústria', 'Av. Paulista, 1000 - Bela Vista, São Paulo - SP', '2024-01-15', '2025-10-05', true),
('Supermercado Bom Preço', '(21) 97654-3210', 'compras@bompreco.com.br', 25000.00, 'Varejo Alimentício', 'Revenda', 'Rua das Flores, 250 - Centro, Rio de Janeiro - RJ', '2024-02-20', '2025-10-08', true),
('Construtora Alicerce S/A', '(85) 96543-2109', 'obras@alicerce.com.br', 50000.00, 'Construção Civil', 'Indústria', 'Av. Beira Mar, 450 - Meireles, Fortaleza - CE', '2024-03-10', '2025-10-01', true),
('Clínica Saúde Total', '(11) 95432-1098', 'administrativo@saudetotal.com.br', 10000.00, 'Saúde', 'Consumidor', 'R. Dr. Almeida Lima, 120 - Pinheiros, São Paulo - SP', '2024-04-05', '2025-09-28', true),
('Escola Futuro Brilhante', '(81) 94321-0987', 'diretoria@futurobrilhante.edu.br', 8000.00, 'Educação', 'Consumidor', 'Av. Professor Morais, 300 - Boa Viagem, Recife - PE', '2024-05-12', '2025-10-10', true),
('Restaurante Sabor & Arte', '(11) 93210-9876', 'gerencia@saborarte.com.br', 12000.00, 'Alimentação', 'Revenda', 'R. do Mercado, 45 - Centro, São Paulo - SP', '2024-06-18', '2025-09-15', true),
('Indústria Metal Forte', '(48) 92109-8765', 'suprimentos@metalforte.ind.br', 80000.00, 'Indústria Metalúrgica', 'Indústria', 'Rod. SC-401, Km 12 - Distrito Industrial, Joinville - SC', '2024-07-22', '2025-10-09', true),
('Farmácia Popular', '(21) 91098-7654', 'comercial@farmaciapopular.com.br', 18000.00, 'Farmacêutico', 'Revenda', 'Av. Brasil, 1500 - Madureira, Rio de Janeiro - RJ', '2024-08-14', '2025-10-06', true),
('Academia Corpo e Mente', '(85) 90987-6543', 'recepcao@corpoeamente.com.br', 6000.00, 'Fitness e Bem-estar', 'Consumidor', 'R. do Ginásio, 88 - Aldeota, Fortaleza - CE', '2024-09-08', '2025-09-20', true),
('Escritório Advocacia & Cia', '(11) 89876-5432', 'contato@advocaciaecia.adv.br', 5000.00, 'Serviços Jurídicos', 'Consumidor', 'Av. Faria Lima, 2000 - Itaim Bibi, São Paulo - SP', '2024-10-01', '2025-10-07', true);
"""
    
    try:
        db.session.execute(db.text(clientes_sql))
        db.session.commit()
        
        from app.models import Cliente
        total = Cliente.query.count()
        print(f"✅ {total} clientes criados com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar clientes: {e}")
        db.session.rollback()
        return False

def criar_cotacoes():
    """Cria as 11 cotações do arquivo SQL"""
    print("\n📋 Criando cotações...")
    
    cotacoes_sql = """
INSERT INTO cotacao (cliente_id, produto, valor, status, data_cotacao, observacoes) VALUES
(1, '5 Licenças Software + 10 Computadores + Servidor + Instalação + Treinamento (40h)', 45000.00, 'Aprovada', '2024-01-25', 'COT-001A - Pagamento em 3x sem juros. Garantia de 12 meses.'),
(2, '4 Checkouts + 2 Balanças + Sistema gestão + 3 Câmeras + Instalação', 32000.00, 'Aprovada', '2024-02-28', 'COT-002A - Frete incluso. Instalação em até 15 dias úteis.'),
(3, '500 sacos cimento + 200m³ areia + 150m³ brita + 50t ferro + Entrega parcelada', 85000.00, 'Aprovada', '2024-03-18', 'COT-003A - Entregas quinzenais. Pagamento 30 dias após cada entrega.'),
(4, '2 Macas elétricas + Autoclave 21L + 5 Cadeiras + Armário + Materiais consumo', 18500.00, 'Enviada', '2024-04-15', 'COT-004E - Valores válidos por 30 dias. Frete grátis para SP.'),
(5, '30 Computadores + Projetor Full HD + 5 Impressoras + Software educacional + Instalação', 52000.00, 'Aprovada', '2024-05-20', 'COT-005A - Desconto especial educação. Garantia 24 meses.'),
(6, 'Forno industrial + Fogão 6 bocas + 2 Fritadeiras + Refrigerador 4 portas + Instalação', 28000.00, 'Rejeitada', '2024-06-22', 'COT-006R - Cliente optou por fornecedor concorrente.'),
(7, 'Contrato anual: 100t aço carbono/mês + 50t alumínio/mês + Entrega programada', 850000.00, 'Aprovada', '2024-08-01', 'COT-007A - Contrato 12 meses renováveis. Reajuste semestral IPCA.'),
(8, 'Fornecimento mensal medicamentos + Higiene/beleza + Suplementos + Equipamentos', 22000.00, 'Aprovada', '2024-08-25', 'COT-008A - Fornecimento mensal renovável. Primeira entrega em 10 dias.'),
(9, '10 Esteiras + 5 Bicicletas + Kit pesos + 3 Aparelhos musculação + Manutenção 6 meses', 42000.00, 'Enviada', '2024-09-20', 'COT-009E - Parcelamento em até 10x. Garantia 18 meses.'),
(10, '8 Mesas executivas + 8 Cadeiras + 5 Armários + 5 Computadores + 2 Impressoras + Rede', 28500.00, 'Aprovada', '2024-10-05', 'COT-010A - Montagem incluída. Entrega em 20 dias úteis.'),
(1, 'Upgrade Enterprise + 5 Licenças adicionais + BI + Consultoria (80h)', 28000.00, 'Enviada', '2025-10-01', 'COT-011E - Proposta de expansão do sistema atual.');
"""
    
    try:
        db.session.execute(db.text(cotacoes_sql))
        db.session.commit()
        
        from app.models import Cotacao
        total = Cotacao.query.count()
        print(f"✅ {total} cotações criadas com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar cotações: {e}")
        db.session.rollback()
        return False

def criar_pedidos():
    """Cria os 11 pedidos do arquivo SQL"""
    print("\n🛒 Criando pedidos...")
    
    pedidos_sql = """
INSERT INTO pedido (cliente_id, produto, quantidade, valor_total, status, data_pedido, observacoes) VALUES
(1, '5 Licenças Software + 10 Computadores + Servidor + Instalação + Treinamento', 1, 45000.00, 'Concluído', '2024-02-01', 'PED-001 - Cliente muito satisfeito. Entregue em 22/02/2024.'),
(2, '4 Checkouts + 2 Balanças + Sistema + 3 Câmeras + Instalação', 1, 32000.00, 'Concluído', '2024-03-05', 'PED-002 - Instalação fora do horário comercial. Entregue 20/03/2024.'),
(3, 'Primeira entrega: 100 sacos cimento + 40m³ areia + 30m³ brita + 10t ferro', 1, 17000.00, 'Concluído', '2024-03-25', 'PED-003A - Primeira de cinco entregas. Entregue 03/04/2024.'),
(3, 'Segunda entrega: 100 sacos cimento + 40m³ areia + 30m³ brita + 10t ferro', 1, 17000.00, 'Em Processamento', '2024-04-10', 'PED-003B - Previsão de entrega: 20/04/2024.'),
(5, '30 Computadores + Projetor + 5 Impressoras + Software + Instalação', 1, 52000.00, 'Em Processamento', '2024-06-25', 'PED-005 - Aguardando logística. Previsão: 20/07/2024.'),
(7, 'Fornecimento Agosto/2024: 100t aço carbono + 50t alumínio', 1, 70000.00, 'Concluído', '2024-08-05', 'PED-007-08 - Entregue 28/08/2024. Qualidade mantida.'),
(7, 'Fornecimento Setembro/2024: 100t aço carbono + 50t alumínio', 1, 70000.00, 'Concluído', '2024-09-05', 'PED-007-09 - Entregue 29/09/2024. Doc fiscal enviada.'),
(7, 'Fornecimento Outubro/2024: 100t aço carbono + 50t alumínio', 1, 70000.00, 'Em Processamento', '2024-10-05', 'PED-007-10 - Carga despachada. Previsão: 30/10/2024.'),
(8, 'Fornecimento Set/2024: Medicamentos + Higiene + Suplementos + Equipamentos', 1, 22000.00, 'Concluído', '2024-09-01', 'PED-008-09 - Primeira entrega contrato. Entregue 08/09/2024.'),
(8, 'Fornecimento Out/2024: Medicamentos + Higiene + Suplementos', 1, 22000.00, 'Pendente', '2024-10-01', 'PED-008-10 - Separação em andamento. Previsão: 10/10/2024.'),
(10, '8 Mesas + 8 Cadeiras + 5 Armários + 5 PCs + 2 Impressoras + Rede', 1, 28500.00, 'Em Processamento', '2024-10-08', 'PED-010 - Móveis em produção. Instalação: 28/10/2024.');
"""
    
    try:
        db.session.execute(db.text(pedidos_sql))
        db.session.commit()
        
        from app.models import Pedido
        total = Pedido.query.count()
        print(f"✅ {total} pedidos criados com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar pedidos: {e}")
        db.session.rollback()
        return False

def verificar_estrutura_banco():
    """Verifica se as tabelas têm a estrutura correta"""
    print("\n🔍 Verificando estrutura do banco de dados...")
    
    try:
        # Verificar se as colunas necessárias existem
        result = db.session.execute(db.text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'cliente'
            ORDER BY ordinal_position;
        """))
        
        colunas_cliente = [row[0] for row in result]
        print(f"   Colunas da tabela cliente: {', '.join(colunas_cliente)}")
        
        # Verificar campos necessários
        campos_necessarios = ['nome', 'telefone', 'email']
        campos_opcionais = ['limite_credito', 'area_atuacao', 'canal_vendas', 'endereco', 
                           'data_cadastro', 'ultimo_contato', 'ativo']
        
        faltando = [c for c in campos_necessarios if c not in colunas_cliente]
        
        if faltando:
            print(f"   ⚠️  Campos obrigatórios faltando: {', '.join(faltando)}")
            print(f"   ℹ️  Vou adaptar os dados para a estrutura atual do banco")
            return False
        else:
            print(f"   ✅ Estrutura do banco compatível!")
            return True
            
    except Exception as e:
        print(f"   ⚠️  Não foi possível verificar estrutura: {e}")
        return False

def main():
    """Função principal"""
    print("\n" + "="*70)
    print("🗃️  POPULANDO BANCO COM DADOS DO ARQUIVO SQL")
    print("    dados_ficticios_crm.sql")
    print("="*70)
    
    with app.app_context():
        try:
            # Verificar estrutura do banco
            estrutura_ok = verificar_estrutura_banco()
            
            # Verificar se há dados existentes
            from app.models import Cliente, Cotacao, Pedido
            
            clientes_existentes = Cliente.query.count()
            cotacoes_existentes = Cotacao.query.count()
            pedidos_existentes = Pedido.query.count()
            
            if clientes_existentes > 0 or cotacoes_existentes > 0 or pedidos_existentes > 0:
                print(f"\n⚠️  Dados existentes no banco:")
                print(f"   • {clientes_existentes} clientes")
                print(f"   • {cotacoes_existentes} cotações")
                print(f"   • {pedidos_existentes} pedidos")
                
                resposta = input("\n⚠️  Deseja LIMPAR todos os dados existentes? (s/n): ")
                if resposta.lower() == 's':
                    limpar_banco()
            
            # Criar dados na ordem correta (por causa das FKs)
            print("\n" + "="*70)
            print("📝 INSERINDO DADOS...")
            print("="*70)
            
            sucesso_clientes = criar_clientes()
            if not sucesso_clientes:
                print("\n❌ Falha ao criar clientes. Abortando...")
                sys.exit(1)
            
            sucesso_cotacoes = criar_cotacoes()
            if not sucesso_cotacoes:
                print("\n⚠️  Falha ao criar cotações, mas continuando...")
            
            sucesso_pedidos = criar_pedidos()
            if not sucesso_pedidos:
                print("\n⚠️  Falha ao criar pedidos, mas continuando...")
            
            # Resumo final
            clientes_final = Cliente.query.count()
            cotacoes_final = Cotacao.query.count()
            pedidos_final = Pedido.query.count()
            
            print("\n" + "="*70)
            print("✅ BANCO POPULADO COM SUCESSO!")
            print("="*70)
            print(f"\n📊 Resumo dos dados criados:")
            print(f"   • {clientes_final} clientes")
            print(f"   • {cotacoes_final} cotações")
            print(f"   • {pedidos_final} pedidos")
            
            print(f"\n💡 Acesse o dashboard para visualizar:")
            print(f"   https://crm-web-production-0848.up.railway.app/")
            
            print(f"\n📋 Detalhes dos clientes criados:")
            clientes = Cliente.query.all()
            for i, cliente in enumerate(clientes, 1):
                print(f"   {i}. {cliente.nome} - {cliente.email}")
            
            print()
            
        except Exception as e:
            print(f"\n❌ Erro fatal ao popular banco: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()
            sys.exit(1)

if __name__ == '__main__':
    main()