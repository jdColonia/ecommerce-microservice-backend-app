"""
Configuración para las pruebas e2e.
"""

import os

# URLs de servicios de infraestructura
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8222")

# Configuración de servicios
SERVICES_CONFIG = {
    "api-gateway": {
        "url": API_GATEWAY_URL,
        "requires_auth": False,
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
    "proxy-client": {
        "url": f"{API_GATEWAY_URL}/proxy-client",
        "requires_auth": True,
        "path_prefix": "",
    },
}

# Configuración de autenticación
AUTH_ENDPOINT = f"{API_GATEWAY_URL}/app/api/authenticate"

# Tiempo de espera para las solicitudes (en segundos)
REQUEST_TIMEOUT = 15

# Usuario de prueba para autenticación
TEST_USER = {
    "username": "selimhorri",
    "password": "12345",
}

# Configuración específica para E2E
E2E_CONFIG = {
    "cleanup_after_test": True,
    "max_retries": 3,
    "retry_delay": 2,
    "test_data_prefix": "e2e_test_",
}
