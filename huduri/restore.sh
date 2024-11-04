#!/bin/bash

# Hardcoded SA password (not recommended for production use)
# SA_PASSWORD="Helloworld1?"  # Replace with your actual SA password

# Wait for SQL Server to start
echo "Waiting for SQL Server to start..."
until sqlcmd -S localhost -U SA -P "$SA_PASSWORD" -Q "SELECT 1"; do
    >&2 echo "SQL Server is starting up"
    sleep 1
done

if [ -f /var/opt/mssql/backup/restore_complete.flag ]; then
    echo "Database restore has already been completed before."
    exit 0
fi

echo "SQL Server started. Restoring database..."

# Restore the database
sqlcmd -S localhost -U SA -P "$SA_PASSWORD" -Q "
RESTORE DATABASE huduri_production20240930
FROM DISK = '/var/opt/mssql/backup/huduri_production20240930.bak'
WITH MOVE 'pihrxyz_production' TO '/var/opt/mssql/data/huduri_production20240930.mdf',
     MOVE 'pihrxyz_production_log' TO '/var/opt/mssql/data/huduri_production20240930_log.ldf',
     REPLACE;
" || { echo "Database restore failed"; exit 1; }

# Create a flag file to indicate that the restore is complete
touch /var/opt/mssql/backup/restore_complete.flag

echo "Database restored successfully."
