"""
Flujo de gestión de usuarios: registro, actualización, eliminación.
"""

import logging
from typing import Dict, Any, List, Optional
from utils.api_client import ApiClient
from utils.data_generator import generate_unique_username, generate_unique_email

logger = logging.getLogger(__name__)

class UserManagementFlow:
    """Implementa el flujo de gestión de usuarios."""
    
    def __init__(self, api_client: ApiClient):
        self.api = api_client
    
    def register_user(self, user_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Registra un nuevo usuario.
        
        Args:
            user_data (dict, optional): Datos del usuario. Si es None, se generan automáticamente.
            
        Returns:
            dict: Datos del usuario registrado
        """
        if user_data is None:
            username = generate_unique_username()
            user_data = {
                "username": username,
                "email": generate_unique_email(username),
                "password": "Test@1234"
            }
        
        logger.info(f"Registrando usuario: {user_data['username']}")
        
        response = self.api.request(
            method="POST",
            endpoint="/api/users",
            data=user_data
        )
        response.raise_for_status()
        user = response.json()
        
        logger.info(f"Usuario registrado con ID {user.get('id')}")
        return user
    
    def create_credentials(self, user_id: int, username: str, password: str) -> Dict[str, Any]:
        """
        Crea credenciales para un usuario.
        
        Args:
            user_id (int): ID del usuario
            username (str): Nombre de usuario
            password (str): Contraseña
            
        Returns:
            dict: Datos de las credenciales creadas
        """
        logger.info(f"Creando credenciales para usuario {user_id}")
        
        credentials_data = {
            "userId": user_id,
            "username": username,
            "password": password
        }
        
        response = self.api.request(
            method="POST",
            endpoint="/api/credentials",
            data=credentials_data
        )
        response.raise_for_status()
        credentials = response.json()
        
        logger.info(f"Credenciales creadas para usuario {user_id}")
        return credentials
    
    def add_user_address(self, user_id: int, address_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Añade una dirección a un usuario.
        
        Args:
            user_id (int): ID del usuario
            address_data (dict): Datos de la dirección
            
        Returns:
            dict: Datos de la dirección creada
        """
        logger.info(f"Añadiendo dirección para usuario {user_id}")
        
        # Asegurarse de que el userId esté en los datos
        address_data["userId"] = user_id
        
        response = self.api.request(
            method="POST",
            endpoint="/api/addresses",
            data=address_data
        )
        response.raise_for_status()
        address = response.json()
        
        logger.info(f"Dirección {address.get('id')} añadida para usuario {user_id}")
        return address
    
    def update_user_profile(self, user_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza el perfil de un usuario.
        
        Args:
            user_id (int): ID del usuario
            update_data (dict): Datos a actualizar
            
        Returns:
            dict: Datos actualizados del usuario
        """
        logger.info(f"Actualizando perfil de usuario {user_id}")
        
        # Asegurarse de que el ID esté en los datos
        update_data["id"] = user_id
        
        response = self.api.request(
            method="PUT",
            endpoint=f"/api/users/{user_id}",
            data=update_data
        )
        response.raise_for_status()
        updated_user = response.json()
        
        logger.info(f"Perfil de usuario {user_id} actualizado")
        return updated_user
    
    def delete_user(self, user_id: int) -> bool:
        """
        Elimina un usuario.
        
        Args:
            user_id (int): ID del usuario
            
        Returns:
            bool: True si se eliminó correctamente
        """
        logger.info(f"Eliminando usuario {user_id}")
        
        response = self.api.request(
            method="DELETE",
            endpoint=f"/api/users/{user_id}"
        )
        
        success = response.status_code in (200, 204)
        if success:
            logger.info(f"Usuario {user_id} eliminado correctamente")
        else:
            logger.error(f"Error al eliminar usuario {user_id}: {response.text}")
        
        return success
    
    def complete_user_setup(self, user_data: Optional[Dict[str, Any]] = None, address_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Realiza el flujo completo de configuración de usuario: registro, credenciales, dirección.
        
        Args:
            user_data (dict, optional): Datos del usuario
            address_data (dict, optional): Datos de la dirección
            
        Returns:
            dict: Datos completos del usuario configurado
        """
        logger.info("Iniciando flujo completo de configuración de usuario")
        
        # 1. Registrar usuario
        user = self.register_user(user_data)
        user_id = user.get("id")
        username = user.get("username")
        
        # 2. Crear credenciales si es necesario
        if "password" in (user_data or {}):
            credentials = self.create_credentials(
                user_id=user_id,
                username=username,
                password=user_data["password"]
            )
            user["credentials"] = credentials
        
        # 3. Añadir dirección
        if address_data:
            address = self.add_user_address(user_id, address_data)
            user["address"] = address
        
        logger.info(f"Configuración de usuario {user_id} completada")
        return user
