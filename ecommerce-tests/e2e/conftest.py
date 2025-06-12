"""
Configuración global para pruebas E2E.
"""

import pytest
import logging
import os
from utils.api_client import ApiClient
from config.config import LOG_LEVEL, LOG_FILE

# Configurar logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

@pytest.fixture(scope="session")
def api_client():
    """
    Fixture que proporciona un cliente API para todas las pruebas.
    
    Returns:
        ApiClient: Cliente API
    """
    client = ApiClient()
    
    # Verificar que el API Gateway esté disponible
    health_check = client.verify_service_health()
    if not health_check:
        logging.warning("No se pudo verificar la salud del API Gateway. Las pruebas podrían fallar.")
    
    return client
