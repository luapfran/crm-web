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
# ROTA CORRIGIDA PARA POPULAR BANCO
# Cole este código no FINAL do arquivo app/controllers.py
# ==================================================

@main_bp.route('/admin/popular-banco')
def popular_banco():
    """Rota administrativa para popular o banco - VERSÃO CORRIGIDA"""
    from flask import render_template_string
    from datetime import datetime
    
    try:
        # Recriar estrutura
        db.drop_all()
        db.create_all()
        
        # Criar clientes - APENAS com campos que existem
        clientes_data = [
            {
                'nome': 'Tech Solutions Ltda',
                'telefone': '(11) 98765-4321',
                'email': 'contato@techsolutions.com.br',
                'empresa': 'Tech Solutions',
                'observacoes': 'Tecnologia da Informação - Indústria - Limite: R$ 15.000 - São Paulo/SP'
            },
            {
                'nome': 'Supermercado Bom Preço',
                'telefone': '(21) 97654-3210',
                'email': 'compras@bompreco.com.br',
                'empresa': 'Bom Preço',
                'observacoes': 'Varejo Alimentício - Revenda - Limite: R$ 25.000 - Rio de Janeiro/RJ'
            },
            {
                'nome': 'Construtora Alicerce S/A',
                'telefone': '(85) 96543-2109',
                'email': 'obras@alicerce.com.br',
                'empresa': 'Alicerce',
                'observacoes': 'Construção Civil - Indústria - Limite: R$ 50.000 - Fortaleza/CE'
            },
            {
                'nome': 'Clínica Saúde Total',
                'telefone': '(11) 95432-1098',
                'email': 'administrativo@saudetotal.com.br',
                'empresa': 'Saúde Total',
                'observacoes': 'Saúde - Consumidor - Limite: R$ 10.000 - São Paulo/SP'
            },
            {
                'nome': 'Escola Futuro Brilhante',
                'telefone': '(81) 94321-0987',
                'email': 'diretoria@futurobrilhante.edu.br',
                'empresa': 'Futuro Brilhante',
                'observacoes': 'Educação - Consumidor - Limite: R$ 8.000 - Recife/PE'
            },
            {
                'nome': 'Restaurante Sabor & Arte',
                'telefone': '(11) 93210-9876',
                'email': 'gerencia@saborarte.com.br',
                'empresa': 'Sabor & Arte',
                'observacoes': 'Alimentação - Revenda - Limite: R$ 12.000 - São Paulo/SP'
            },
            {
                'nome': 'Indústria Metal Forte',
                'telefone': '(48) 92109-8765',
                'email': 'suprimentos@metalforte.ind.br',
                'empresa': 'Metal Forte',
                'observacoes': 'Indústria Metalúrgica - Indústria - Limite: R$ 80.000 - Joinville/SC'
            },
            {
                'nome': 'Farmácia Popular',
                'telefone': '(21) 91098-7654',
                'email': 'comercial@farmaciapopular.com.br',
                'empresa': 'Farmácia Popular',
                'observacoes': 'Farmacêutico - Revenda - Limite: R$ 18.000 - Rio de Janeiro/RJ'
            },
            {
                'nome': 'Academia Corpo e Mente',
                'telefone': '(85) 90987-6543',
                'email': 'recepcao@corpoeamente.com.br',
                'empresa': 'Corpo e Mente',
                'observacoes': 'Fitness e Bem-estar - Consumidor - Limite: R$ 6.000 - Fortaleza/CE'
            },
            {
                'nome': 'Escritório Advocacia & Cia',
                'telefone': '(11) 89876-5432',
                'email': 'contato@advocaciaecia.adv.br',
                'empresa': 'Advocacia & Cia',
                'observacoes': 'Serviços Jurídicos - Consumidor - Limite: R$ 5.000 - São Paulo/SP'
            }
        ]
        
        # Criar clientes
        for data in clientes_data:
            cliente = Cliente(**data)
            db.session.add(cliente)
        db.session.commit()
        
        # Buscar clientes criados
        clientes = Cliente.query.all()
        
        # Criar cotações
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
                'produto': '4 Checkouts completos + 2 Balanças digitais + Sistema gestão + 3 Câmeras',
                'valor': 32000.00,
                'status': 'Aprovada',
                'data_cotacao': datetime(2024, 2, 28),
                'observacoes': 'COT-002A - Frete incluso. Instalação em até 15 dias úteis.'
            },
            {
                'cliente_id': clientes[2].id,
                'produto': '500 sacos cimento + 200m³ areia + 150m³ brita + 50t ferro',
                'valor': 85000.00,
                'status': 'Aprovada',
                'data_cotacao': datetime(2024, 3, 18),
                'observacoes': 'COT-003A - Entregas quinzenais. Pagamento 30 dias após cada entrega.'
            },
            {
                'cliente_id': clientes[3].id,
                'produto': '2 Macas hospitalares elétricas + Autoclave 21L + 5 Cadeiras + Armário',
                'valor': 18500.00,
                'status': 'Em Análise',
                'data_cotacao': datetime(2024, 4, 15),
                'observacoes': 'COT-004E - Valores válidos por 30 dias. Frete grátis para SP.'
            },
            {
                'cliente_id': clientes[4].id,
                'produto': '30 Computadores + Projetor Full HD + 5 Impressoras + Software educacional',
                'valor': 52000.00,
                'status': 'Aprovada',
                'data_cotacao': datetime(2024, 5, 20),
                'observacoes': 'COT-005A - Desconto especial para educação. Garantia 24 meses.'
            },
            {
                'cliente_id': clientes[5].id,
                'produto': 'Forno industrial + Fogão 6 bocas + 2 Fritadeiras + Refrigerador 4 portas',
                'valor': 28000.00,
                'status': 'Rejeitada',
                'data_cotacao': datetime(2024, 6, 22),
                'observacoes': 'COT-006R - Cliente optou por fornecedor concorrente.'
            },
            {
                'cliente_id': clientes[6].id,
                'produto': 'Contrato anual: 100t aço carbono/mês + 50t alumínio/mês',
                'valor': 850000.00,
                'status': 'Aprovada',
                'data_cotacao': datetime(2024, 8, 1),
                'observacoes': 'COT-007A - Contrato 12 meses renováveis. Reajuste semestral IPCA.'
            },
            {
                'cliente_id': clientes[7].id,
                'produto': 'Fornecimento mensal: medicamentos + higiene + suplementos',
                'valor': 22000.00,
                'status': 'Aprovada',
                'data_cotacao': datetime(2024, 8, 25),
                'observacoes': 'COT-008A - Fornecimento mensal renovável. Primeira entrega em 10 dias.'
            },
            {
                'cliente_id': clientes[8].id,
                'produto': '10 Esteiras + 5 Bicicletas + Kit pesos + 3 Aparelhos musculação',
                'valor': 42000.00,
                'status': 'Em Análise',
                'data_cotacao': datetime(2024, 9, 20),
                'observacoes': 'COT-009E - Parcelamento em até 10x. Garantia 18 meses.'
            },
            {
                'cliente_id': clientes[9].id,
                'produto': '8 Mesas executivas + 8 Cadeiras + 5 Armários + 5 Computadores + Rede',
                'valor': 28500.00,
                'status': 'Aprovada',
                'data_cotacao': datetime(2024, 10, 5),
                'observacoes': 'COT-010A - Montagem e instalação incluídas. Entrega em 20 dias úteis.'
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
        
        for data in cotacoes_data:
            cotacao = Cotacao(**data)
            db.session.add(cotacao)
        db.session.commit()
        
        # Criar pedidos
        pedidos_data = [
            {
                'cliente_id': clientes[0].id,
                'produto': '5 Licenças Software + 10 Computadores + Servidor',
                'quantidade': 1,
                'valor_total': 45000.00,
                'status': 'Concluído',
                'data_pedido': datetime(2024, 2, 1),
                'observacoes': 'PED-001 - Cliente muito satisfeito. Entregue em 22/02/2024.'
            },
            {
                'cliente_id': clientes[1].id,
                'produto': '4 Checkouts + 2 Balanças + Sistema + 3 Câmeras',
                'quantidade': 1,
                'valor_total': 32000.00,
                'status': 'Concluído',
                'data_pedido': datetime(2024, 3, 5),
                'observacoes': 'PED-002 - Instalação fora do horário. Entregue 20/03/2024.'
            },
            {
                'cliente_id': clientes[2].id,
                'produto': '1ª entrega: 100 sacos cimento + 40m³ areia + 30m³ brita + 10t ferro',
                'quantidade': 1,
                'valor_total': 17000.00,
                'status': 'Concluído',
                'data_pedido': datetime(2024, 3, 25),
                'observacoes': 'PED-003A - Primeira de cinco entregas. Entregue 03/04/2024.'
            },
            {
                'cliente_id': clientes[2].id,
                'produto': '2ª entrega: 100 sacos cimento + 40m³ areia + 30m³ brita + 10t ferro',
                'quantidade': 1,
                'valor_total': 17000.00,
                'status': 'Em Processamento',
                'data_pedido': datetime(2024, 4, 10),
                'observacoes': 'PED-003B - Previsão de entrega: 20/04/2024.'
            },
            {
                'cliente_id': clientes[4].id,
                'produto': '30 Computadores + Projetor + 5 Impressoras + Software',
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
                'produto': 'Fornecimento Set/2024: Medicamentos + Higiene + Suplementos',
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
        
        for data in pedidos_data:
            pedido = Pedido(**data)
            db.session.add(pedido)
        db.session.commit()
        
        # Contar totais
        total_clientes = Cliente.query.count()
        total_cotacoes = Cotacao.query.count()
        total_pedidos = Pedido.query.count()
        
        # HTML de sucesso
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Banco Populado com Sucesso</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                * {{ margin: 0; padding: 0; box-sizing: border-box; }}
                body {{ 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
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
                    max-width: 600px;
                    width: 100%;
                    overflow: hidden;
                }}
                .header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 40px 30px;
                    text-align: center;
                }}
                .header h1 {{
                    font-size: 2.5em;
                    margin-bottom: 10px;
                }}
                .header p {{
                    opacity: 0.9;
                    font-size: 1.1em;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .stats {{
                    background: #f8f9fa;
                    border-radius: 10px;
                    padding: 25px;
                    margin-bottom: 30px;
                }}
                .stats h2 {{
                    color: #333;
                    margin-bottom: 20px;
                    font-size: 1.5em;
                }}
                .stat-item {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 15px 0;
                    border-bottom: 1px solid #e0e0e0;
                }}
                .stat-item:last-child {{
                    border-bottom: none;
                }}
                .stat-label {{
                    color: #666;
                    font-size: 1.1em;
                }}
                .stat-value {{
                    font-size: 1.8em;
                    font-weight: bold;
                    color: #667eea;
                }}
                .btn {{
                    display: block;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    text-decoration: none;
                    padding: 15px 30px;
                    border-radius: 10px;
                    text-align: center;
                    font-size: 1.1em;
                    font-weight: 600;
                    transition: transform 0.2s, box-shadow 0.2s;
                }}
                .btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
                }}
                .footer {{
                    text-align: center;
                    padding: 20px;
                    color: #999;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Sucesso!</h1>
                    <p>Banco de dados populado com dados fictícios</p>
                </div>
                
                <div class="content">
                    <div class="stats">
                        <h2>📊 Dados Criados</h2>
                        <div class="stat-item">
                            <span class="stat-label">👥 Clientes</span>
                            <span class="stat-value">{total_clientes}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">📋 Cotações</span>
                            <span class="stat-value">{total_cotacoes}</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">🛒 Pedidos</span>
                            <span class="stat-value">{total_pedidos}</span>
                        </div>
                    </div>
                    
                    <a href="/" class="btn">🏠 Ir para o Dashboard</a>
                </div>
                
                <div class="footer">
                    Sistema CRM - Dados de exemplo para testes
                </div>
            </div>
        </body>
        </html>
        """
        
        return render_template_string(html)
        
    except Exception as e:
        # HTML de erro
        error_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Erro ao Popular Banco</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
                .error {{ background: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; padding: 20px; border-radius: 5px; }}
                pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                .btn {{ display: inline-block; margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="error">
                <h1>❌ Erro ao Popular Banco</h1>
                <p><strong>Mensagem de erro:</strong></p>
                <pre>{str(e)}</pre>
            </div>
            <a href="/" class="btn">Voltar ao Dashboard</a>
        </body>
        </html>
        """
        return render_template_string(error_html), 500