#!/bin/bash

# Script para verificar el estado de la aplicación

ENVIRONMENT=${1:-dev}
NAMESPACE="ecommerce"
RELEASE_NAME="ecommerce-app-$ENVIRONMENT"

echo "=== Estado de la aplicación en ambiente: $ENVIRONMENT ==="
echo ""

# Verificar si el release existe
if ! helm list -n $NAMESPACE | grep -q $RELEASE_NAME; then
  echo "Error: El release $RELEASE_NAME no existe en el namespace $NAMESPACE"
  echo "Releases disponibles:"
  helm list -n $NAMESPACE
  exit 1
fi

# Estado del release
echo "📦 Estado del Release Helm:"
helm status $RELEASE_NAME -n $NAMESPACE

echo ""
echo "🔧 Pods:"
kubectl get pods -n $NAMESPACE -l app.kubernetes.io/instance=$RELEASE_NAME

echo ""
echo "🌐 Servicios:"
kubectl get svc -n $NAMESPACE -l app.kubernetes.io/instance=$RELEASE_NAME

echo ""
echo "🔗 Ingress:"
kubectl get ingress -n $NAMESPACE

echo ""
echo "📊 Eventos recientes:"
kubectl get events -n $NAMESPACE --sort-by='.lastTimestamp' | tail -10

echo ""
echo "🔍 Para logs detallados de un pod específico:"
echo "  kubectl logs <pod-name> -n $NAMESPACE"
echo ""
echo "🌍 URL de acceso: http://ecommerce-$ENVIRONMENT.local"
