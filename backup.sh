#!/bin/bash

BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="crm_backup_$DATE.sql"

echo "Criando backup..."

docker-compose exec -T db pg_dump -U crm_user crm_database > "$BACKUP_DIR/$BACKUP_FILE"
gzip "$BACKUP_DIR/$BACKUP_FILE"

echo "✅ Backup: $BACKUP_FILE.gz"
