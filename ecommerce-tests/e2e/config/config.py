"""
Configuración para las pruebas E2E.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

# URL base del API Gateway
API_BASE_URL = os.getenv('API_BASE_URL', 'https://api-gateway.your-cluster.com')

# Timeouts (en segundos)
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 10))
WAIT_TIMEOUT = int(os.getenv('WAIT_TIMEOUT', 30))

# Credenciales para pruebas
TEST_USER = {
    'username': os.getenv('TEST_USERNAME', 'e2e_test_user'),
    'password': os.getenv('TEST_PASSWORD', 'Test@1234'),
    'email': os.getenv('TEST_EMAIL', 'e2e_test_user@example.com')
}

# Producto de prueba por defecto (para casos donde se necesita crear un producto)
TEST_PRODUCT = {
    'name': 'Producto E2E Test',
    'description': 'Este es un producto de prueba para E2E',
    'price': 99.99,
    'stock': 100,
    'categoryId': 1
}

# Dirección de prueba por defecto
TEST_ADDRESS = {
    'street': 'Calle de Prueba E2E',
    'number': '123',
    'city': 'Ciudad de Prueba',
    'state': 'Estado de Prueba',
    'country': 'País de Prueba',
    'zipCode': '12345'
}

# Datos de tarjeta de crédito para pruebas
TEST_CREDIT_CARD = {
    'number': '4111111111111111',
    'expiryMonth': '12',
    'expiryYear': '2030',
    'cvv': '123'
}

# Configuración de logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'e2e_tests.log')

# Configuración de reintentos
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
RETRY_DELAY = int(os.getenv('RETRY_DELAY', 2))  # segundos
