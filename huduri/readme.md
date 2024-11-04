docker build --platform linux/amd64 -t huduri-mssql .
docker run --name huduri -p 1433:1433 -d huduri-mssql

