set -e


echo "Aguardando MinIO iniciar..."
sleep 10


mc alias set minio http://datalake:9000 "$MINIO_ROOT_USER" "$MINIO_ROOT_PASSWORD"
mc mb minio/landing-zone --ignore-existing
mc cp /clientes.csv minio/landing-zone/
echo "Upload do clientes.csv concluído!"
