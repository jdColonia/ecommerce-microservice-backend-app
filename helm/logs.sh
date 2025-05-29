#!/bin/bash

# Script para ver logs de los servicios

ENVIRONMENT=${1:-dev}
SERVICE=${2}
NAMESPACE="ecommerce"
RELEASE_NAME="ecommerce-app-$ENVIRONMENT"

if [[ -z "$SERVICE" ]]; then
  echo "Servicios disponibles:"
  kubectl get pods -n $NAMESPACE -l app.kubernetes.io/instance=$RELEASE_NAME -o custom-columns=NAME:.metadata.name,STATUS:.status.phase
  echo ""
  echo "Uso: ./logs.sh [env] [service-name]"
  echo "Ejemplo: ./logs.sh dev api-gateway"
  exit 1
fi

# Buscar el pod del servicio
POD_NAME=$(kubectl get pods -n $NAMESPACE -l app.kubernetes.io/instance=$RELEASE_NAME -o name | grep $SERVICE | head -1)

if [[ -z "$POD_NAME" ]]; then
  echo "Error: No se encontró el pod para el servicio '$SERVICE' en el ambiente '$ENVIRONMENT'"
  echo "Pods disponibles:"
  kubectl get pods -n $NAMESPACE -l app.kubernetes.io/instance=$RELEASE_NAME
  exit 1
fi

echo "Mostrando logs para $SERVICE en ambiente $ENVIRONMENT..."
echo "Pod: $POD_NAME"
echo ""

kubectl logs $POD_NAME -n $NAMESPACE -f
