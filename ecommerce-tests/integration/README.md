# Pruebas de Integración - Ecosistema de Microservicios

Este directorio contiene las pruebas de integración completas para todo el ecosistema de microservicios del e-commerce.

## 🏗️ Arquitectura de Servicios

### Servicios de Infraestructura

- **API Gateway** (puerto 8080): Punto de entrada principal
- **Service Discovery** (puerto 8761): Registro y descubrimiento de servicios
- **Cloud Config** (puerto 9296): Gestión centralizada de configuración
- **Proxy Client** (puerto 8900): Cliente proxy para comunicación entre servicios

### Microservicios de Negocio

- **User Service** (puerto 8700): Gestión de usuarios
- **Product Service** (puerto 8500): Gestión de productos y categorías
- **Order Service** (puerto 8300): Gestión de carritos y órdenes
- **Payment Service** (puerto 8400): Procesamiento de pagos
- **Favourite Service** (puerto 8800): Gestión de favoritos
- **Shipping Service** (puerto 8600): Gestión de envíos

## 🚀 Ejecución de Pruebas

### Prerrequisitos

```bash
pip install -r requirements.txt
```

### Verificación de Conectividad

```bash
# Verificar que todos los servicios estén disponibles
python run_integration_tests.py --connectivity

# Verificar conectividad individual
python -c "from utils.api_utils import test_all_services_connectivity; test_all_services_connectivity()"
```

### Ejecución Completa

```bash
# Ejecutar todas las pruebas
python run_integration_tests.py

# Con reporte HTML
python run_integration_tests.py --html

# Con ejecución en paralelo
python run_integration_tests.py --parallel

# Modo verboso
python run_integration_tests.py --verbose
```

### Ejecución por Categorías

```bash
# Solo servicios de infraestructura
python run_integration_tests.py --service infrastructure

# Solo microservicios de negocio
python run_integration_tests.py --service business

# Atajos directos
python run_integration_tests.py --infrastructure
python run_integration_tests.py --business
```

### Ejecución por Servicio Individual

```bash
# API Gateway
python run_integration_tests.py --service api-gateway

# User Service
python run_integration_tests.py --service user-service

# Product Service
python run_integration_tests.py --service product-service

# Otros servicios disponibles:
# --service cloud-config
# --service service-discovery
# --service proxy-client
# --service order-service
# --service payment-service
# --service favourite-service
# --service shipping-service
```

### Opciones Avanzadas

```bash
# Solo pruebas de conectividad/health
python run_integration_tests.py --connectivity-only

# Detener en el primer fallo
python run_integration_tests.py --fail-fast

# Filtros por método específico
python run_integration_tests.py --method save
python run_integration_tests.py --method find
python run_integration_tests.py --method health

# URL personalizada del Gateway
python run_integration_tests.py --gateway-url http://localhost:9090

# Combinando opciones
python run_integration_tests.py --service user-service --method save --html --verbose --fail-fast
```

### Atajos Rápidos

```bash
# Verificación rápida de conectividad
python run_integration_tests.py --connectivity

# Pruebas de humo (solo health checks)
python run_integration_tests.py --smoke

# Verificar autenticación únicamente
python run_integration_tests.py --auth

# Solo infraestructura
python run_integration_tests.py --infrastructure

# Solo microservicios de negocio
python run_integration_tests.py --business
```

## 📁 Estructura de Archivos

```
integration/
├── config/
│   └── config.py                   # Configuración de URLs y servicios
├── utils/
│   └── api_utils.py                # Utilidades para peticiones HTTP
├── tests/
│   ├── test_api_gateway.py         # Pruebas del API Gateway
│   ├── test_cloud_config.py        # Pruebas del Cloud Config
│   ├── test_service_discovery.py   # Pruebas del Service Discovery
│   ├── test_proxy_client.py        # Pruebas del Proxy Client
│   ├── test_user_service.py        # Pruebas del User Service
│   ├── test_product_service.py     # Pruebas del Product Service
│   ├── test_order_service.py       # Pruebas del Order Service
│   ├── test_payment_service.py     # Pruebas del Payment Service
│   ├── test_favourite_service.py   # Pruebas del Favourite Service
│   └── test_shipping_service.py    # Pruebas del Shipping Service
├── conftest.py                     # Configuración de pytest
├── run_integration_tests.py        # Script principal de ejecución
└── README.md                       # Este archivo
```

## 🔧 Configuración

### Variables de Entorno

```bash
# URLs de servicios de infraestructura
export SERVICE_DISCOVERY_URL="http://localhost:8761"
export CLOUD_CONFIG_URL="http://localhost:9296"
export API_GATEWAY_URL="http://localhost:8080"
export PROXY_CLIENT_URL="http://localhost:8900"

# URLs de microservicios (automáticas vía Gateway)
export USER_SERVICE_URL="http://localhost:8700"
export PRODUCT_SERVICE_URL="http://localhost:8500"
export ORDER_SERVICE_URL="http://localhost:8300"
export PAYMENT_SERVICE_URL="http://localhost:8400"
export FAVOURITE_SERVICE_URL="http://localhost:8800"
export SHIPPING_SERVICE_URL="http://localhost:8600"
```

### Autenticación

Las pruebas de microservicios de negocio requieren autenticación JWT que se obtiene automáticamente usando las credenciales configuradas en `config/config.py`.

## 📊 Interpretación de Resultados

### Códigos de Estado Esperados

#### Servicios de Infraestructura

- `200`: Servicio funcionando correctamente
- `404`: Endpoints actuator no expuestos (normal en producción)

#### Microservicios de Negocio

- `200`: Operación exitosa
- `401/403`: Requerida autenticación (normal)
- `500`: Error interno del servicio

### Reportes HTML

Los reportes HTML incluyen:

- Resumen ejecutivo de todas las pruebas
- Detalles de cada prueba individual
- Logs de peticiones HTTP
- Tiempo de ejecución por prueba

## 🐛 Resolución de Problemas

### Servicios No Disponibles

```bash
# Verificar que los servicios estén ejecutándose
docker ps
# o
docker-compose ps

# Verificar puertos
netstat -an | grep LISTEN
```

### Problemas de Autenticación

```bash
# Resetear token y volver a autenticar
python -c "from utils.api_utils import reset_auth_token; reset_auth_token()"
```

### Timeouts de Conexión

Ajustar `REQUEST_TIMEOUT` en `config/config.py` si los servicios tardan en responder.

## 📈 Métricas y Monitoreo

Las pruebas validan:

- ✅ Conectividad de servicios
- ✅ Endpoints de salud/actuator
- ✅ Operaciones CRUD básicas
- ✅ Autenticación y autorización
- ✅ Formato de respuestas
- ✅ Códigos de estado HTTP

## 🔄 Integración Continua

Para uso en CI/CD:

```bash
# Ejecución silenciosa con reporte
python run_integration_tests.py --html --fail-fast --connectivity-only
```

## 📞 Soporte

Para reportar problemas o sugerir mejoras, consultar la documentación del proyecto principal.
