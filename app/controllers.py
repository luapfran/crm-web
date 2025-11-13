from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Cliente, Interacao, Cotacao, Pedido
from app.forms import ClienteForm, InteracaoForm, CotacaoForm, PedidoForm, StatusEntregaForm
from datetime import datetime, timedelta
from sqlalchemy import func, desc

# Cria o Blueprint principal
main_bp = Blueprint('main', __name__)


# ==================== ROTAS PRINCIPAIS ====================

@main_bp.route('/')
def index():
    """Página inicial - Dashboard"""
    
    # Estatísticas gerais
    total_clientes = Cliente.query.filter_by(ativo=True).count()
    total_cotacoes = Cotacao.query.count()
    total_pedidos = Pedido.query.count()
    
    # Cotações por status
    cotacoes_enviadas = Cotacao.query.filter_by(status='Enviada').count()
    cotacoes_aprovadas = Cotacao.query.filter_by(status='Aprovada').count()
    
    # Pedidos pendentes
    pedidos_pendentes = Pedido.query.filter_by(status_entrega='Pendente').count()
    
    return render_template('index.html',
        total_clientes=total_clientes,
        total_cotacoes=total_cotacoes,
        total_pedidos=total_pedidos,
        cotacoes_enviadas=cotacoes_enviadas,
        cotacoes_aprovadas=cotacoes_aprovadas,
        pedidos_pendentes=pedidos_pendentes
    )


# ==================== ROTAS DE CLIENTES ====================

@main_bp.route('/clientes')
def listar_clientes():
    """Lista todos os clientes"""
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Cliente.query.filter_by(ativo=True)
    
    if search:
        query = query.filter(
            (Cliente.nome.ilike(f'%{search}%')) |
            (Cliente.email.ilike(f'%{search}%')) |
            (Cliente.telefone.ilike(f'%{search}%'))
        )
    
    clientes = query.order_by(Cliente.nome).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('clientes/lista.html', clientes=clientes, search=search)


@main_bp.route('/clientes/novo', methods=['GET', 'POST'])
def novo_cliente():
    """Adiciona um novo cliente"""
    
    form = ClienteForm()
    
    if form.validate_on_submit():
        cliente = Cliente(
            nome=form.nome.data,
            telefone=form.telefone.data,
            email=form.email.data,
            limite_credito=form.limite_credito.data,
            area_atuacao=form.area_atuacao.data,
            canal_vendas=form.canal_vendas.data,
            empresa=form.empresa.data,
            endereco=form.endereco.data
        )
        
        db.session.add(cliente)
        db.session.commit()
        
        flash(f'Cliente {cliente.nome} cadastrado com sucesso!', 'success')
        return redirect(url_for('main.listar_clientes'))
    
    return render_template('clientes/novo.html', form=form)


@main_bp.route('/clientes/<int:id>')
def detalhes_cliente(id):
    """Exibe detalhes de um cliente específico"""
    
    cliente = Cliente.query.get_or_404(id)
    
    # Últimas interações
    interacoes = cliente.interacoes.order_by(desc(Interacao.data_hora)).limit(10).all()
    
    # Cotações
    cotacoes = cliente.cotacoes.order_by(desc(Cotacao.data_criacao)).all()
    
    # Pedidos
    pedidos = cliente.pedidos.order_by(desc(Pedido.data_criacao)).all()
    
    return render_template('clientes/detalhes.html',
        cliente=cliente,
        interacoes=interacoes,
        cotacoes=cotacoes,
        pedidos=pedidos
    )


@main_bp.route('/clientes/<int:id>/editar', methods=['GET', 'POST'])
def editar_cliente(id):
    """Edita um cliente existente"""
    
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(obj=cliente)
    
    if form.validate_on_submit():
        cliente.nome = form.nome.data
        cliente.telefone = form.telefone.data
        cliente.email = form.email.data
        cliente.limite_credito = form.limite_credito.data
        cliente.area_atuacao = form.area_atuacao.data
        cliente.canal_vendas = form.canal_vendas.data
        cliente.empresa = form.empresa.data
        cliente.endereco = form.endereco.data

        db.session.commit()
        
        flash(f'Cliente {cliente.nome} atualizado com sucesso!', 'success')
        return redirect(url_for('main.detalhes_cliente', id=cliente.id))
    
    return render_template('clientes/editar.html', form=form, cliente=cliente)


@main_bp.route('/clientes/<int:id>/desativar', methods=['POST'])
def desativar_cliente(id):
    """Desativa um cliente (soft delete)"""
    
    cliente = Cliente.query.get_or_404(id)
    cliente.ativo = False
    db.session.commit()
    
    flash(f'Cliente {cliente.nome} desativado com sucesso!', 'info')
    return redirect(url_for('main.listar_clientes'))


# ==================== ROTAS DE INTERAÇÕES ====================

@main_bp.route('/clientes/<int:cliente_id>/interacoes/nova', methods=['GET', 'POST'])
def nova_interacao(cliente_id):
    """Registra nova interação com cliente"""
    
    cliente = Cliente.query.get_or_404(cliente_id)
    form = InteracaoForm()
    
    if form.validate_on_submit():
        interacao = Interacao(
            cliente_id=cliente.id,
            tipo=form.tipo.data,
            descricao=form.descricao.data
        )
        
        # Atualiza último contato do cliente
        cliente.ultimo_contato = datetime.now().date()
        
        db.session.add(interacao)
        db.session.commit()
        
        flash('Interação registrada com sucesso!', 'success')
        return redirect(url_for('main.detalhes_cliente', id=cliente.id))
    
    return render_template('interacoes/nova.html', form=form, cliente=cliente)


# ==================== ROTAS DE COTAÇÕES ====================

@main_bp.route('/cotacoes')
def listar_cotacoes():
    """Lista todas as cotações"""
    
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '', type=str)
    
    query = Cotacao.query
    
    if status:
        query = query.filter_by(status=status)
    
    cotacoes = query.order_by(desc(Cotacao.data_criacao)).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('cotacoes/lista.html', cotacoes=cotacoes, status=status)


@main_bp.route('/clientes/<int:cliente_id>/cotacoes/nova', methods=['GET', 'POST'])
def nova_cotacao(cliente_id):
    """Cria nova cotação para cliente"""
    
    cliente = Cliente.query.get_or_404(cliente_id)
    form = CotacaoForm()
    
    if form.validate_on_submit():
        cotacao = Cotacao(
            cliente_id=cliente.id,
            itens=form.itens.data,
            valor_total=form.valor_total.data,
            validade=form.validade.data,
            observacoes=form.observacoes.data
        )
        
        # Atualiza último contato do cliente
        cliente.ultimo_contato = datetime.now().date()
        
        db.session.add(cotacao)
        db.session.commit()
        
        flash(f'Cotação {cotacao.id_cotacao} criada com sucesso!', 'success')
        return redirect(url_for('main.detalhes_cliente', id=cliente.id))
    
    return render_template('cotacoes/nova.html', form=form, cliente=cliente)


@main_bp.route('/cotacoes/<int:id>/converter', methods=['POST'])
def converter_cotacao_pedido(id):
    """Converte uma cotação em pedido"""
    
    cotacao = Cotacao.query.get_or_404(id)
    
    # Atualiza status da cotação
    cotacao.status = 'Aprovada'
    
    # Cria o pedido
    pedido = Pedido(
        cliente_id=cotacao.cliente_id,
        cotacao_id=cotacao.id,
        itens=cotacao.itens,
        valor_final=cotacao.valor_total
    )
    
    db.session.add(pedido)
    db.session.commit()
    
    flash(f'Cotação convertida em pedido {pedido.id_pedido} com sucesso!', 'success')
    return redirect(url_for('main.detalhes_cliente', id=cotacao.cliente_id))


@main_bp.route('/cotacoes/<int:id>/status', methods=['POST'])
def atualizar_status_cotacao(id):
    """Atualiza status de uma cotação"""
    
    cotacao = Cotacao.query.get_or_404(id)
    novo_status = request.form.get('status')
    
    if novo_status in ['Enviada', 'Aprovada', 'Recusada']:
        cotacao.status = novo_status
        db.session.commit()
        flash('Status da cotação atualizado!', 'success')
    else:
        flash('Status inválido!', 'error')
    
    return redirect(url_for('main.detalhes_cliente', id=cotacao.cliente_id))


# ==================== ROTAS DE PEDIDOS ====================

@main_bp.route('/pedidos')
def listar_pedidos():
    """Lista todos os pedidos"""
    
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '', type=str)
    
    query = Pedido.query
    
    if status:
        query = query.filter_by(status_entrega=status)
    
    pedidos = query.order_by(desc(Pedido.data_criacao)).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('pedidos/lista.html', pedidos=pedidos, status=status)


@main_bp.route('/pedidos/novo', methods=['GET', 'POST'])
def novo_pedido():
    """Cria novo pedido"""
    from app.forms import PedidoForm
    
    form = PedidoForm()
    
    # Lista de clientes ativos para o select
    clientes = Cliente.query.filter_by(ativo=True).order_by(Cliente.nome).all()
    
    if form.validate_on_submit():
        cliente_id = request.form.get('cliente_id')
        
        if not cliente_id:
            flash('Por favor, selecione um cliente!', 'error')
            return render_template('pedidos/novo.html', form=form, clientes=clientes)
        
        pedido = Pedido(
            cliente_id=int(cliente_id),
            itens=form.itens.data,
            valor_final=form.valor_final.data,
            data_entrega_prevista=form.data_entrega_prevista.data,
            observacoes=form.observacoes.data
        )
        
        db.session.add(pedido)
        db.session.commit()
        
        flash(f'Pedido {pedido.id_pedido} criado com sucesso!', 'success')
        return redirect(url_for('main.listar_pedidos'))
    
    return render_template('pedidos/novo.html', form=form, clientes=clientes)


@main_bp.route('/pedidos/<int:id>')
def detalhes_pedido(id):
    """Exibe detalhes de um pedido"""
    
    pedido = Pedido.query.get_or_404(id)
    form = StatusEntregaForm(obj=pedido)
    
    return render_template('pedidos/detalhes.html', pedido=pedido, form=form)


@main_bp.route('/pedidos/<int:id>/status', methods=['POST'])
def atualizar_status_pedido(id):
    """Atualiza status de entrega de um pedido"""
    
    pedido = Pedido.query.get_or_404(id)
    form = StatusEntregaForm()
    
    if form.validate_on_submit():
        pedido.status_entrega = form.status_entrega.data
        if form.data_entrega_real.data:
            pedido.data_entrega_real = form.data_entrega_real.data
        
        db.session.commit()
        flash('Status de entrega atualizado!', 'success')
    
    return redirect(url_for('main.detalhes_pedido', id=pedido.id))


# ==================== ROTAS DE RELATÓRIOS ====================

@main_bp.route('/relatorios')
def relatorios():
    """Dashboard de relatórios"""
    
    # Vendas por canal
    vendas_por_canal = db.session.query(
        Cliente.canal_vendas,
        func.count(Pedido.id).label('total_pedidos'),
        func.sum(Pedido.valor_final).label('valor_total')
    ).join(Pedido).group_by(Cliente.canal_vendas).all()
    
    # Top 10 clientes por valor de pedidos
    top_clientes = db.session.query(
        Cliente.nome,
        func.sum(Pedido.valor_final).label('valor_total')
    ).join(Pedido).group_by(Cliente.id).order_by(desc('valor_total')).limit(10).all()
    
    # Pedidos por status
    pedidos_por_status = db.session.query(
        Pedido.status_entrega,
        func.count(Pedido.id).label('total')
    ).group_by(Pedido.status_entrega).all()
    
    return render_template('relatorios/dashboard.html',
        vendas_por_canal=vendas_por_canal,
        top_clientes=top_clientes,
        pedidos_por_status=pedidos_por_status
    )


# ==================== API JSON (opcional) ====================

@main_bp.route('/api/clientes')
def api_clientes():
    """Retorna lista de clientes em JSON"""
    
    clientes = Cliente.query.filter_by(ativo=True).all()
    return jsonify([cliente.to_dict() for cliente in clientes])


@main_bp.route('/api/clientes/<int:id>')
def api_cliente_detalhes(id):
    """Retorna detalhes de um cliente em JSON"""
    
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.to_dict())

# ==================================================
# ROTA DEFINITIVA - USA SEU models.py ATUAL
# Cole este código no FINAL do arquivo app/controllers.py
# Substitua qualquer rota /admin/popular-banco anterior
# ==================================================

@main_bp.route('/admin/popular-banco')
def popular_banco():
    """Popula banco usando a estrutura CORRETA do models.py"""
    from flask import render_template_string
    from datetime import datetime
    
    try:
        # Recriar estrutura
        db.drop_all()
        db.create_all()
        
        # Inserir clientes - NOMES DE TABELA CORRETOS (PLURAL)
        sql_clientes = """
INSERT INTO clientes (nome, telefone, email, limite_credito, area_atuacao, canal_vendas, endereco, data_cadastro, ultimo_contato, ativo) VALUES
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
        
        # Inserir interações
        sql_interacoes = """
INSERT INTO interacoes (cliente_id, tipo, descricao, data_hora) VALUES
(1, 'Telefone', 'Primeiro contato - Cliente interessado em soluções de software empresarial', '2024-01-15 10:30:00'),
(1, 'Email', 'Envio de apresentação institucional e portfólio de produtos', '2024-01-16 14:20:00'),
(1, 'Reunião', 'Reunião presencial para entender necessidades específicas do cliente', '2024-01-22 15:00:00'),
(1, 'WhatsApp', 'Cliente solicitou cotação urgente para sistema de gestão', '2025-10-05 11:15:00'),
(2, 'Email', 'Cliente solicitou cotação de equipamentos para supermercado', '2024-02-20 09:00:00'),
(2, 'Telefone', 'Esclarecimento de dúvidas sobre prazo de entrega e garantia', '2024-02-25 16:45:00'),
(2, 'Visita', 'Visita técnica ao estabelecimento para avaliar necessidades', '2024-03-05 10:00:00'),
(2, 'Email', 'Cliente aprovou proposta e solicitou início do fornecimento', '2025-10-08 13:30:00'),
(3, 'Reunião', 'Apresentação de soluções para obras de grande porte', '2024-03-10 14:00:00'),
(3, 'Email', 'Envio de orçamento detalhado para obra do Shopping Leste', '2024-03-15 10:30:00'),
(3, 'Telefone', 'Negociação de condições de pagamento e prazo de entrega', '2024-03-20 11:00:00');
"""
        
        # Inserir cotações
        sql_cotacoes = """
INSERT INTO cotacoes (id_cotacao, cliente_id, itens, valor_total, status, data_criacao, validade, observacoes) VALUES
('COT-001A', 1, '- 5 Licenças de Software de Gestão Empresarial
- 10 Estações de trabalho (computadores)
- Servidor dedicado
- Instalação e configuração
- Treinamento para equipe (40h)', 45000.00, 'Aprovada', '2024-01-25', '2024-02-25', 'Pagamento em 3x sem juros. Garantia de 12 meses.'),

('COT-002A', 2, '- 4 Checkouts completos com leitores de código de barras
- 2 Balanças digitais
- Sistema de gestão de estoque
- 3 Câmeras de segurança
- Instalação e configuração', 32000.00, 'Aprovada', '2024-02-28', '2024-03-31', 'Frete incluso. Instalação em até 15 dias úteis.'),

('COT-003A', 3, '- 500 sacos de cimento CP-II 50kg
- 200 m³ de areia média
- 150 m³ de brita 1
- 50 toneladas de ferro 10mm
- Entrega parcelada conforme cronograma', 85000.00, 'Aprovada', '2024-03-18', '2024-04-18', 'Entregas quinzenais. Pagamento 30 dias após cada entrega.'),

('COT-004E', 4, '- 2 Macas hospitalares elétricas
- 1 Autoclave 21 litros
- 5 Cadeiras para sala de espera
- 1 Armário para medicamentos
- Materiais de consumo (diversos)', 18500.00, 'Enviada', '2024-04-15', '2025-11-15', 'Valores válidos por 30 dias. Frete grátis para São Paulo.'),

('COT-005A', 5, '- 30 Computadores para laboratório de informática
- 1 Projetor Full HD + tela de projeção
- 5 Impressoras multifuncionais
- Software educacional (licenças anuais)
- Instalação e configuração', 52000.00, 'Aprovada', '2024-05-20', '2024-06-20', 'Desconto especial para instituições de ensino. Garantia estendida de 24 meses.'),

('COT-006R', 6, '- 1 Forno industrial a gás
- 1 Fogão industrial 6 bocas
- 2 Fritadeiras elétricas
- 1 Refrigerador vertical 4 portas
- Instalação', 28000.00, 'Recusada', '2024-06-22', '2024-07-22', 'Cliente optou por fornecedor concorrente.'),

('COT-007A', 7, '- Contrato anual de fornecimento de matéria-prima
- 100 toneladas de aço carbono por mês
- 50 toneladas de alumínio por mês
- Entrega mensal programada
- Condições especiais de preço', 850000.00, 'Aprovada', '2024-08-01', '2024-09-01', 'Contrato de 12 meses renováveis. Reajuste semestral pelo IPCA.'),

('COT-008A', 8, '- Fornecimento mensal de medicamentos genéricos (lista anexa)
- Produtos de higiene e beleza
- Suplementos alimentares
- Equipamentos para farmácia (2x termômetros digitais, oxímetros)
- Condições de pagamento especiais', 22000.00, 'Aprovada', '2024-08-25', '2024-09-25', 'Fornecimento mensal renovável. Primeira entrega em 10 dias.'),

('COT-009E', 9, '- 10 Esteiras ergométricas
- 5 Bicicletas ergométricas
- Conjunto de pesos e halteres (kit completo)
- 3 Aparelhos de musculação multifuncionais
- Instalação e manutenção por 6 meses', 42000.00, 'Enviada', '2024-09-20', '2025-11-20', 'Parcelamento em até 10x. Garantia de 18 meses para equipamentos.'),

('COT-010A', 10, '- 8 Mesas executivas com gaveteiros
- 8 Cadeiras giratórias ergonômicas
- 5 Armários para arquivos
- 5 Computadores completos
- 2 Impressoras multifuncionais laser
- Rede estruturada e cabeamento', 28500.00, 'Aprovada', '2024-10-05', '2024-11-05', 'Montagem e instalação incluídas. Entrega em 20 dias úteis.'),

('COT-011E', 1, '- Upgrade do sistema de gestão para versão Enterprise
- 5 Licenças adicionais
- Módulo de Business Intelligence
- Consultoria e customização (80h)', 28000.00, 'Enviada', '2025-10-01', '2025-11-01', 'Proposta de expansão do sistema atual.');
"""
        
        # Inserir pedidos
        sql_pedidos = """
INSERT INTO pedidos (id_pedido, cliente_id, cotacao_id, itens, valor_final, status_entrega, data_criacao, data_entrega_prevista, data_entrega_real, observacoes) VALUES
('PED-001', 1, 1, '- 5 Licenças de Software de Gestão Empresarial
- 10 Estações de trabalho (computadores)
- Servidor dedicado
- Instalação e configuração
- Treinamento para equipe (40h)', 45000.00, 'Entregue', '2024-02-01', '2024-02-25', '2024-02-22', 'Cliente muito satisfeito. Treinamento concluído com sucesso.'),

('PED-002', 2, 2, '- 4 Checkouts completos com leitores de código de barras
- 2 Balanças digitais
- Sistema de gestão de estoque
- 3 Câmeras de segurança
- Instalação e configuração', 32000.00, 'Entregue', '2024-03-05', '2024-03-25', '2024-03-20', 'Instalação realizada fora do horário comercial conforme solicitado.'),

('PED-003A', 3, 3, 'Primeira entrega (cronograma):
- 100 sacos de cimento CP-II 50kg
- 40 m³ de areia média
- 30 m³ de brita 1
- 10 toneladas de ferro 10mm', 17000.00, 'Entregue', '2024-03-25', '2024-04-05', '2024-04-03', 'Primeira de cinco entregas programadas.'),

('PED-003B', 3, 3, 'Segunda entrega (cronograma):
- 100 sacos de cimento CP-II 50kg
- 40 m³ de areia média
- 30 m³ de brita 1
- 10 toneladas de ferro 10mm', 17000.00, 'Enviado', '2024-04-10', '2024-04-20', NULL, 'Previsão de entrega confirmada para 20/04.'),

('PED-005', 5, 5, '- 30 Computadores para laboratório de informática
- 1 Projetor Full HD + tela de projeção
- 5 Impressoras multifuncionais
- Software educacional (licenças anuais)
- Instalação e configuração', 52000.00, 'Em processamento', '2024-06-25', '2024-07-20', NULL, 'Aguardando liberação do setor de logística. Entrega prevista dentro do prazo.'),

('PED-007-08', 7, 7, 'Fornecimento mensal - Agosto/2024:
- 100 toneladas de aço carbono
- 50 toneladas de alumínio
- Entrega conforme programação', 70000.00, 'Entregue', '2024-08-05', '2024-08-30', '2024-08-28', 'Entrega dentro do cronograma. Cliente solicitou manutenção do padrão de qualidade.'),

('PED-007-09', 7, 7, 'Fornecimento mensal - Setembro/2024:
- 100 toneladas de aço carbono
- 50 toneladas de alumínio
- Entrega conforme programação', 70000.00, 'Entregue', '2024-09-05', '2024-09-30', '2024-09-29', 'Entrega concluída. Documentação fiscal enviada por email.'),

('PED-007-10', 7, 7, 'Fornecimento mensal - Outubro/2024:
- 100 toneladas de aço carbono
- 50 toneladas de alumínio
- Entrega conforme programação', 70000.00, 'Enviado', '2024-10-05', '2024-10-30', NULL, 'Carga despachada. Previsão de chegada em 3 dias úteis.'),

('PED-008-09', 8, 8, 'Fornecimento mensal - Setembro/2024:
- Medicamentos genéricos (lista anexa)
- Produtos de higiene e beleza
- Suplementos alimentares
- Equipamentos (termômetros, oxímetros)', 22000.00, 'Entregue', '2024-09-01', '2024-09-10', '2024-09-08', 'Primeira entrega do contrato mensal. Tudo conforme especificado.'),

('PED-008-10', 8, 8, 'Fornecimento mensal - Outubro/2024:
- Medicamentos genéricos (lista anexa)
- Produtos de higiene e beleza
- Suplementos alimentares', 22000.00, 'Pendente', '2024-10-01', '2024-10-10', NULL, 'Pedido confirmado. Separação em andamento no CD.'),

('PED-010', 10, 10, '- 8 Mesas executivas com gaveteiros
- 8 Cadeiras giratórias ergonômicas
- 5 Armários para arquivos
- 5 Computadores completos
- 2 Impressoras multifuncionais laser
- Rede estruturada e cabeamento', 28500.00, 'Em processamento', '2024-10-08', '2024-10-28', NULL, 'Móveis em produção. Computadores já estão no estoque. Instalação agendada para 28/10.');
"""
        
        # Executar todos os SQLs
        db.session.execute(db.text(sql_clientes))
        db.session.execute(db.text(sql_interacoes))
        db.session.execute(db.text(sql_cotacoes))
        db.session.execute(db.text(sql_pedidos))
        db.session.commit()
        
        # Contar dados criados
        from app.models import Cliente, Interacao, Cotacao, Pedido
        total_clientes = Cliente.query.count()
        total_interacoes = Interacao.query.count()
        total_cotacoes = Cotacao.query.count()
        total_pedidos = Pedido.query.count()
        
        # HTML de sucesso bonito
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>✅ Banco Populado com Sucesso!</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }}
                .container {{
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                    max-width: 700px;
                    width: 100%;
                    overflow: hidden;
                    animation: slideUp 0.5s ease-out;
                }}
                @keyframes slideUp {{
                    from {{ opacity: 0; transform: translateY(30px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 50px 30px;
                    text-align: center;
                }}
                .header h1 {{
                    font-size: 3em;
                    margin-bottom: 10px;
                    animation: bounce 1s ease;
                }}
                @keyframes bounce {{
                    0%, 100% {{ transform: translateY(0); }}
                    50% {{ transform: translateY(-10px); }}
                }}
                .header p {{
                    opacity: 0.95;
                    font-size: 1.2em;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .stats {{
                    background: #f8f9fa;
                    border-radius: 15px;
                    padding: 30px;
                    margin-bottom: 30px;
                }}
                .stats h2 {{
                    color: #333;
                    margin-bottom: 25px;
                    font-size: 1.6em;
                    text-align: center;
                }}
                .stat-grid {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 20px;
                }}
                .stat-card {{
                    background: white;
                    padding: 20px;
                    border-radius: 12px;
                    text-align: center;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.07);
                    transition: transform 0.2s;
                }}
                .stat-card:hover {{
                    transform: translateY(-5px);
                }}
                .stat-icon {{
                    font-size: 2.5em;
                    margin-bottom: 10px;
                }}
                .stat-value {{
                    font-size: 2.5em;
                    font-weight: bold;
                    color: #667eea;
                    margin-bottom: 5px;
                }}
                .stat-label {{
                    color: #666;
                    font-size: 1em;
                }}
                .btn {{
                    display: block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    padding: 18px 30px;
                    border-radius: 12px;
                    text-align: center;
                    font-size: 1.2em;
                    font-weight: 600;
                    transition: all 0.3s;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                }}
                .btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                }}
                .footer {{
                    text-align: center;
                    padding: 25px;
                    color: #999;
                    font-size: 0.95em;
                    border-top: 1px solid #f0f0f0;
                }}
                @media (max-width: 600px) {{
                    .stat-grid {{ grid-template-columns: 1fr; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅</h1>
                    <p><strong>Banco Populado com Sucesso!</strong></p>
                    <p style="font-size: 0.9em; margin-top: 10px;">Dados do arquivo dados_ficticios_crm.sql</p>
                </div>
                
                <div class="content">
                    <div class="stats">
                        <h2>📊 Dados Criados</h2>
                        <div class="stat-grid">
                            <div class="stat-card">
                                <div class="stat-icon">👥</div>
                                <div class="stat-value">{total_clientes}</div>
                                <div class="stat-label">Clientes</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-icon">💬</div>
                                <div class="stat-value">{total_interacoes}</div>
                                <div class="stat-label">Interações</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-icon">📋</div>
                                <div class="stat-value">{total_cotacoes}</div>
                                <div class="stat-label">Cotações</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-icon">🛒</div>
                                <div class="stat-value">{total_pedidos}</div>
                                <div class="stat-label">Pedidos</div>
                            </div>
                        </div>
                    </div>
                    
                    <a href="/" class="btn">🏠 Ir para o Dashboard</a>
                </div>
                
                <div class="footer">
                    Sistema CRM - Dados de exemplo inseridos com sucesso
                </div>
            </div>
        </body>
        </html>
        """
        
        return render_template_string(html)
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>❌ Erro ao Popular Banco</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 50px auto; padding: 20px; background: #f5f5f5; }}
                .error {{ background: #f8d7da; border: 2px solid #f5c6cb; color: #721c24; padding: 30px; border-radius: 10px; }}
                h1 {{ margin-bottom: 20px; }}
                pre {{ background: #fff; padding: 20px; border-radius: 5px; overflow-x: auto; font-size: 13px; border: 1px solid #ddd; }}
                .btn {{ display: inline-block; margin-top: 20px; padding: 12px 25px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>❌ Erro ao Popular Banco de Dados</h1>
                <p><strong>Erro:</strong> {str(e)}</p>
                <p><strong>Detalhes técnicos:</strong></p>
                <pre>{error_detail}</pre>
            </div>
            <a href="/" class="btn">Voltar ao Dashboard</a>
        </body>
        </html>
        """
        return render_template_string(error_html), 500