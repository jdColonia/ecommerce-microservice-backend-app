"""
Cliente para interactuar con la API Gateway.
"""

import requests
import logging
import json
import time
from typing import Dict, Any, Optional, Union, List
from requests.exceptions import RequestException
from config.config import API_BASE_URL, REQUEST_TIMEOUT, MAX_RETRIES, RETRY_DELAY

logger = logging.getLogger(__name__)

class ApiClient:
    """Cliente para interactuar con la API Gateway."""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.auth_token = None
    
    def authenticate(self, username: str, password: str) -> bool:
        """
        Autentica con el servicio y guarda el token JWT.
        
        Args:
            username (str): Nombre de usuario
            password (str): Contraseña
            
        Returns:
            bool: True si la autenticación fue exitosa, False en caso contrario
        """
        try:
            response = self._make_request_with_retry(
                method="POST",
                url=f"{self.base_url}/api/authenticate",
                json={"username": username, "password": password}
            )
            
            response.raise_for_status()
            self.auth_token = response.json().get("token")
            if self.auth_token:
                self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
                logger.info(f"Autenticación exitosa para {username}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error en autenticación: {str(e)}")
            return False
    
    def request(
        self, 
        method: str, 
        endpoint: str, 
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        Realiza una petición HTTP al API Gateway.
        
        Args:
            method (str): Método HTTP ('GET', 'POST', 'PUT', 'DELETE')
            endpoint (str): Endpoint relativo
            data (dict, optional): Datos para la solicitud
            params (dict, optional): Parámetros de consulta
            files (dict, optional): Archivos para subir
            
        Returns:
            Response: Objeto de respuesta
        """
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"Realizando petición {method} a {url}")
        
        try:
            return self._make_request_with_retry(
                method=method,
                url=url,
                json=data,
                params=params,
                files=files
            )
        except Exception as e:
            logger.error(f"Error en petición {method} {url}: {str(e)}")
            raise
    
    def _make_request_with_retry(self, method: str, url: str, **kwargs) -> requests.Response:
        """
        Realiza una petición HTTP con reintentos en caso de error.
        
        Args:
            method (str): Método HTTP
            url (str): URL completa
            **kwargs: Argumentos para requests
            
        Returns:
            Response: Objeto de respuesta
            
        Raises:
            RequestException: Si la petición falla después de todos los reintentos
        """
        retries = 0
        last_exception = None
        
        while retries < MAX_RETRIES:
            try:
                response = self.session.request(
                    method=method,
                    url=url,
                    timeout=REQUEST_TIMEOUT,
                    **kwargs
                )
                
                # Registrar detalles de la respuesta
                log_message = (
                    f"Respuesta: {response.status_code} - "
                    f"{response.text[:100] + '...' if len(response.text) > 100 else response.text}"
                )
                if 200 <= response.status_code < 300:
                    logger.debug(log_message)
                else:
                    logger.warning(log_message)
                
                return response
            
            except RequestException as e:
                last_exception = e
                retries += 1
                logger.warning(f"Intento {retries}/{MAX_RETRIES} falló: {str(e)}")
                
                if retries < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
        
        logger.error(f"Todos los reintentos fallaron para {method} {url}")
        raise last_exception
    
    def verify_service_health(self) -> bool:
        """
        Verifica que el API Gateway esté disponible.
        
        Returns:
            bool: True si el servicio está disponible, False en caso contrario
        """
        try:
            # Intentar hacer una petición simple para verificar conectividad
            # Este endpoint debería ser uno que no requiera autenticación
            response = self.session.get(
                f"{self.base_url}/health",  # Ajustar según el endpoint real de health check
                timeout=REQUEST_TIMEOUT
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error verificando salud del servicio: {str(e)}")
            return False
    
    def get_by_id(self, service: str, entity_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """
        Obtiene una entidad por su ID.
        
        Args:
            service (str): Nombre del servicio (users, products, orders, etc.)
            entity_id (int|str): ID de la entidad
            
        Returns:
            dict|None: Datos de la entidad o None si no se encuentra
        """
        try:
            response = self.request('GET', f"/api/{service}/{entity_id}")
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                logger.warning(f"No se encontró {service} con ID {entity_id}")
                return None
            else:
                response.raise_for_status()
        except Exception as e:
            logger.error(f"Error obteniendo {service}/{entity_id}: {str(e)}")
            return None
    
    def create_entity(self, service: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Crea una nueva entidad.
        
        Args:
            service (str): Nombre del servicio (users, products, orders, etc.)
            data (dict): Datos para crear la entidad
            
        Returns:
            dict|None: Datos de la entidad creada o None si falla
        """
        try:
            response = self.request('POST', f"/api/{service}", data=data)
            
            if response.status_code in (200, 201):
                return response.json()
            else:
                response.raise_for_status()
        except Exception as e:
            logger.error(f"Error creando {service}: {str(e)}")
            return None
    
    def update_entity(self, service: str, entity_id: Union[int, str], data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Actualiza una entidad existente.
        
        Args:
            service (str): Nombre del servicio (users, products, orders, etc.)
            entity_id (int|str): ID de la entidad
            data (dict): Datos para actualizar
            
        Returns:
            dict|None: Datos actualizados o None si falla
        """
        try:
            response = self.request('PUT', f"/api/{service}/{entity_id}", data=data)
            
            if response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()
        except Exception as e:
            logger.error(f"Error actualizando {service}/{entity_id}: {str(e)}")
            return None
    
    def delete_entity(self, service: str, entity_id: Union[int, str]) -> bool:
        """
        Elimina una entidad.
        
        Args:
            service (str): Nombre del servicio (users, products, orders, etc.)
            entity_id (int|str): ID de la entidad
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
        """
        try:
            response = self.request('DELETE', f"/api/{service}/{entity_id}")
            
            return response.status_code in (200, 204)
        except Exception as e:
            logger.error(f"Error eliminando {service}/{entity_id}: {str(e)}")
            return False
    
    def get_all_entities(self, service: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Obtiene todas las entidades de un servicio.
        
        Args:
            service (str): Nombre del servicio (users, products, orders, etc.)
            params (dict, optional): Parámetros de consulta
            
        Returns:
            list: Lista de entidades
        """
        try:
            response = self.request('GET', f"/api/{service}", params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                response.raise_for_status()
                return []
        except Exception as e:
            logger.error(f"Error obteniendo {service}: {str(e)}")
            return []
