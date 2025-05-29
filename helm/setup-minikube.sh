#!/bin/bash

# Script para configurar minikube y habilitar ingress

echo "Configurando minikube para el proyecto..."

# Verificar si minikube está corriendo
if ! minikube status > /dev/null 2>&1; then
  echo "Iniciando minikube..."
  minikube start --cpus=4 --memory=8192 --disk-size=20g
fi

# Habilitar ingress
echo "Habilitando ingress controller..."
minikube addons enable ingress

# Habilitar dashboard
echo "Habilitando dashboard..."
minikube addons enable dashboard

# Esperar a que el ingress controller esté listo
echo "Esperando a que el ingress controller esté listo..."
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Configurar Docker para usar el registro de minikube
echo "Configurando Docker para usar el registro de minikube..."
eval $(minikube docker-env)

# Crear namespace si no existe
echo "Creando namespace ecommerce..."
kubectl create namespace ecommerce --dry-run=client -o yaml | kubectl apply -f -

# Agregar entrada al /etc/hosts para acceso local
MINIKUBE_IP=$(minikube ip)
echo "Agregando entradas al /etc/hosts..."
echo "Para acceder a la aplicación, agrega estas líneas a tu /etc/hosts:"
echo "$MINIKUBE_IP ecommerce.local"
echo "$MINIKUBE_IP ecommerce-dev.local"
echo "$MINIKUBE_IP ecommerce-stage.local"

echo "Configuración de minikube completada!"
echo "IP de minikube: $MINIKUBE_IP"
