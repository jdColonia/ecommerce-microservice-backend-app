"""
Configuración para pruebas de rendimiento con Locust.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# URL base del API Gateway
HOST = os.getenv("API_BASE_URL", "https://api-gateway.your-cluster.com")

# Credenciales para pruebas de carga
ADMIN_USERNAME = os.getenv("LOAD_ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("LOAD_ADMIN_PASSWORD", "admin123")

# Usuario normal para pruebas
USER_USERNAME = os.getenv("LOAD_USER_USERNAME", "testuser")
USER_PASSWORD = os.getenv("LOAD_USER_PASSWORD", "test123")

# Configuración de generación de carga
MIN_WAIT = int(os.getenv("MIN_WAIT", 1000))  # Tiempo mínimo entre peticiones (ms)
MAX_WAIT = int(os.getenv("MAX_WAIT", 5000))  # Tiempo máximo entre peticiones (ms)

# Proporciones de usuarios (%)
BROWSE_USER_WEIGHT = int(os.getenv("BROWSE_USER_WEIGHT", 70))
BUYER_USER_WEIGHT = int(os.getenv("BUYER_USER_WEIGHT", 20))
ADMIN_USER_WEIGHT = int(os.getenv("ADMIN_USER_WEIGHT", 10))

# Configuración de tiempos de espera y reintentos
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))  # segundos
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))

# Endpoints principales
ENDPOINTS = {
    "authentication": "/api/authenticate",
    "users": "/api/users",
    "products": "/api/products",
    "categories": "/api/categories",
    "orders": "/api/orders",
    "carts": "/api/carts",
    "payments": "/api/payments",
    "shipping": "/api/shippings",
    "favorites": "/api/favourites"
}

# Perfiles de usuario para pruebas
USER_PROFILES = {
    "browser": {
        "description": "Usuario que solo navega por productos y categorías",
        "endpoints": ["products", "categories", "favorites"],
        "auth_required": False
    },
    "buyer": {
        "description": "Usuario que compra productos",
        "endpoints": ["products", "categories", "carts", "orders", "payments", "shipping"],
        "auth_required": True
    },
    "admin": {
        "description": "Usuario administrador que gestiona catálogo y usuarios",
        "endpoints": ["users", "products", "categories", "orders"],
        "auth_required": True
    }
}
