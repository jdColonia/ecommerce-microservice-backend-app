#!/bin/bash

# Script para desplegar la aplicación con Helm

# Verificar si se proporcionó un ambiente
ENVIRONMENT=${1:-dev}
ACTION=${2:-install}

# Validar que el ambiente sea válido
if [[ "$ENVIRONMENT" != "dev" && "$ENVIRONMENT" != "stage" && "$ENVIRONMENT" != "prod" ]]; then
  echo "Error: El ambiente debe ser 'dev', 'stage' o 'prod'."
  echo "Uso: ./deploy-helm.sh [dev|stage|prod] [install|upgrade|uninstall]"
  exit 1
fi

# Validar que la acción sea válida
if [[ "$ACTION" != "install" && "$ACTION" != "upgrade" && "$ACTION" != "uninstall" ]]; then
  echo "Error: La acción debe ser 'install', 'upgrade' o 'uninstall'."
  echo "Uso: ./deploy-helm.sh [dev|stage|prod] [install|upgrade|uninstall]"
  exit 1
fi

NAMESPACE="ecommerce"

echo "Ejecutando acción '$ACTION' para el ambiente: $ENVIRONMENT..."

# Función para esperar a que un pod esté listo
wait_for_pod() {
  local service_name=$1
  local timeout=${2:-300}
  
  echo "  Esperando a que $service_name esté listo..."
  if kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=$service_name -n $NAMESPACE --timeout=${timeout}s; then
    echo "  ✅ $service_name está listo"
    return 0
  else
    echo "  ❌ $service_name no pudo iniciarse en $timeout segundos"
    return 1
  fi
}

# Función para desplegar un servicio individual
deploy_service() {
  local service_name=$1
  local release_suffix=$2
  local wait_time=${3:-300}
  
  local release_name="ecommerce-app-$ENVIRONMENT-$release_suffix"
  
  echo "📦 Desplegando $service_name..."
  
  if helm install $release_name ./ecommerce-app/charts/$service_name \
    -n $NAMESPACE \
    --set global.environment=$ENVIRONMENT \
    --set global.imageTag=latest \
    --set global.imagePullPolicy=IfNotPresent \
    --wait \
    --timeout=5m; then
    
    # Esperar a que el pod esté completamente listo
    wait_for_pod $service_name $wait_time
    return $?
  else
    echo "  ❌ Error desplegando $service_name"
    return 1
  fi
}

# Función para actualizar un servicio individual
upgrade_service() {
  local service_name=$1
  local release_suffix=$2
  
  local release_name="ecommerce-app-$ENVIRONMENT-$release_suffix"
  
  echo "📦 Actualizando $service_name..."
  
  helm upgrade $release_name ./ecommerce-app/charts/$service_name \
    -n $NAMESPACE \
    --set global.environment=$ENVIRONMENT \
    --set global.imageTag=latest \
    --set global.imagePullPolicy=IfNotPresent \
    --wait \
    --timeout=5m
}

# Función para desinstalar todos los servicios
uninstall_all_services() {
  echo "🧹 Desinstalando todos los servicios del ambiente $ENVIRONMENT..."
  
  # Listar todos los releases que coincidan con el patrón
  releases=$(helm list -n $NAMESPACE -q | grep "ecommerce-app-$ENVIRONMENT" || true)
  
  if [ -n "$releases" ]; then
    echo "Releases encontrados:"
    echo "$releases"
    echo ""
    
    # Desinstalar cada release
    echo "$releases" | while read -r release; do
      if [ -n "$release" ]; then
        echo "Desinstalando $release..."
        helm uninstall "$release" -n $NAMESPACE
      fi
    done
  else
    echo "No se encontraron releases para el ambiente $ENVIRONMENT"
  fi
}

# Función para desplegar servicios en paralelo
deploy_parallel() {
  local services=("$@")
  local pids=()
  local failures=0

  # Iniciar todos los servicios en segundo plano
  for service_config in "${services[@]}"; do
    service_name=$(echo $service_config | cut -d: -f1)
    service_suffix=$(echo $service_config | cut -d: -f2)
    
    echo "🚀 Iniciando despliegue de $service_name en segundo plano..."
    deploy_service "$service_name" "$service_suffix" 240 &
    pids+=($!)
  done

  # Esperar a que todos los procesos terminen
  for pid in "${pids[@]}"; do
    wait $pid || ((failures++))
  done

  return $failures
}

# Función para actualizar servicios en paralelo
upgrade_parallel() {
  local services=("$@")
  local pids=()
  local failures=0

  # Iniciar todas las actualizaciones en segundo plano
  for service_config in "${services[@]}"; do
    service_name=$(echo $service_config | cut -d: -f1)
    service_suffix=$(echo $service_config | cut -d: -f2)
    
    echo "🔄 Iniciando actualización de $service_name en segundo plano..."
    upgrade_service "$service_name" "$service_suffix" &
    pids+=($!)
  done

  # Esperar a que todos los procesos terminen
  for pid in "${pids[@]}"; do
    wait $pid || ((failures++))
  done

  return $failures
}

# Crear namespace si no existe (solo para install/upgrade)
if [[ "$ACTION" == "install" || "$ACTION" == "upgrade" ]]; then
  kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
fi

case $ACTION in
  "install")
    echo ""
    echo "🚀 INICIANDO DESPLIEGUE POR FASES PARA AMBIENTE: $ENVIRONMENT"
    echo "=================================================="
    
    # FASE 1: Servicios de Infraestructura
    echo ""
    echo "📋 FASE 1: Desplegando servicios de infraestructura..."
    echo "----------------------------------------------------"
    
    # 1.1: Zipkin (primero, sin dependencias)
    if ! deploy_service "zipkin" "zipkin" 300; then
      echo "❌ Error en Fase 1: Zipkin falló. Abortando despliegue."
      exit 1
    fi
    
    # 1.2: Service Discovery (depende de tener un sistema de trazado listo)
    if ! deploy_service "service-discovery" "eureka" 300; then
      echo "❌ Error en Fase 1: Service Discovery falló. Abortando despliegue."
      exit 1
    fi
    
    # 1.3: Cloud Config (depende de Service Discovery)
    if ! deploy_service "cloud-config" "config" 300; then
      echo "❌ Error en Fase 1: Cloud Config falló. Abortando despliegue."
      exit 1
    fi
    
    echo "✅ Fase 1 completada: Infraestructura lista"
    
    # FASE 2: API Gateway
    echo ""
    echo "📋 FASE 2: Desplegando API Gateway..."
    echo "------------------------------------"
    
    if ! deploy_service "api-gateway" "gateway" 300; then
      echo "❌ Error en Fase 2: API Gateway falló. Abortando despliegue."
      exit 1
    fi
    
    echo "✅ Fase 2 completada: API Gateway listo"
    
    # FASE 3: Microservicios de Aplicación (en paralelo)
    echo ""
    echo "📋 FASE 3: Desplegando microservicios de aplicación en paralelo..."
    echo "--------------------------------------------------------------"
    
    # Lista de microservicios para despliegue paralelo
    app_services=(
      "user-service:user"
      "product-service:product" 
      "order-service:order"
      "payment-service:payment"
      "shipping-service:shipping"
      "favourite-service:favourite"
      "proxy-client:client"
    )
    
    deploy_parallel "${app_services[@]}"
    failures=$?
    
    if [ $failures -ne 0 ]; then
      echo "⚠️  Advertencia: $failures servicios fallaron durante el despliegue paralelo"
    fi
    
    echo "✅ Fase 3 completada: Microservicios desplegados"
    
    # FASE 4: Ingreso
    echo ""
    echo "📋 FASE 4: Configurando Ingress..."
    echo "---------------------------------"
    
    cat <<EOL | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ecommerce-app-$ENVIRONMENT-ingress
  namespace: $NAMESPACE
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  ingressClassName: nginx
  rules:
  - host: ecommerce-$ENVIRONMENT.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: ecommerce-app-$ENVIRONMENT-gateway-api-gateway
            port:
              number: 8222
EOL
    
    echo "✅ Fase 4 completada: Ingress configurado"
    ;;
    
  "upgrade")
    echo ""
    echo "🔄 ACTUALIZANDO APLICACIÓN EN AMBIENTE: $ENVIRONMENT"
    echo "================================================="
    
    # Actualizar en el mismo orden que el despliegue para servicios críticos
    echo "Actualizando servicios de infraestructura..."
    upgrade_service "zipkin" "zipkin"
    upgrade_service "service-discovery" "eureka" 
    upgrade_service "cloud-config" "config"
    
    echo "Actualizando API Gateway..."
    upgrade_service "api-gateway" "gateway"
    
    echo "Actualizando microservicios en paralelo..."
    app_services=(
      "user-service:user"
      "product-service:product" 
      "order-service:order"
      "payment-service:payment"
      "shipping-service:shipping"
      "favourite-service:favourite"
      "proxy-client:client"
    )
    
    upgrade_parallel "${app_services[@]}"
    failures=$?
    
    if [ $failures -ne 0 ]; then
      echo "⚠️  Advertencia: $failures servicios fallaron durante la actualización paralela"
    fi
    ;;
    
  "uninstall")
    uninstall_all_services
    ;;
esac

if [[ "$ACTION" == "install" || "$ACTION" == "upgrade" ]]; then
  echo ""
  echo "=================================================="
  echo "✅ DESPLIEGUE COMPLETADO PARA AMBIENTE: $ENVIRONMENT"
  echo "=================================================="
  echo ""
  echo "📊 Para verificar el estado:"
  echo "  kubectl get pods -n $NAMESPACE"
  echo ""
  echo "🌐 Para ver los servicios:"
  echo "  kubectl get svc -n $NAMESPACE"
  echo ""
  echo "🔗 Para ver el ingress:"
  echo "  kubectl get ingress -n $NAMESPACE"
  echo ""
  echo "🌍 URL de acceso: http://ecommerce-$ENVIRONMENT.local"
  echo ""
  echo "🔍 Para monitorear logs:"
  echo "  ./logs.sh $ENVIRONMENT [service-name]"
  echo ""
  echo "📈 Para ver el estado detallado:"
  echo "  ./status.sh $ENVIRONMENT"
fi
