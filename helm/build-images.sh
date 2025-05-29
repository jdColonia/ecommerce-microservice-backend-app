#!/bin/bash

# Script para construir todas las imágenes Docker

ENVIRONMENT=${1:-dev}
TAG=${ENVIRONMENT}-$(date +%Y%m%d%H%M)

echo "Construyendo imágenes Docker para todos los servicios con tag: $TAG..."

services=("api-gateway" "cloud-config" "service-discovery" "order-service" "payment-service" "product-service" "shipping-service" "user-service" "favourite-service" "proxy-client")

for service in "${services[@]}"; do
  echo "Construyendo imagen para $service..."
  if [ -d "../$service" ]; then
    cd ..
    docker build -f $service/Dockerfile -t $service:$TAG -t $service:latest .
    cd helm
  else
    echo "Warning: Directory ../$service not found, skipping..."
  fi
done

echo "Todas las imágenes han sido construidas con tag: $TAG"
echo "También se ha creado el tag 'latest' para todas las imágenes"

# Verificar que las imágenes se crearon correctamente
echo "Verificando imágenes creadas:"
docker images | grep -E "($(IFS=\|; echo "${services[*]}"))"
