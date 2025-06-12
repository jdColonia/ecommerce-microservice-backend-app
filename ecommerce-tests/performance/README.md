# Pruebas de Rendimiento - Microservicios E-Commerce

Este directorio contiene pruebas de rendimiento para la aplicación de microservicios de e-commerce utilizando [Locust](https://locust.io/), una herramienta de pruebas de carga distribuida escrita en Python.

## Estructura del Proyecto

```
performance-tests/
│
├── config/             # Configuración para las pruebas
│   └── settings.py     # Configuración global
│
├── data/               # Datos para las pruebas
│
├── locustfiles/        # Clases de usuario para Locust
│   ├── base_user.py    # Clase base para usuarios
│   ├── browse_user.py  # Usuarios que solo navegan
│   ├── buyer_user.py   # Usuarios que realizan compras
│   └── admin_user.py   # Usuarios administradores
│
├── reports/            # Informes generados (creado automáticamente)
│
├── scenarios/          # Definiciones de escenarios personalizados
│
├── locustfile.py       # Archivo principal de Locust
├── run_performance_tests.py  # Script para ejecutar escenarios de prueba
└── requirements.txt    # Dependencias
```

## Tipos de Usuarios

Las pruebas de rendimiento simulan diferentes tipos de usuarios con comportamientos distintos:

1. **Browse User (70%)**: Usuario que solo navega por productos y categorías sin autenticación.
2. **Buyer User (20%)**: Usuario que realiza compras completas, desde añadir al carrito hasta el pago.
3. **Admin User (10%)**: Usuario administrador que gestiona productos, categorías y órdenes.

## Escenarios de Prueba

El script `run_performance_tests.py` permite ejecutar diferentes escenarios de carga:

1. **Light**: 10 usuarios, tasa de 5/s, duración de 1 minuto
2. **Medium**: 50 usuarios, tasa de 10/s, duración de 3 minutos
3. **Heavy**: 100 usuarios, tasa de 20/s, duración de 5 minutos
4. **Spike**: 200 usuarios, tasa de 50/s, duración de 2 minutos
5. **Endurance**: 30 usuarios, tasa de 5/s, duración de 10 minutos

## Requisitos

- Python 3.8 o superior
- Entorno virtual (venv)
- Dependencias: locust, python-dotenv, faker, matplotlib, pandas

## Configuración

1. Activar el entorno virtual:

```bash
cd performance-tests
venv\Scripts\activate  # En Windows
source venv/bin/activate  # En Unix/Linux
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar la URL del API Gateway y otras variables en un archivo `.env`:

```
API_BASE_URL=https://api-gateway.your-cluster.com
LOAD_ADMIN_USERNAME=admin
LOAD_ADMIN_PASSWORD=admin123
LOAD_USER_USERNAME=testuser
LOAD_USER_PASSWORD=test123
```

## Ejecución de Pruebas

### Ejecutar un escenario específico

```bash
python run_performance_tests.py --scenario light
python run_performance_tests.py --scenario medium
python run_performance_tests.py --scenario heavy
python run_performance_tests.py --scenario spike
python run_performance_tests.py --scenario endurance
```

### Ejecutar todos los escenarios

```bash
python run_performance_tests.py --scenario all
```

### Ejecutar con interfaz gráfica

```bash
python run_performance_tests.py --gui
```

### Especificar host

```bash
python run_performance_tests.py --host https://api-gateway.your-cluster.com
```

## Ejecutar Locust directamente

También puedes ejecutar Locust directamente con su interfaz web:

```bash
locust -f locustfile.py
```

O en modo headless:

```bash
locust -f locustfile.py --headless --users 50 --spawn-rate 10 --run-time 3m --host https://api-gateway.your-cluster.com
```

## Informes

Los informes se guardan en el directorio `reports/[escenario]/[timestamp]/`:

- `report.html`: Informe HTML con gráficas y estadísticas
- `stats_*.csv`: Datos en formato CSV para análisis adicional
- `config.json`: Configuración utilizada para la prueba
- `results.json`: Resultados de la ejecución
- `stdout.log` y `stderr.log`: Salida de Locust

## Análisis de Resultados

Las métricas clave a analizar son:

1. **Tiempo de respuesta (ms)**: Promedio, mediana, percentiles 95 y 99
2. **Throughput (RPS)**: Peticiones por segundo que el sistema puede manejar
3. **Tasa de error (%)**: Porcentaje de peticiones fallidas
4. **Usuarios concurrentes**: Número máximo de usuarios simultáneos soportados

## Troubleshooting

1. **Error de conexión**: Verifica que el API Gateway esté accesible desde el entorno de pruebas.
2. **Error de autenticación**: Asegúrate de que las credenciales en `settings.py` sean válidas.
3. **Error de memoria**: Reduce el número de usuarios o distribuye la carga en múltiples workers.
