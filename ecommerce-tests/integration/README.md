# Pruebas de Integración - Microservicios E-Commerce

Este directorio contiene pruebas de integración para la aplicación de microservicios de e-commerce. Las pruebas validan que los servicios interactúen correctamente entre sí a través del API Gateway.

## Estructura del Proyecto

```
integration-tests/
│
├── config/             # Configuración para las pruebas
│   └── config.py       # Configuración global
│
├── utils/              # Utilidades para las pruebas
│   └── api_utils.py    # Funciones de ayuda para interactuar con la API
│
├── tests/              # Archivos de prueba
│   ├── test_user_service.py       # Pruebas para el servicio de usuarios
│   ├── test_product_service.py    # Pruebas para el servicio de productos
│   └── test_order_service.py      # Pruebas para el servicio de órdenes
│
├── conftest.py         # Configuración global para pytest
└── run_tests.py        # Script para ejecutar las pruebas
```

## Requisitos

- Python 3.8 o superior
- Entorno virtual (venv)
- Dependencias: pytest, requests, pytest-html, pytest-xdist

## Configuración

1. Activar el entorno virtual:

```bash
cd integration-tests
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Unix/Linux
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar la URL del API Gateway en `config/config.py`:

```python
# URL base del API Gateway
BASE_URL = "https://api-gateway.your-cluster.com"  # Reemplazar con la URL real
```

## Ejecución de Pruebas

### Ejecutar todas las pruebas

```bash
python run_tests.py
```

### Ejecutar pruebas con salida detallada

```bash
python run_tests.py --verbose
```

### Generar reporte HTML

```bash
python run_tests.py --html
```

### Ejecutar pruebas en paralelo

```bash
python run_tests.py --parallel
```

### Ejecutar pruebas para un servicio específico

```bash
python run_tests.py --service user
python run_tests.py --service product
python run_tests.py --service order
```

## Notas Adicionales

- Las pruebas se ejecutan contra el API Gateway, que enruta las solicitudes a los servicios correspondientes.
- Todas las pruebas crean sus propios datos de prueba y realizan limpieza después de la ejecución.
- Se utiliza un token JWT para autenticación, obtenido en el inicio de la sesión de pruebas.

## Troubleshooting

1. **Error de conexión**: Verifica que el API Gateway esté accesible desde el entorno de pruebas.
2. **Error de autenticación**: Asegúrate de que las credenciales en `config.py` sean válidas.
3. **Fallos en las pruebas**: Revisa los logs del servicio específico para obtener más detalles.

## Extensión

Para añadir pruebas para más servicios, crea un nuevo archivo en el directorio `tests/` siguiendo el patrón `test_[servicio]_service.py` e implementa las pruebas correspondientes.
