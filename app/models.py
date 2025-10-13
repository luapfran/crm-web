from datetime import datetime
from app import db
import uuid

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    limite_credito = db.Column(db.Float, default=0.0)
    area_atuacao = db.Column(db.String(100))
    canal_vendas = db.Column(db.String(50))
    endereco = db.Column(db.String(200))  # <--- novo campo
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)
    ultimo_contato = db.Column(db.Date, nullable=True)
    ativo = db.Column(db.Boolean, default=True)
    
    interacoes = db.relationship('Interacao', backref='cliente', lazy='dynamic', cascade='all, delete-orphan')
    cotacoes = db.relationship('Cotacao', backref='cliente', lazy='dynamic', cascade='all, delete-orphan')
    pedidos = db.relationship('Pedido', backref='cliente', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Cliente {self.nome}>'

class Interacao(db.Model):
    __tablename__ = 'interacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.utcnow)

class Cotacao(db.Model):
    __tablename__ = 'cotacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    id_cotacao = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4())[:8])
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    itens = db.Column(db.Text, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='Enviada')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    validade = db.Column(db.Date, nullable=True)
    observacoes = db.Column(db.Text)

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    
    id = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.String(50), unique=True, default=lambda: str(uuid.uuid4())[:8])
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    cotacao_id = db.Column(db.Integer, db.ForeignKey('cotacoes.id'), nullable=True)
    itens = db.Column(db.Text, nullable=False)
    valor_final = db.Column(db.Float, nullable=False)
    status_entrega = db.Column(db.String(30), default='Pendente')
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_entrega_prevista = db.Column(db.Date, nullable=True)
    data_entrega_real = db.Column(db.Date, nullable=True)
    observacoes = db.Column(db.Text)
