"""
Configuración para las pruebas de integración.
"""

import os

# URLs de servicios de infraestructura
SERVICE_DISCOVERY_URL = os.getenv("SERVICE_DISCOVERY_URL", "http://localhost:8761")
CLOUD_CONFIG_URL = os.getenv("CLOUD_CONFIG_URL", "http://localhost:9296")
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8222")
PROXY_CLIENT_URL = os.getenv("PROXY_CLIENT_URL", "http://localhost:8900")

# Configuración de servicios
SERVICES_CONFIG = {
    "service-discovery": {
        "url": SERVICE_DISCOVERY_URL,
        "requires_auth": False,
        "path_prefix": "",
    },
    "cloud-config": {
        "url": CLOUD_CONFIG_URL,
        "requires_auth": False,
        "path_prefix": "",
    },
    "api-gateway": {
        "url": API_GATEWAY_URL,
        "requires_auth": False,
        "path_prefix": "",
    },
    "proxy-client": {
        "url": PROXY_CLIENT_URL,
        "requires_auth": True,
        "path_prefix": "",
    },
    "user-service": {
        "url": f"{API_GATEWAY_URL}/user-service",
        "requires_auth": True,
        "path_prefix": "",
    },
    "product-service": {
        "url": f"{API_GATEWAY_URL}/product-service",
        "requires_auth": True,
        "path_prefix": "",
    },
    "order-service": {
        "url": f"{API_GATEWAY_URL}/order-service",
        "requires_auth": True,
        "path_prefix": "",
    },
    "payment-service": {
        "url": f"{API_GATEWAY_URL}/payment-service",
        "requires_auth": True,
        "path_prefix": "",
    },
    "favourite-service": {
        "url": f"{API_GATEWAY_URL}/favourite-service",
        "requires_auth": True,
        "path_prefix": "",
    },
    "shipping-service": {
        "url": f"{API_GATEWAY_URL}/shipping-service",
        "requires_auth": True,
        "path_prefix": "",
    },
}

# Configuración de autenticación
AUTH_ENDPOINT = f"{API_GATEWAY_URL}/app/api/authenticate"
JWT_TOKEN = None  # Se establecerá durante la ejecución de las pruebas

# Tiempo de espera para las solicitudes (en segundos)
REQUEST_TIMEOUT = 10

# Usuario de prueba para autenticación
TEST_USER = {
    "username": "selimhorri",
    "password": "12345",
}
