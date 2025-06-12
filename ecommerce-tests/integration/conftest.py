"""
Archivo de inicio para las pruebas de integración.
"""

import pytest
from config.config import JWT_TOKEN
from utils.api_utils import get_auth_token

@pytest.fixture(scope="session", autouse=True)
def setup_auth_token():
    """
    Configura un token JWT para todas las pruebas.
    """
    global JWT_TOKEN
    JWT_TOKEN = get_auth_token()
    return JWT_TOKEN
