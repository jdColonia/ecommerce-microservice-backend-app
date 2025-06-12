"""
Prueba E2E del ciclo de vida completo de un usuario.
"""

import pytest
import logging
from utils.api_client import ApiClient
from utils.assertions import assert_status_code, assert_contains_keys, assert_entity_exists, assert_entity_deleted
from utils.data_generator import generate_user_data, generate_address_data
from flows.user_management import UserManagementFlow

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def user_flow(api_client):
    """Fixture para el flujo de gestión de usuarios."""
    return UserManagementFlow(api_client)

def test_user_registration_and_authentication(api_client, user_flow):
    """
    Prueba E2E: registro de usuario y autenticación.
    
    Este test verifica que un usuario pueda:
    1. Registrarse en el sistema
    2. Autenticarse con sus credenciales
    """
    logger.info("Iniciando prueba de registro y autenticación de usuario")
    
    # Generar datos de usuario
    user_data = generate_user_data()
    
    # Registrar usuario
    user = user_flow.register_user(user_data)
    user_id = user.get("id")
    
    try:
        # Verificar que el usuario se haya creado correctamente
        assert_contains_keys(user, ["id", "username", "email"])
        assert user.get("username") == user_data.get("username"), "El nombre de usuario no coincide"
        assert user.get("email") == user_data.get("email"), "El email no coincide"
        
        # Verificar que el usuario existe en el sistema
        get_response = api_client.request("GET", f"/api/users/{user_id}")
        assert_status_code(get_response, 200)
        
        # Autenticar usuario
        auth_success = api_client.authenticate(user_data.get("username"), user_data.get("password"))
        assert auth_success, "La autenticación falló"
        
        logger.info("Prueba de registro y autenticación finalizada con éxito")
    
    finally:
        # Limpiar: eliminar usuario
        logger.info(f"Eliminando usuario de prueba: {user_id}")
        user_flow.delete_user(user_id)

def test_complete_user_lifecycle(api_client, user_flow):
    """
    Prueba E2E: ciclo de vida completo de un usuario.
    
    Este test verifica el flujo completo de un usuario:
    1. Registro
    2. Añadir dirección
    3. Actualizar perfil
    4. Eliminar cuenta
    """
    logger.info("Iniciando prueba de ciclo de vida completo de usuario")
    
    # Generar datos
    user_data = generate_user_data()
    address_data = generate_address_data()
    
    # 1. Registrar usuario
    user = user_flow.register_user(user_data)
    user_id = user.get("id")
    
    try:
        # Verificar registro
        assert user.get("id") is not None, "El usuario no tiene ID"
        assert user.get("username") == user_data.get("username"), "El nombre de usuario no coincide"
        
        # 2. Añadir dirección
        address = user_flow.add_user_address(user_id, address_data)
        address_id = address.get("id")
        
        # Verificar dirección
        assert address.get("id") is not None, "La dirección no tiene ID"
        assert address.get("street") == address_data.get("street"), "La calle no coincide"
        
        # 3. Actualizar perfil
        new_email = f"updated_{user_data.get('email')}"
        updated_user = user_flow.update_user_profile(user_id, {"email": new_email})
        
        # Verificar actualización
        assert updated_user.get("email") == new_email, "El email no se actualizó correctamente"
        
        # Verificar que los cambios persisten
        get_response = api_client.request("GET", f"/api/users/{user_id}")
        assert_status_code(get_response, 200)
        assert get_response.json().get("email") == new_email, "El email no se guardó correctamente"
        
        # 4. Eliminar usuario
        deleted = user_flow.delete_user(user_id)
        assert deleted, "No se pudo eliminar el usuario"
        
        # Verificar eliminación
        get_deleted_response = api_client.request("GET", f"/api/users/{user_id}")
        assert get_deleted_response.status_code == 404, "El usuario no se eliminó correctamente"
        
        logger.info("Prueba de ciclo de vida completo de usuario finalizada con éxito")
    
    except Exception as e:
        logger.error(f"Error en prueba de ciclo de vida de usuario: {str(e)}")
        # Asegurar limpieza en caso de error
        user_flow.delete_user(user_id)
        raise

def test_user_address_management(api_client, user_flow):
    """
    Prueba E2E: gestión de direcciones de usuario.
    
    Este test verifica que un usuario pueda:
    1. Añadir una dirección
    2. Obtener sus direcciones
    """
    logger.info("Iniciando prueba de gestión de direcciones")
    
    # Crear usuario para la prueba
    user = user_flow.register_user()
    user_id = user.get("id")
    
    try:
        # Añadir dirección
        address_data = generate_address_data()
        address = user_flow.add_user_address(user_id, address_data)
        address_id = address.get("id")
        
        # Verificar dirección
        assert_contains_keys(address, ["id", "street", "city", "country"])
        
        # Obtener dirección
        get_response = api_client.request("GET", f"/api/addresses/{address_id}")
        assert_status_code(get_response, 200)
        
        retrieved_address = get_response.json()
        assert retrieved_address.get("street") == address_data.get("street"), "La dirección no coincide"
        
        # Obtener todas las direcciones del usuario
        # Suponiendo que existe un endpoint para filtrar por usuario
        all_addresses_response = api_client.request("GET", "/api/addresses", params={"userId": user_id})
        assert_status_code(all_addresses_response, 200)
        
        addresses = all_addresses_response.json()
        assert isinstance(addresses, list), "Se esperaba una lista de direcciones"
        assert len(addresses) >= 1, "No se encontraron direcciones para el usuario"
        
        # Verificar que la dirección está en la lista
        address_found = False
        for addr in addresses:
            if addr.get("id") == address_id:
                address_found = True
                break
        
        assert address_found, f"La dirección {address_id} no se encontró en la lista de direcciones del usuario"
        
        logger.info("Prueba de gestión de direcciones finalizada con éxito")
    
    finally:
        # Limpiar: eliminar usuario
        logger.info(f"Eliminando usuario de prueba: {user_id}")
        user_flow.delete_user(user_id)
