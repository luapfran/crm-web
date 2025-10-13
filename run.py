import os
from app import create_app, db
from app.models import Cliente, Interacao, Cotacao, Pedido

app = create_app(os.getenv('FLASK_ENV') or 'development')

@app.cli.command()
def init_db():
    """Inicializa o banco de dados"""
    db.create_all()
    print('Banco de dados inicializado!')

@app.cli.command()
def seed_db():
    """Popula o banco com dados de exemplo"""
    if Cliente.query.first():
        print('Banco já contém dados!')
        return
    
    cliente = Cliente(
        nome='Empresa Exemplo Ltda',
        telefone='11999998888',
        email='contato@exemplo.com',
        limite_credito=5000.00,
        area_atuacao='Tecnologia',
        canal_vendas='Indústria'
    )
    db.session.add(cliente)
    db.session.commit()
    print('Dados de exemplo adicionados!')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
