"""
Clase base para usuarios de Locust.
"""

import time
import random
import json
import logging
from typing import Dict, Any, Optional, List
from locust import User, TaskSet, task, constant_throughput, between
from locust.exception import StopUser
from config import settings

logger = logging.getLogger(__name__)

class BaseUser(User):
    """Clase base para todos los usuarios de Locust."""
    
    abstract = True  # No se instanciará directamente
    
    # Tiempo entre tareas
    wait_time = between(settings.MIN_WAIT / 1000, settings.MAX_WAIT / 1000)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.timeout = settings.REQUEST_TIMEOUT
        self.token = None
        self.user_id = None
    
    def on_start(self):
        """Método llamado cuando el usuario comienza la simulación."""
        if hasattr(self, 'auth_required') and self.auth_required:
            self.login()
    
    def on_stop(self):
        """Método llamado cuando el usuario termina la simulación."""
        if self.token:
            self.logout()
    
    def login(self):
        """Realiza el login y guarda el token JWT."""
        if not hasattr(self, 'username') or not hasattr(self, 'password'):
            logger.error("No se encontraron credenciales para el usuario")
            raise StopUser()
        
        with self.client.post(
            settings.ENDPOINTS['authentication'],
            json={"username": self.username, "password": self.password},
            catch_response=True,
            name="Login"
        ) as response:
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.user_id = data.get('userId')
                
                if self.token:
                    self.client.headers.update({"Authorization": f"Bearer {self.token}"})
                    logger.debug(f"Login exitoso para {self.username}")
                else:
                    response.failure("No se recibió token JWT")
                    logger.error(f"No se recibió token JWT para {self.username}")
                    raise StopUser()
            else:
                response.failure(f"Login fallido: {response.text}")
                logger.error(f"Login fallido para {self.username}: {response.text}")
                raise StopUser()
    
    def logout(self):
        """Limpia el token y las cabeceras."""
        # No hay un endpoint real de logout, solo limpiamos el token
        self.token = None
        if "Authorization" in self.client.headers:
            del self.client.headers["Authorization"]
        logger.debug(f"Logout para {self.username}")
    
    def make_request_with_retry(
        self, 
        method: str, 
        endpoint: str, 
        name: Optional[str] = None,
        **kwargs
    ):
        """
        Realiza una petición HTTP con reintentos.
        
        Args:
            method (str): Método HTTP (get, post, put, delete)
            endpoint (str): Endpoint relativo
            name (str, optional): Nombre para la petición en los informes
            **kwargs: Argumentos adicionales para la petición
            
        Returns:
            Response: Objeto de respuesta
        """
        method_func = getattr(self.client, method.lower())
        retries = 0
        
        if 'catch_response' not in kwargs:
            kwargs['catch_response'] = True
        
        while retries < settings.MAX_RETRIES:
            with method_func(endpoint, name=name, **kwargs) as response:
                if 200 <= response.status_code < 500:
                    return response
                
                retries += 1
                if retries < settings.MAX_RETRIES:
                    response.failure(f"Reintentando {retries}/{settings.MAX_RETRIES}: {response.status_code}")
                    time.sleep(0.5)  # Pequeña espera antes de reintentar
                else:
                    response.failure(f"Fallo después de {settings.MAX_RETRIES} intentos: {response.text}")
                    return response
