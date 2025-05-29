#!/bin/bash

# Script para limpiar recursos

ENVIRONMENT=${1}
NAMESPACE="ecommerce"

# Función para limpiar un ambiente específico
cleanup_environment() {
  local env=$1
  echo ""
  echo "🧹 Limpiando ambiente: $env"
  echo "=========================="
  
  # Listar todos los releases que coincidan con el patrón
  echo "Buscando releases para el ambiente $env..."
  releases=$(helm list -n $NAMESPACE -q | grep "ecommerce-app-$env" || true)
  
  if [ -n "$releases" ]; then
    echo ""
    echo "📦 Releases encontrados:"
    echo "$releases"
    echo ""
    
    # Mostrar el orden de desinstalación
    echo "🔄 Desinstalando en orden inverso al despliegue..."
    echo ""
    
    # Desinstalar en orden inverso (aplicación -> infraestructura)
    echo "1. Desinstalando microservicios de aplicación..."
    app_releases=$(echo "$releases" | grep -E "(client|favourite|shipping|payment|order|product|user)" || true)
    if [ -n "$app_releases" ]; then
      echo "$app_releases" | while read -r release; do
        if [ -n "$release" ]; then
          echo "  Desinstalando $release..."
          helm uninstall "$release" -n $NAMESPACE
        fi
      done
    fi
    
    echo ""
    echo "2. Desinstalando API Gateway..."
    gateway_release=$(echo "$releases" | grep "gateway" || true)
    if [ -n "$gateway_release" ]; then
      echo "  Desinstalando $gateway_release..."
      helm uninstall "$gateway_release" -n $NAMESPACE
    fi
    
    echo ""
    echo "3. Desinstalando servicios de infraestructura..."
    infra_releases=$(echo "$releases" | grep -E "(config|eureka|zipkin)" || true)
    if [ -n "$infra_releases" ]; then
      # Desinstalar en orden inverso: config -> eureka -> zipkin
      config_release=$(echo "$infra_releases" | grep "config" || true)
      eureka_release=$(echo "$infra_releases" | grep "eureka" || true)
      zipkin_release=$(echo "$infra_releases" | grep "zipkin" || true)
      
      [ -n "$config_release" ] && echo "  Desinstalando $config_release..." && helm uninstall "$config_release" -n $NAMESPACE
      [ -n "$eureka_release" ] && echo "  Desinstalando $eureka_release..." && helm uninstall "$eureka_release" -n $NAMESPACE
      [ -n "$zipkin_release" ] && echo "  Desinstalando $zipkin_release..." && helm uninstall "$zipkin_release" -n $NAMESPACE
    fi
    
    # Verificar que no queden releases
    remaining=$(helm list -n $NAMESPACE -q | grep "ecommerce-app-$env" || true)
    if [ -n "$remaining" ]; then
      echo ""
      echo "⚠️  Releases restantes encontrados, forzando eliminación:"
      echo "$remaining" | while read -r release; do
        if [ -n "$release" ]; then
          echo "  Forzando eliminación de $release..."
          helm uninstall "$release" -n $NAMESPACE --ignore-not-found
        fi
      done
    fi
    
  else
    echo "ℹ️  No se encontraron releases para el ambiente $env"
  fi
  
  # Limpiar Ingress específico del ambiente
  echo ""
  echo "4. Limpiando Ingress..."
  kubectl delete ingress "ecommerce-app-$env-ingress" -n $NAMESPACE --ignore-not-found
  
  echo ""
  echo "✅ Ambiente $env limpiado correctamente"
}

# Función para limpiar todo
cleanup_all() {
  echo ""
  echo "🧹 LIMPIEZA COMPLETA DE TODOS LOS AMBIENTES"
  echo "=========================================="
  
  # Listar todos los releases en el namespace
  all_releases=$(helm list -n $NAMESPACE -q || true)
  
  if [ -n "$all_releases" ]; then
    echo ""
    echo "📦 Todos los releases encontrados:"
    echo "$all_releases"
    echo ""
    
    echo "🔄 Desinstalando todos los releases..."
    echo "$all_releases" | while read -r release; do
      if [ -n "$release" ]; then
        echo "  Desinstalando $release..."
        helm uninstall "$release" -n $NAMESPACE
      fi
    done
  else
    echo "ℹ️  No se encontraron releases en el namespace $NAMESPACE"
  fi
  
  # Eliminar todos los Ingress
  echo ""
  echo "🔗 Limpiando todos los Ingress..."
  kubectl delete ingress --all -n $NAMESPACE --ignore-not-found
  
  # Eliminar namespace completo
  echo ""
  echo "📁 Eliminando namespace $NAMESPACE..."
  kubectl delete namespace $NAMESPACE --ignore-not-found
  
  echo ""
  echo "✅ Limpieza completa realizada"
}

# Lógica principal
if [[ -z "$ENVIRONMENT" ]]; then
  echo "🤔 No se especificó un ambiente específico."
  echo ""
  echo "Ambientes disponibles:"
  
  # Mostrar ambientes disponibles
  envs=$(helm list -n $NAMESPACE -o json 2>/dev/null | jq -r '.[].name' | sed 's/ecommerce-app-\([^-]*\)-.*/\1/' | sort -u || echo "No hay ambientes desplegados")
  
  if [ "$envs" != "No hay ambientes desplegados" ]; then
    echo "$envs" | while read -r env; do
      if [ -n "$env" ]; then
        releases_count=$(helm list -n $NAMESPACE -q | grep "ecommerce-app-$env" | wc -l)
        echo "  - $env ($releases_count releases)"
      fi
    done
  else
    echo "  No hay ambientes desplegados actualmente"
  fi
  
  echo ""
  echo "¿Deseas limpiar TODOS los ambientes? (y/N)"
  read -r response
  if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    cleanup_all
  else
    echo "Operación cancelada."
    echo ""
    echo "💡 Para limpiar un ambiente específico:"
    echo "   ./cleanup.sh [dev|stage|prod]"
  fi
else
  # Validar ambiente
  if [[ "$ENVIRONMENT" != "dev" && "$ENVIRONMENT" != "stage" && "$ENVIRONMENT" != "prod" ]]; then
    echo "❌ Error: El ambiente debe ser 'dev', 'stage' o 'prod'."
    echo "Uso: ./cleanup.sh [dev|stage|prod]"
    exit 1
  fi
  
  cleanup_environment "$ENVIRONMENT"
fi

echo ""
echo "🔍 Para verificar que la limpieza fue exitosa:"
echo "   kubectl get pods -n $NAMESPACE"
echo "   helm list -n $NAMESPACE"
