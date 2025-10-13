# 📊 Sistema CRM Web - Customer Relationship Management

Sistema completo de gerenciamento de relacionamento com clientes (CRM) desenvolvido em Python com Flask, seguindo o padrão MVC (Model-View-Controller).

## 🚀 Início Rápido

```bash
# Executar setup automático
chmod +x setup.sh
./setup.sh

# Ou usar Make
make dev

# Ou Docker Compose direto
docker-compose up -d
```

Acesse: http://localhost:5000

## 📚 Documentação Completa

- [README.md](README.md) - Documentação principal
- [QUICKSTART.md](QUICKSTART.md) - Guia rápido
- [DEPLOY.md](DEPLOY.md) - Deploy em produção
- [CHANGELOG.md](CHANGELOG.md) - Histórico de versões

## 🛠️ Tecnologias

- Python 3.11 + Flask 3.0
- PostgreSQL 15
- Bootstrap 5
- Docker & Docker Compose

## 📦 Estrutura

```
crm-web/
├── app/                    # Aplicação principal
│   ├── models.py          # Models (Banco)
│   ├── controllers.py     # Controllers (Lógica)
│   ├── forms.py           # Formulários
│   ├── templates/         # Views (HTML)
│   └── static/            # CSS, JS
├── docker-compose.yml     # Docker
├── requirements.txt       # Dependências
└── run.py                # Executar app
```

## 📞 Suporte

Abra uma Issue no GitHub ou consulte a documentação.

---

**Desenvolvido com ❤️ usando Python & Flask**
