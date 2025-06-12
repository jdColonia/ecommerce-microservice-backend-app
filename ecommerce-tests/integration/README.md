# Pruebas End-to-End (E2E) - Microservicios E-Commerce

Este directorio contiene pruebas end-to-end (E2E) para la aplicación de microservicios de e-commerce. Estas pruebas validan flujos de negocio completos que atraviesan múltiples servicios, asegurando que el sistema funcione correctamente como un todo.

## 🏗️ Arquitectura y Enfoque

### Concepto de Pruebas E2E para Backend

A diferencia de las pruebas E2E tradicionales que involucran interfaces de usuario, estas pruebas se centran en validar **flujos de negocio completos** a través de las APIs REST de los microservicios. Simulan las operaciones que realizaría un frontend o cualquier cliente, verificando:

- ✅ **Integridad de los datos** a través de múltiples servicios
- ✅ **Correcta coordinación** entre microservicios
- ✅ **Flujos de usuario end-to-end** (registro → compra → pago → envío)
- ✅ **Consistencia** en el comportamiento del sistema
- ✅ **Happy Path scenarios** - casos de uso exitosos

## 📁 Estructura del Proyecto

```
e2e/
│
├── config/
│   └── config.py                  # Configuración de URLs y servicios
│
├── tests/
│   ├── test_user_service.py       # Gestión completa de usuarios
│   ├── test_product_service.py    # Catálogo y productos
│   ├── test_order_service.py      # Carritos y órdenes
│   ├── test_payment_service.py    # Procesamiento de pagos
│   ├── test_favourite_service.py  # Sistema de favoritos
│   ├── test_shipping_service.py   # Gestión de envíos
│   └── test_proxy_client.py       # Comunicación entre servicios
│
├── conftest.py                    # Configuración global de pytest
├── run_e2e_tests.py               # Script principal de ejecución
├── requirements.txt               # Dependencias Python
└── README.md                      # Esta documentación
```

## 🎯 Pruebas Implementadas

### **User Service** (5 pruebas E2E)

1. **Ciclo de vida completo de usuario**: Crear → Obtener → Actualizar → Eliminar
2. **Gestión de direcciones**: Usuario con múltiples direcciones
3. **Flujo de credenciales**: Crear usuario → Credenciales → Autenticación
4. **Tokens de verificación**: Gestión completa de tokens
5. **Múltiples usuarios**: Creación masiva y listado

### **Product Service** (5 pruebas E2E)

1. **Ciclo de vida de categoría**: Crear → Obtener → Actualizar → Listar
2. **Producto con categoría**: Categoría → Producto → Gestión completa
3. **Múltiples productos**: Varios productos en una categoría
4. **Gestión de inventario**: Stock → Precios → Reabastecimiento
5. **Operaciones en lote**: Múltiples categorías y productos

### **Order Service** (5 pruebas E2E)

1. **Ciclo de vida de carrito**: Crear → Obtener → Actualizar → Listar
2. **Orden desde carrito**: Carrito → Orden → Actualización
3. **Múltiples órdenes**: Gestión de varias órdenes simultáneas
4. **Cálculo de tarifas**: Precios → Descuentos → Impuestos
5. **Operaciones en lote**: Procesamiento masivo de órdenes

### **Payment Service** (5 pruebas E2E)

1. **Ciclo de vida de pago**: NOT_STARTED → IN_PROGRESS → COMPLETED
2. **Transiciones de estado**: Flujo completo de estados de pago
3. **Múltiples pagos**: Varios pagos para diferentes órdenes
4. **Manejo de fallos**: Fallo → Reintento → Éxito
5. **Procesamiento en lote**: Múltiples pagos simultáneos

### **Favourite Service** (5 pruebas E2E)

1. **Ciclo de vida de favorito**: Crear → Obtener → Actualizar → Listar
2. **Usuario con múltiples favoritos**: Un usuario marca varios productos
3. **Producto popular**: Múltiples usuarios marcan el mismo producto
4. **Gestión de timestamps**: Fechas y ordenamiento temporal
5. **Operaciones en lote**: Creación y gestión masiva de favoritos

### **Shipping Service** (5 pruebas E2E)

1. **Ciclo de vida de envío**: Crear → Obtener → Actualizar → Listar
2. **Múltiples productos por orden**: Varios items en un envío
3. **Referencias a productos/órdenes**: Relaciones entre entidades
4. **Gestión de cantidades**: Stock → Picking → Reabastecimiento
5. **Operaciones en lote**: Procesamiento masivo de envíos

### **Proxy Client** (5 pruebas E2E)

1. **Conectividad y salud**: Health checks y métricas
2. **Comunicación con User Service**: Routing y respuestas
3. **Comunicación con Product Service**: Diferentes tipos de contenido
4. **Routing múltiple**: Acceso a varios servicios via proxy
5. **Manejo de errores**: Resilencia y recuperación

## 🚀 Ejecución de Pruebas

### Prerrequisitos

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar URL del API Gateway (opcional)
export API_GATEWAY_URL="http://localhost:8222"
```

### Ejecución Completa

```bash
# Ejecutar todas las pruebas E2E
python run_e2e_tests.py

# Con reporte HTML detallado
python run_e2e_tests.py --html

# Con ejecución en paralelo
python run_e2e_tests.py --parallel

# Modo verboso con detalles
python run_e2e_tests.py --verbose
```

### Ejecución por Servicio

```bash
# User Service
python run_e2e_tests.py --service user-service

# Product Service
python run_e2e_tests.py --service product-service

# Order Service
python run_e2e_tests.py --service order-service

# Payment Service
python run_e2e_tests.py --service payment-service

# Favourite Service
python run_e2e_tests.py --service favourite-service

# Shipping Service
python run_e2e_tests.py --service shipping-service

# Proxy Client
python run_e2e_tests.py --service proxy-client
```

### Opciones Avanzadas

```bash
# Detener en el primer fallo
python run_e2e_tests.py --fail-fast

# Solo pruebas de conectividad
python run_e2e_tests.py --connectivity-only

# Timeout personalizado (default: 300s)
python run_e2e_tests.py --timeout 600

# URL personalizada del Gateway
python run_e2e_tests.py --gateway-url http://localhost:9090

# Combinando opciones
python run_e2e_tests.py --service user-service --html --verbose --fail-fast
```

### Atajos Rápidos

```bash
# Pruebas de humo rápidas
python run_e2e_tests.py --smoke

# Reporte de cobertura
python run_e2e_tests.py --coverage

# Servicio específico con atajo
python run_e2e_tests.py --service=product-service
```

## 🔧 Configuración

### Variables de Entorno

```bash
# URL del API Gateway
export API_GATEWAY_URL="http://localhost:8222"

# Configuración de timeouts
export REQUEST_TIMEOUT=15

# Configuración de autenticación
export TEST_USERNAME="selimhorri"
export TEST_PASSWORD="12345"
```

### Autenticación

Las pruebas E2E utilizan autenticación JWT que se obtiene automáticamente del endpoint `/app/api/authenticate` usando las credenciales configuradas.

## 📊 Características de las Pruebas

### **Happy Path Focus**

- ✅ Todas las pruebas siguen el **camino feliz** (escenarios exitosos)
- ✅ No incluyen casos de error o validaciones negativas
- ✅ Se enfocan en verificar funcionalidad correcta

### **Limpieza Automática**

- 🧹 Cada prueba limpia sus datos automáticamente
- 🧹 Sistema de cleanup inteligente por dependencias
- 🧹 Estado limpio después de cada ejecución

### **Datos Únicos**

- 🔢 Generación automática de IDs únicos
- 🔢 Prefijos distintivos para datos de prueba
- 🔢 Evita conflictos entre ejecuciones

### **Resilencia**

- 🔄 Reintentos automáticos en fallos de red
- 🔄 Timeouts configurables
- 🔄 Manejo elegante de errores temporales

## 📈 Interpretación de Resultados

### Códigos de Estado Esperados

- **200**: Operación exitosa
- **201**: Recurso creado exitosamente
- **401/403**: Autenticación requerida (esperado)
- **404**: Recurso no encontrado (en algunos casos esperado)

### Reportes HTML

Los reportes incluyen:

- 📊 Resumen ejecutivo de todas las pruebas
- 📝 Detalles de cada flujo E2E
- 🕐 Tiempos de ejecución por prueba
- 🔍 Logs detallados de peticiones HTTP
- 📈 Métricas de éxito por servicio

## 🐛 Resolución de Problemas

### Fallas de Conectividad

```bash
# Verificar API Gateway
curl http://localhost:8222/actuator/health

# Verificar servicios
docker-compose ps
```

### Problemas de Autenticación

```bash
# Verificar credenciales
curl -X POST http://localhost:8222/app/api/authenticate \
  -H "Content-Type: application/json" \
  -d '{"username":"selimhorri","password":"12345"}'
```

### Timeouts de Pruebas

```bash
# Aumentar timeout para entornos lentos
python run_e2e_tests.py --timeout 600

# Verificar latencia de red
ping localhost
```

### Limpieza Manual

```bash
# Si quedan datos residuales, ejecutar limpieza manual
python -c "
from conftest import cleanup_test_data
resources = {'users': [], 'products': [], 'orders': []}
cleanup_test_data(resources)
"
```

## 🔄 Integración Continua

### Para Pipelines CI/CD

```bash
# Ejecución silenciosa con reporte
python run_e2e_tests.py --html --fail-fast --timeout 300

# Solo verificación de conectividad
python run_e2e_tests.py --connectivity-only --timeout 60

# Ejecución en paralelo para velocidad
python run_e2e_tests.py --parallel --html
```

### Variables para CI

```yaml
# .github/workflows/e2e-tests.yml
env:
  API_GATEWAY_URL: 'http://api-gateway:8222'
  REQUEST_TIMEOUT: '30'
  E2E_CLEANUP: 'true'
```

## 🎯 Casos de Uso Validados

### **Flujo de E-Commerce Completo**

1. **Registro de Usuario** → Crear usuario con credenciales
2. **Navegación de Catálogo** → Listar categorías y productos
3. **Gestión de Favoritos** → Marcar productos favoritos
4. **Proceso de Compra** → Carrito → Orden → Pago
5. **Gestión de Envío** → Crear items de envío con cantidades

### **Operaciones Administrativas**

1. **Gestión de Inventario** → Productos → Stock → Precios
2. **Procesamiento de Órdenes** → Múltiples órdenes simultáneas
3. **Gestión de Pagos** → Estados → Fallos → Reintentos
4. **Análisis de Favoritos** → Productos populares → Usuarios activos
5. **Logística de Envíos** → Consolidación → Tracking → Cantidades

### **Operaciones del Sistema**

1. **Comunicación entre Servicios** → Proxy → Routing → Resilencia
2. **Autenticación y Autorización** → JWT → Permisos → Sesiones
3. **Consistencia de Datos** → Referencias → Integridad → Cleanup
4. **Rendimiento** → Operaciones en lote → Concurrencia → Timeouts

## 📋 Checklist de Validación

### Antes de Ejecutar

- [ ] API Gateway accesible
- [ ] Servicios de backend ejecutándose
- [ ] Credenciales de prueba configuradas
- [ ] Base de datos limpia y accesible

### Durante la Ejecución

- [ ] Autenticación JWT funcionando
- [ ] Servicios respondiendo correctamente
- [ ] Datos únicos generándose sin conflictos
- [ ] Cleanup automático funcionando

### Después de la Ejecución

- [ ] Todas las pruebas pasaron (Happy Path)
- [ ] Datos de prueba limpiados automáticamente
- [ ] Reportes HTML generados correctamente
- [ ] No quedan recursos residuales

## 🏆 Métricas de Éxito

### **Cobertura de Servicios**

- ✅ 7 microservicios cubiertos
- ✅ 35 pruebas E2E totales (5 por servicio)
- ✅ 100% de operaciones CRUD validadas
- ✅ Flujos de negocio completos verificados

### **Calidad de Pruebas**

- ✅ Happy Path enfocado
- ✅ Datos únicos sin conflictos
- ✅ Cleanup automático 100% efectivo
- ✅ Resilencia ante fallos temporales

### **Rendimiento**

- ⚡ Ejecución completa < 10 minutos
- ⚡ Ejecución por servicio < 2 minutos
- ⚡ Ejecución en paralelo disponible
- ⚡ Timeouts configurables

## 🔮 Extensiones Futuras

### **Próximas Características**

- 🚀 Pruebas de carga E2E con Locust
- 🚀 Validación de contratos API (Pact)
- 🚀 Pruebas de caos (Chaos Engineering)
- 🚀 Monitoreo de métricas de negocio

### **Integración con Herramientas**

- 📊 Dashboards de métricas en tiempo real
- 📊 Alertas automáticas en fallos
- 📊 Integración con sistemas de monitoreo
- 📊 Análisis de tendencias de rendimiento

## 📞 Soporte y Contribución

### **Reportar Problemas**

- 🐛 Usar GitHub Issues para bugs
- 🐛 Incluir logs completos y configuración
- 🐛 Especificar versión de servicios usada

### **Contribuir Nuevas Pruebas**

- 🤝 Seguir patrón de Happy Path
- 🤝 Incluir cleanup automático
- 🤝 Documentar casos de uso validados
- 🤝 Mantener consistencia con pruebas existentes

### **Mejores Prácticas**

- ✨ Usar datos únicos con `generate_unique_id()`
- ✨ Implementar cleanup en `cleanup_resources`
- ✨ Verificar códigos de estado apropiados
- ✨ Mantener pruebas independientes y determinísticas

---

## 🎉 Conclusión

Las pruebas E2E de este proyecto validan **35 escenarios críticos** de negocio a través de **7 microservicios**, asegurando que el sistema de e-commerce funcione correctamente de extremo a extremo.
