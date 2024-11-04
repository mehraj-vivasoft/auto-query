docker pull mcr.microsoft.com/mssql/server:2022-latest
docker run --name huduri -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=Helloworld1?' -e 'MSSQL_PID=Developer' -p 1433:1433 --platform linux/amd64 -d mcr.microsoft.com/mssql/server:2022-latest
sudo docker exec -it huduri mkdir var/opt/mssql/backup
sudo docker cp huduri_production20240930.bak huduri:var/opt/mssql/backup
docker exec -it --user root huduri /bin/bash
apt-get update
apt-get install -y sudo curl git gnupg2 software-properties-common
apt-get install curl apt-transport-https gnupg2 -y
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/20.04/prod.list)"
apt-get update -y
apt-get install -y sqlcmd
sqlcmd -S localhost -U SA -P "Helloworld1?" -Q "RESTORE DATABASE huduri_production20240930 FROM DISK = '/var/opt/mssql/backup/huduri_production20240930.bak' WITH MOVE 'pihrxyz_production' TO '/var/opt/mssql/data/huduri_production20240930.mdf', MOVE 'pihrxyz_production_log' TO '/var/opt/mssql/data/huduri_production20240930_log.ldf', REPLACE"
exit
exit