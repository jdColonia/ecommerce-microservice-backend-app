# Helm Charts para Microservicios E-commerce

Este directorio contiene los charts de Helm para desplegar la aplicación de microservicios de e-commerce en Kubernetes.

## Estructura del Proyecto

```
helm/
├── ecommerce-app/                # Chart principal
│   ├── Chart.yaml                # Metadatos del chart
│   ├── values*.yaml              # Configuraciones por ambiente
│   ├── templates/                # Templates de Kubernetes
│   │   ├── _helpers.tpl          # Helpers globales
│   │   ├── configmap.yaml        # ConfigMap global
│   │   ├── serviceaccount.yaml   # ServiceAccount
│   │   └── ingress.yaml          # Ingress para API Gateway
│   └── charts/                   # Sub-charts de microservicios
│       ├── api-gateway/
│       ├── user-service/
│       ├── product-service/
│       ├── order-service/
│       ├── payment-service/
│       ├── shipping-service/
│       ├── favourite-service/
│       └── proxy-client/
├── build-images.sh               # Construcción de imágenes Docker
├── cleanup.sh                    # Limpieza de ambientes
├── deploy-helm.sh                # Despliegue estándar
├── logs.sh                       # Visualización de logs
├── setup-minikube.sh             # Configuración inicial de minikube
├── status.sh                     # Estado de la aplicación
├── switch-environment.sh         # Cambio entre ambientes
└── README.md                     # Esta documentación
```

## Ambientes Disponibles

- **dev**: Ambiente de desarrollo (1 replica por servicio)
- **stage**: Ambiente de staging (2 replicas por servicio)
- **prod**: Ambiente de producción (3 replicas por servicio)

## Scripts de Gestión

### 1. Configuración Inicial

```bash
# Configurar minikube y habilitar ingress
./setup-minikube.sh

# Construir imágenes Docker
./build-images.sh dev
```

### 2. Despliegue

```bash
# Instalar en ambiente dev
./deploy-helm.sh dev install

# Actualizar en ambiente dev
./deploy-helm.sh dev upgrade

# Desinstalar ambiente dev
./deploy-helm.sh dev uninstall
```

### 3. Gestión de Ambientes

```bash
# Cambiar de dev a stage
./switch-environment.sh dev stage

# Ver estado del ambiente
./status.sh dev

# Ver logs de un servicio
./logs.sh dev api-gateway
```

### 4. Limpieza

```bash
# Limpiar un ambiente específico
./cleanup.sh dev

# Limpiar todos los ambientes
./cleanup.sh
```

## Configuración de Red

### URLs de Acceso

- **Dev**: http://ecommerce-dev.local
- **Stage**: http://ecommerce-stage.local
- **Prod**: http://ecommerce.example.com

### Configurar /etc/hosts

```bash
# Obtener IP de minikube
MINIKUBE_IP=$(minikube ip)

# Agregar a /etc/hosts
echo "$MINIKUBE_IP ecommerce-dev.local" | sudo tee -a /etc/hosts
echo "$MINIKUBE_IP ecommerce-stage.local" | sudo tee -a /etc/hosts
```

## Personalización

### Modificar Recursos

Edita los archivos `values-*.yaml` para ajustar:

- Número de replicas
- Límites de CPU/memoria
- Variables de entorno
- Configuración de ingress

## Monitoreo

### Comandos Útiles

```bash
# Ver todos los pods
kubectl get pods -n ecommerce

# Ver servicios
kubectl get svc -n ecommerce

# Ver ingress
kubectl get ingress -n ecommerce

# Describir un pod
kubectl describe pod <pod-name> -n ecommerce

# Ejecutar bash en un pod
kubectl exec -it <pod-name> -n ecommerce -- /bin/bash
```

### Health Checks

Todos los servicios incluyen health checks en:

- Liveness Probe: `/actuator/health`
- Readiness Probe: `/actuator/health`

## Troubleshooting

### Problemas Comunes

1. **Pods en estado Pending**
   - Verificar recursos disponibles: `kubectl describe nodes`
   - Verificar tolerations y node selectors

2. **Ingress no funciona**
   - Verificar que ingress controller esté habilitado: `minikube addons list`
   - Verificar configuración de /etc/hosts

3. **Servicios no se comunican**
   - Verificar service discovery: `kubectl get ep -n ecommerce`
   - Revisar logs de eureka server

4. **Imágenes no se encuentran**
   - Verificar que Docker esté configurado para minikube: `eval $(minikube docker-env)`
   - Reconstruir imágenes: `./build-images.sh dev`

### Logs y Debugging

```bash
# Ver logs de todos los pods de un servicio
kubectl logs -l app=user-service -n ecommerce

# Ver eventos del namespace
kubectl get events -n ecommerce --sort-by='.lastTimestamp'

# Port forward para acceso directo
kubectl port-forward svc/ecommerce-app-dev-api-gateway 8080:8222 -n ecommerce
```

## Estructura de Configuración

### Variables de Entorno Comunes

- `SPRING_PROFILES_ACTIVE`: Ambiente actual (dev/stage/prod)
- `EUREKA_CLIENT_SERVICEURL_DEFAULTZONE`: URL del servidor Eureka
- `SPRING_ZIPKIN_BASE_URL`: URL de Zipkin para tracing
- `SPRING_CONFIG_IMPORT`: URL del config server

### ConfigMaps

Cada servicio tiene su propio ConfigMap con:

- Configuración específica de Spring Boot
- Variables de entorno del servicio
- Configuración de endpoints de actuator

### Secrets (Opcional)

Para ambientes de producción, considera usar Secrets para:

- Credenciales de base de datos
- Claves de API
- Certificados TLS
