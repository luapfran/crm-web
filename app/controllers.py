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

@main_bp.route('/admin/popular-banco')
def popular_banco():
    """Rota administrativa para popular o banco"""
    from flask import render_template_string
    
    try:
        # Recriar estrutura
        db.drop_all()
        db.create_all()
        
        # Criar clientes
        clientes_data = [
            Cliente(nome='Tech Solutions Ltda', telefone='(11) 98765-4321', email='contato@techsolutions.com.br', empresa='Tech Solutions', segmento='Tecnologia', observacoes='Cliente Indústria - SP'),
            Cliente(nome='Supermercado Bom Preço', telefone='(21) 97654-3210', email='compras@bompreco.com.br', empresa='Bom Preço', segmento='Varejo', observacoes='Cliente Revenda - RJ'),
            Cliente(nome='Construtora Alicerce S/A', telefone='(85) 96543-2109', email='obras@alicerce.com.br', empresa='Alicerce', segmento='Construção', observacoes='Cliente Indústria - CE'),
            Cliente(nome='Clínica Saúde Total', telefone='(11) 95432-1098', email='administrativo@saudetotal.com.br', empresa='Saúde Total', segmento='Saúde', observacoes='Cliente Consumidor - SP'),
            Cliente(nome='Escola Futuro Brilhante', telefone='(81) 94321-0987', email='diretoria@futurobrilhante.edu.br', empresa='Futuro Brilhante', segmento='Educação', observacoes='Cliente Consumidor - PE'),
            Cliente(nome='Restaurante Sabor & Arte', telefone='(11) 93210-9876', email='gerencia@saborarte.com.br', empresa='Sabor & Arte', segmento='Alimentação', observacoes='Cliente Revenda - SP'),
            Cliente(nome='Indústria Metal Forte', telefone='(48) 92109-8765', email='suprimentos@metalforte.ind.br', empresa='Metal Forte', segmento='Metalúrgica', observacoes='Cliente Indústria - SC'),
            Cliente(nome='Farmácia Popular', telefone='(21) 91098-7654', email='comercial@farmaciapopular.com.br', empresa='Farmácia Popular', segmento='Farmacêutico', observacoes='Cliente Revenda - RJ'),
            Cliente(nome='Academia Corpo e Mente', telefone='(85) 90987-6543', email='recepcao@corpoeamente.com.br', empresa='Corpo e Mente', segmento='Fitness', observacoes='Cliente Consumidor - CE'),
            Cliente(nome='Escritório Advocacia & Cia', telefone='(11) 89876-5432', email='contato@advocaciaecia.adv.br', empresa='Advocacia & Cia', segmento='Jurídico', observacoes='Cliente Consumidor - SP'),
        ]
        
        for cliente in clientes_data:
            db.session.add(cliente)
        db.session.commit()
        
        # Criar cotações (pegando IDs dos clientes)
        clientes = Cliente.query.all()
        
        cotacoes_data = [
            Cotacao(cliente_id=clientes[0].id, produto='5 Licenças Software + Computadores + Servidor', valor=45000.00, status='Aprovada', data_cotacao=datetime(2024, 1, 25), observacoes='COT-001A'),
            Cotacao(cliente_id=clientes[1].id, produto='4 Checkouts + Balanças + Sistema', valor=32000.00, status='Aprovada', data_cotacao=datetime(2024, 2, 28), observacoes='COT-002A'),
            Cotacao(cliente_id=clientes[2].id, produto='Materiais construção (cimento, areia, brita)', valor=85000.00, status='Aprovada', data_cotacao=datetime(2024, 3, 18), observacoes='COT-003A'),
            Cotacao(cliente_id=clientes[3].id, produto='Equipamentos hospitalares', valor=18500.00, status='Em Análise', data_cotacao=datetime(2024, 4, 15), observacoes='COT-004E'),
            Cotacao(cliente_id=clientes[4].id, produto='Equipamentos informática escola', valor=52000.00, status='Aprovada', data_cotacao=datetime(2024, 5, 20), observacoes='COT-005A'),
            Cotacao(cliente_id=clientes[5].id, produto='Equipamentos cozinha industrial', valor=28000.00, status='Rejeitada', data_cotacao=datetime(2024, 6, 22), observacoes='COT-006R'),
            Cotacao(cliente_id=clientes[6].id, produto='Contrato anual: aço + alumínio', valor=850000.00, status='Aprovada', data_cotacao=datetime(2024, 8, 1), observacoes='COT-007A'),
            Cotacao(cliente_id=clientes[7].id, produto='Fornecimento mensal medicamentos', valor=22000.00, status='Aprovada', data_cotacao=datetime(2024, 8, 25), observacoes='COT-008A'),
            Cotacao(cliente_id=clientes[8].id, produto='Equipamentos academia completa', valor=42000.00, status='Em Análise', data_cotacao=datetime(2024, 9, 20), observacoes='COT-009E'),
            Cotacao(cliente_id=clientes[9].id, produto='Mobiliário escritório + TI', valor=28500.00, status='Aprovada', data_cotacao=datetime(2024, 10, 5), observacoes='COT-010A'),
        ]
        
        for cotacao in cotacoes_data:
            db.session.add(cotacao)
        db.session.commit()
        
        # Criar pedidos
        pedidos_data = [
            Pedido(cliente_id=clientes[0].id, produto='Software + Computadores', quantidade=1, valor_total=45000.00, status='Concluído', data_pedido=datetime(2024, 2, 1), observacoes='PED-001'),
            Pedido(cliente_id=clientes[1].id, produto='Checkouts + Sistema', quantidade=1, valor_total=32000.00, status='Concluído', data_pedido=datetime(2024, 3, 5), observacoes='PED-002'),
            Pedido(cliente_id=clientes[2].id, produto='Materiais 1ª entrega', quantidade=1, valor_total=17000.00, status='Concluído', data_pedido=datetime(2024, 3, 25), observacoes='PED-003A'),
            Pedido(cliente_id=clientes[2].id, produto='Materiais 2ª entrega', quantidade=1, valor_total=17000.00, status='Em Processamento', data_pedido=datetime(2024, 4, 10), observacoes='PED-003B'),
            Pedido(cliente_id=clientes[4].id, produto='Equipamentos escola', quantidade=1, valor_total=52000.00, status='Em Processamento', data_pedido=datetime(2024, 6, 25), observacoes='PED-005'),
            Pedido(cliente_id=clientes[6].id, produto='Fornecimento Agosto', quantidade=1, valor_total=70000.00, status='Concluído', data_pedido=datetime(2024, 8, 5), observacoes='PED-007-08'),
            Pedido(cliente_id=clientes[6].id, produto='Fornecimento Setembro', quantidade=1, valor_total=70000.00, status='Concluído', data_pedido=datetime(2024, 9, 5), observacoes='PED-007-09'),
            Pedido(cliente_id=clientes[6].id, produto='Fornecimento Outubro', quantidade=1, valor_total=70000.00, status='Em Processamento', data_pedido=datetime(2024, 10, 5), observacoes='PED-007-10'),
            Pedido(cliente_id=clientes[7].id, produto='Medicamentos Setembro', quantidade=1, valor_total=22000.00, status='Concluído', data_pedido=datetime(2024, 9, 1), observacoes='PED-008-09'),
            Pedido(cliente_id=clientes[7].id, produto='Medicamentos Outubro', quantidade=1, valor_total=22000.00, status='Pendente', data_pedido=datetime(2024, 10, 1), observacoes='PED-008-10'),
            Pedido(cliente_id=clientes[9].id, produto='Mobiliário + TI', quantidade=1, valor_total=28500.00, status='Em Processamento', data_pedido=datetime(2024, 10, 8), observacoes='PED-010'),
        ]
        
        for pedido in pedidos_data:
            db.session.add(pedido)
        db.session.commit()
        
        # Contar
        total_clientes = Cliente.query.count()
        total_cotacoes = Cotacao.query.count()
        total_pedidos = Pedido.query.count()
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Banco Populado</title>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background: #f5f5f5; }}
                .success {{ background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 20px; border-radius: 5px; }}
                .stats {{ background: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-top: 20px; }}
                .btn {{ display: inline-block; padding: 10px 20px; background: #007bff; color: white !important; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="success">
                <h1>✅ Banco Populado com Sucesso!</h1>
            </div>
            <div class="stats">
                <h2>📊 Dados Criados:</h2>
                <ul>
                    <li><strong>{total_clientes}</strong> clientes</li>
                    <li><strong>{total_cotacoes}</strong> cotações</li>
                    <li><strong>{total_pedidos}</strong> pedidos</li>
                </ul>
                <a href="/" class="btn">Ir para o Dashboard</a>
            </div>
        </body>
        </html>
        """
        
        return render_template_string(html)
        
    except Exception as e:
        return f"<h1>Erro:</h1><pre>{str(e)}</pre>", 500