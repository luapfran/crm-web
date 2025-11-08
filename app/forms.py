from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
import phonenumbers


class ClienteForm(FlaskForm):
    """Formulário para cadastro e edição de clientes"""
    
    nome = StringField('Nome', validators=[
        DataRequired(message='Nome é obrigatório'),
        Length(min=3, max=200, message='Nome deve ter entre 3 e 200 caracteres')
    ])
    
    telefone = StringField('Telefone', validators=[
        DataRequired(message='Telefone é obrigatório'),
        Length(min=10, max=20, message='Telefone inválido')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email é obrigatório'),
        Email(message='Email inválido')
    ])
    
    empresa = StringField('Empresa', validators=[DataRequired(message='Empresa é obrigatória'),
        Length(min=5, max=200, message='Empresa deve ter entre 5 e 200 caracteres')
    ])
    
    limite_credito = FloatField('Limite de Crédito (R$)', validators=[
        DataRequired(message='Limite de crédito é obrigatório'),
        NumberRange(min=0, message='Limite de crédito deve ser positivo')
    ])
    
    area_atuacao = StringField('Área de Atuação', validators=[
        DataRequired(message='Área de atuação é obrigatória'),
        Length(max=100)
    ])
    
    endereco = StringField('Endereço', validators=[
        Length(max=200, message='Endereço deve ter no máximo 200 caracteres'),
        Optional()
    ])
    
    canal_vendas = SelectField('Canal de Vendas', 
        choices=[
            ('', 'Selecione...'),
            ('Revenda', 'Revenda'),
            ('Indústria', 'Indústria'),
            ('Consumidor', 'Consumidor')
        ],
        validators=[DataRequired(message='Canal de vendas é obrigatório')]
    )
    
    submit = SubmitField('Salvar')
    
    def validate_telefone(self, field):
        """Validação personalizada para telefone brasileiro"""
        try:
            # Remove caracteres não numéricos
            numero_limpo = ''.join(filter(str.isdigit, field.data))
            
            # Valida se tem pelo menos 10 dígitos (DDD + número)
            if len(numero_limpo) < 10:
                raise ValueError('Telefone deve ter pelo menos 10 dígitos')
                
            # Tenta validar como número brasileiro
            numero = phonenumbers.parse('+55' + numero_limpo, 'BR')
            if not phonenumbers.is_valid_number(numero):
                raise ValueError('Número de telefone inválido')
                
        except Exception as e:
            from wtforms.validators import ValidationError
            raise ValidationError('Telefone inválido. Use formato: (XX) XXXXX-XXXX')


class InteracaoForm(FlaskForm):
    """Formulário para registro de interações"""
    
    tipo = SelectField('Tipo de Interação',
        choices=[
            ('', 'Selecione...'),
            ('Telefone', 'Telefone'),
            ('Email', 'Email'),
            ('Reunião', 'Reunião'),
            ('WhatsApp', 'WhatsApp'),
            ('Visita', 'Visita'),
            ('Outro', 'Outro')
        ],
        validators=[DataRequired(message='Tipo de interação é obrigatório')]
    )
    
    descricao = TextAreaField('Descrição', validators=[
        DataRequired(message='Descrição é obrigatória'),
        Length(min=10, max=1000, message='Descrição deve ter entre 10 e 1000 caracteres')
    ])
    
    submit = SubmitField('Registrar')


class CotacaoForm(FlaskForm):
    """Formulário para criação de cotações"""
    
    itens = TextAreaField('Descrição dos Itens', validators=[
        DataRequired(message='Descrição dos itens é obrigatória'),
        Length(min=10, max=2000)
    ])
    
    valor_total = FloatField('Valor Total (R$)', validators=[
        DataRequired(message='Valor total é obrigatório'),
        NumberRange(min=0.01, message='Valor deve ser maior que zero')
    ])
    
    validade = DateField('Validade da Cotação', validators=[Optional()], format='%Y-%m-%d')
    
    observacoes = TextAreaField('Observações', validators=[Optional(), Length(max=1000)])
    
    submit = SubmitField('Criar Cotação')


class PedidoForm(FlaskForm):
    """Formulário para criação de pedidos"""
    
    itens = TextAreaField('Descrição dos Itens', validators=[
        DataRequired(message='Descrição dos itens é obrigatória'),
        Length(min=10, max=2000)
    ])
    
    valor_final = FloatField('Valor Final (R$)', validators=[
        DataRequired(message='Valor final é obrigatório'),
        NumberRange(min=0.01, message='Valor deve ser maior que zero')
    ])
    
    data_entrega_prevista = DateField('Data de Entrega Prevista', 
        validators=[Optional()], 
        format='%Y-%m-%d'
    )
    
    observacoes = TextAreaField('Observações', validators=[Optional(), Length(max=1000)])
    
    submit = SubmitField('Criar Pedido')


class StatusEntregaForm(FlaskForm):
    """Formulário para atualizar status de entrega"""
    
    status_entrega = SelectField('Status da Entrega',
        choices=[
            ('Pendente', 'Pendente'),
            ('Em processamento', 'Em processamento'),
            ('Enviado', 'Enviado'),
            ('Entregue', 'Entregue'),
            ('Cancelado', 'Cancelado')
        ],
        validators=[DataRequired()]
    )
    
    data_entrega_real = DateField('Data de Entrega Real', 
        validators=[Optional()], 
        format='%Y-%m-%d'
    )
    
    submit = SubmitField('Atualizar Status')