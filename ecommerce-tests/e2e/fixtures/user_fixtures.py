"""
Fixtures para pruebas E2E relacionadas con usuarios.
"""

import pytest
import logging
from typing import Dict, Any, Optional
from utils.api_client import ApiClient
from utils.data_generator import generate_user_data, generate_address_data
from flows.user_management import UserManagementFlow

logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def test_user(api_client: ApiClient) -> Dict[str, Any]:
    """
    Fixture que crea un usuario de prueba y lo elimina al finalizar.
    
    Args:
        api_client (ApiClient): Cliente API
        
    Returns:
        dict: Datos del usuario creado
    """
    user_flow = UserManagementFlow(api_client)
    user_data = generate_user_data()
    
    # Crear usuario
    user = user_flow.register_user(user_data)
    user_id = user.get("id")
    
    # Añadir contraseña a los datos del usuario para poder autenticar
    user["password"] = user_data["password"]
    
    logger.info(f"Usuario de prueba creado: {user_id}")
    
    yield user
    
    # Limpiar: eliminar usuario
    logger.info(f"Eliminando usuario de prueba: {user_id}")
    user_flow.delete_user(user_id)

@pytest.fixture(scope="function")
def test_user_with_address(api_client: ApiClient, test_user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fixture que crea un usuario con dirección.
    
    Args:
        api_client (ApiClient): Cliente API
        test_user (dict): Usuario de prueba
        
    Returns:
        dict: Datos del usuario con dirección
    """
    user_flow = UserManagementFlow(api_client)
    user_id = test_user.get("id")
    
    # Crear dirección
    address_data = generate_address_data()
    address = user_flow.add_user_address(user_id, address_data)
    
    # Añadir dirección a los datos del usuario
    test_user["address"] = address
    
    logger.info(f"Dirección creada para usuario {user_id}: {address.get('id')}")
    
    return test_user

@pytest.fixture(scope="function")
def authenticated_api_client(api_client: ApiClient, test_user: Dict[str, Any]) -> ApiClient:
    """
    Fixture que devuelve un cliente API autenticado.
    
    Args:
        api_client (ApiClient): Cliente API
        test_user (dict): Usuario de prueba
        
    Returns:
        ApiClient: Cliente API autenticado
    """
    username = test_user.get("username")
    password = test_user.get("password")
    
    success = api_client.authenticate(username, password)
    assert success, f"No se pudo autenticar con el usuario {username}"
    
    logger.info(f"Cliente API autenticado con usuario {username}")
    
    return api_client
