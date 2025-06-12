"""
Pruebas de integración para el servicio de usuarios.
"""

import pytest
import uuid
from utils.api_utils import make_request, validate_response_schema
from config.config import TEST_USER

# Esquema esperado para un usuario
USER_SCHEMA = {
    "id": int,
    "username": str,
    "email": str
}

class TestUserService:
    """
    Pruebas para el servicio de usuarios.
    """
    
    @pytest.fixture
    def create_test_user(self):
        """
        Fixture para crear un usuario de prueba.
        """
        # Generamos un nombre de usuario único para evitar conflictos
        unique_username = f"test_user_{uuid.uuid4().hex[:8]}"
        unique_email = f"{unique_username}@example.com"
        
        user_data = {
            "username": unique_username,
            "email": unique_email,
            "password": "Test@1234"
        }
        
        # Creamos el usuario
        response = make_request('POST', '/api/users', data=user_data)
        
        # Verificamos que se haya creado correctamente
        assert response.status_code == 201, f"Error al crear usuario: {response.text}"
        
        created_user = response.json()
        user_id = created_user.get('id')
        
        yield {
            "id": user_id,
            "username": unique_username,
            "email": unique_email
        }
        
        # Limpieza: eliminamos el usuario
        make_request('DELETE', f'/api/users/{user_id}')
    
    def test_get_all_users(self):
        """
        Prueba para obtener todos los usuarios.
        """
        response = make_request('GET', '/api/users')
        
        assert response.status_code == 200, f"Error: {response.text}"
        assert isinstance(response.json(), list), "Se esperaba una lista de usuarios"
        
        # Si hay usuarios, validamos el esquema del primero
        if len(response.json()) > 0:
            assert validate_response_schema(response, USER_SCHEMA), "El esquema no es válido"
    
    def test_get_user_by_id(self, create_test_user):
        """
        Prueba para obtener un usuario por ID.
        """
        user = create_test_user
        response = make_request('GET', f'/api/users/{user["id"]}')
        
        assert response.status_code == 200, f"Error: {response.text}"
        assert response.json().get('id') == user['id'], "El ID no coincide"
        assert validate_response_schema(response, USER_SCHEMA), "El esquema no es válido"
    
    def test_get_user_by_username(self, create_test_user):
        """
        Prueba para obtener un usuario por nombre de usuario.
        """
        user = create_test_user
        response = make_request('GET', f'/api/users/username/{user["username"]}')
        
        assert response.status_code == 200, f"Error: {response.text}"
        assert response.json().get('username') == user['username'], "El nombre de usuario no coincide"
        assert validate_response_schema(response, USER_SCHEMA), "El esquema no es válido"
    
    def test_create_user(self):
        """
        Prueba para crear un nuevo usuario.
        """
        unique_username = f"create_test_{uuid.uuid4().hex[:8]}"
        user_data = {
            "username": unique_username,
            "email": f"{unique_username}@example.com",
            "password": "Create@1234"
        }
        
        response = make_request('POST', '/api/users', data=user_data)
        
        assert response.status_code == 201, f"Error al crear usuario: {response.text}"
        created_user = response.json()
        
        # Limpieza
        make_request('DELETE', f'/api/users/{created_user.get("id")}')
    
    def test_update_user(self, create_test_user):
        """
        Prueba para actualizar un usuario existente.
        """
        user = create_test_user
        updated_email = f"updated_{user['email']}"
        
        update_data = {
            "id": user['id'],
            "username": user['username'],
            "email": updated_email
        }
        
        # Actualizamos con el endpoint que requiere el ID en el cuerpo
        response = make_request('PUT', '/api/users', data=update_data)
        
        assert response.status_code == 200, f"Error al actualizar usuario: {response.text}"
        assert response.json().get('email') == updated_email, "El email no se actualizó correctamente"
    
    def test_update_user_by_id(self, create_test_user):
        """
        Prueba para actualizar un usuario específico por ID.
        """
        user = create_test_user
        updated_email = f"updated_id_{user['email']}"
        
        update_data = {
            "username": user['username'],
            "email": updated_email
        }
        
        # Actualizamos con el endpoint que incluye el ID en la URL
        response = make_request('PUT', f'/api/users/{user["id"]}', data=update_data)
        
        assert response.status_code == 200, f"Error al actualizar usuario: {response.text}"
        assert response.json().get('email') == updated_email, "El email no se actualizó correctamente"
    
    def test_delete_user(self):
        """
        Prueba para eliminar un usuario.
        """
        # Creamos un usuario para luego eliminarlo
        unique_username = f"delete_test_{uuid.uuid4().hex[:8]}"
        user_data = {
            "username": unique_username,
            "email": f"{unique_username}@example.com",
            "password": "Delete@1234"
        }
        
        create_response = make_request('POST', '/api/users', data=user_data)
        assert create_response.status_code == 201, f"Error al crear usuario: {create_response.text}"
        
        user_id = create_response.json().get('id')
        
        # Eliminamos el usuario
        delete_response = make_request('DELETE', f'/api/users/{user_id}')
        assert delete_response.status_code == 204, f"Error al eliminar usuario: {delete_response.text}"
        
        # Verificamos que ya no exista
        get_response = make_request('GET', f'/api/users/{user_id}')
        assert get_response.status_code == 404, "El usuario no se eliminó correctamente"
