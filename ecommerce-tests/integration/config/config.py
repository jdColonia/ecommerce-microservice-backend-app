"""
Configuración para las pruebas de integración.
"""

# URL base del API Gateway
BASE_URL = "https://api-gateway.your-cluster.com"  # Reemplazar con la URL real de tu API Gateway

# Configuración de autenticación
AUTH_ENDPOINT = f"{BASE_URL}/api/authenticate"
JWT_TOKEN = None  # Se establecerá durante la ejecución de las pruebas

# Tiempo de espera para las solicitudes (en segundos)
REQUEST_TIMEOUT = 10

# Usuario de prueba
TEST_USER = {
    "username": "test_user",
    "password": "test_password",
    "email": "test@example.com"
}

# Producto de prueba
TEST_PRODUCT = {
    "name": "Producto de Prueba",
    "description": "Este es un producto para pruebas",
    "price": 99.99,
    "stock": 100,
    "categoryId": 1
}

# Dirección de prueba
TEST_ADDRESS = {
    "street": "Calle de Prueba",
    "number": "123",
    "city": "Ciudad de Prueba",
    "state": "Estado de Prueba",
    "country": "País de Prueba",
    "zipCode": "12345"
}

# Orden de prueba
TEST_ORDER = {
    "userId": 1,
    "totalAmount": 99.99,
    "status": "PENDING"
}
