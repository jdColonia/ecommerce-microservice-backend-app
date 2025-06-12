# Pruebas End-to-End (E2E) - Microservicios E-Commerce

Este directorio contiene pruebas end-to-end (E2E) para la aplicación de microservicios de e-commerce. Estas pruebas validan flujos de negocio completos que atraviesan múltiples servicios, asegurando que el sistema funcione correctamente como un todo.

## Estructura del Proyecto

```
e2e-tests/
│
├── config/             # Configuración para las pruebas
│   └── config.py       # Configuración global
│
├── fixtures/           # Fixtures para configurar el estado inicial
│   ├── product_fixtures.py  # Fixtures relacionados con productos
│   └── user_fixtures.py     # Fixtures relacionados con usuarios
│
├── flows/              # Flujos de negocio
│   ├── checkout_flow.py     # Flujo de compra
│   ├── product_catalog.py   # Gestión de catálogo
│   └── user_management.py   # Gestión de usuarios
│
├── scenarios/          # Escenarios de prueba E2E
│   ├── test_complete_purchase.py     # Prueba de flujo de compra
│   ├── test_inventory_management.py  # Prueba de gestión de inventario
│   └── test_user_lifecycle.py        # Prueba de ciclo de vida de usuario
│
├── utils/              # Utilidades para las pruebas
│   ├── api_client.py        # Cliente para interactuar con la API
│   ├── assertions.py        # Funciones de aserción personalizadas
│   └── data_generator.py    # Generador de datos de prueba
│
├── conftest.py         # Configuración global para pytest
├── run_e2e_tests.py    # Script para ejecutar las pruebas
└── requirements.txt    # Dependencias
```

## Concepto de Pruebas E2E para Backend

A diferencia de las pruebas E2E tradicionales que involucran interfaces de usuario, estas pruebas se centran en validar flujos de negocio completos a través de las APIs REST de los microservicios. Simulan las operaciones que realizaría un frontend o cualquier cliente, verificando la integridad de los datos y la correcta coordinación entre servicios.

## Requisitos

- Python 3.8 o superior
- Entorno virtual (venv)
- Dependencias: pytest, requests, pytest-html, pytest-vcr, pytest-asyncio, etc.

## Configuración

1. Activar el entorno virtual:

```bash
cd e2e-tests
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Unix/Linux
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar la URL del API Gateway en `.env` o `config/config.py`:

```
API_BASE_URL=https://api-gateway.your-cluster.com
```

## Ejecución de Pruebas

### Ejecutar todas las pruebas E2E

```bash
python run_e2e_tests.py
```

### Ejecutar un escenario específico

```bash
python run_e2e_tests.py --scenario complete_purchase
python run_e2e_tests.py --scenario user_lifecycle
python run_e2e_tests.py --scenario inventory_management
```

### Opciones adicionales

```bash
# Salida detallada
python run_e2e_tests.py --verbose

# Generar reporte HTML
python run_e2e_tests.py --html

# Detener en el primer fallo
python run_e2e_tests.py --failfast

# Grabar las peticiones para depuración
python run_e2e_tests.py --record

# Configurar nivel de logging
python run_e2e_tests.py --log-level DEBUG
```

## Flujos Implementados

1. **Checkout Flow**: Simula el proceso completo de compra, desde añadir productos al carrito hasta procesar el pago y crear el envío.

2. **User Management**: Gestión del ciclo de vida del usuario, incluyendo registro, actualización de perfil, gestión de direcciones y eliminación.

3. **Product Catalog**: Gestión del catálogo de productos, incluyendo creación, actualización, gestión de inventario y categorías.

## Escenarios de Prueba

1. **Complete Purchase**: Valida el flujo completo de compra de un producto.

2. **User Lifecycle**: Verifica el ciclo de vida completo de un usuario en el sistema.

3. **Inventory Management**: Prueba la gestión de inventario, categorías y favoritos.

## Notas Adicionales

- Las pruebas crean y limpian sus propios datos, dejando el sistema en su estado original después de cada ejecución.
- Se utiliza autenticación mediante JWT para acceder a los endpoints protegidos.
- Los tiempos de espera y reintentos están configurados para adaptarse a la latencia en entornos cloud.

## Troubleshooting

1. **Error de conexión**: Verifica que el API Gateway esté accesible desde el entorno de pruebas.
2. **Error de autenticación**: Asegúrate de que las credenciales en `config.py` sean válidas.
3. **Fallos intermitentes**: Aumenta los tiempos de espera y reintentos en `config.py`.
4. **Fallos en limpieza**: Revisa si quedaron datos residuales que puedan afectar pruebas futuras.
