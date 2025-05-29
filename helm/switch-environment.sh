#!/bin/bash

# Script para cambiar entre ambientes (dev, stage, prod)

# Verificar si se proporcionó un ambiente
CURRENT_ENV=${1}
TARGET_ENV=${2}

# Validar que se proporcionen ambos ambientes
if [[ -z "$CURRENT_ENV" || -z "$TARGET_ENV" ]]; then
  echo "Error: Debes proporcionar el ambiente actual y el objetivo."
  echo "Uso: ./switch-environment.sh [current_env] [target_env]"
  echo "Ambientes válidos: dev, stage, prod"
  exit 1
fi

# Validar que los ambientes sean válidos
for env in "$CURRENT_ENV" "$TARGET_ENV"; do
  if [[ "$env" != "dev" && "$env" != "stage" && "$env" != "prod" ]]; then
    echo "Error: El ambiente '$env' no es válido."
    echo "Ambientes válidos: dev, stage, prod"
    exit 1
  fi
done

CURRENT_RELEASE="ecommerce-app-$CURRENT_ENV"
TARGET_RELEASE="ecommerce-app-$TARGET_ENV"
NAMESPACE="ecommerce"

echo "Cambiando de ambiente $CURRENT_ENV a $TARGET_ENV..."

# Verificar si el release actual existe
if ! helm list -n $NAMESPACE | grep -q $CURRENT_RELEASE; then
  echo "Warning: El release $CURRENT_RELEASE no existe. Procediendo con la instalación del nuevo ambiente."
else
  echo "Desinstalando ambiente actual: $CURRENT_ENV"
  helm uninstall $CURRENT_RELEASE -n $NAMESPACE
fi

echo "Instalando nuevo ambiente: $TARGET_ENV"
helm install $TARGET_RELEASE ./ecommerce-app \
  -f ./ecommerce-app/values-$TARGET_ENV.yaml \
  -n $NAMESPACE \
  --create-namespace \
  --wait \
  --timeout=10m

echo "Cambio de ambiente completado de $CURRENT_ENV a $TARGET_ENV"
echo "URL de acceso: http://ecommerce-$TARGET_ENV.local"
