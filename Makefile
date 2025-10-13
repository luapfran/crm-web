help:
	@echo "Comandos disponíveis:"
	@echo "  make dev      - Inicia ambiente de desenvolvimento"
	@echo "  make up       - Inicia containers"
	@echo "  make down     - Para containers"
	@echo "  make logs     - Mostra logs"
	@echo "  make shell    - Acessa shell da aplicação"
	@echo "  make backup   - Cria backup do banco"

dev:
	docker-compose up -d
	@sleep 10
	docker-compose exec web flask db upgrade || docker-compose exec web flask init-db
	docker-compose exec web flask seed-db

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec web bash

backup:
	./backup.sh
