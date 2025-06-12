"""
Utilidades para pruebas de integración.
"""

import requests
import json
from config.config import BASE_URL, AUTH_ENDPOINT, TEST_USER, REQUEST_TIMEOUT

def get_auth_token():
    """
    Obtiene un token JWT de autenticación.
    
    Returns:
        str: Token JWT.
    """
    response = requests.post(
        AUTH_ENDPOINT,
        json={
            "username": TEST_USER["username"],
            "password": TEST_USER["password"]
        },
        timeout=REQUEST_TIMEOUT
    )
    
    if response.status_code == 200:
        return response.json().get("token")
    else:
        raise Exception(f"Error al obtener token de autenticación: {response.text}")

def get_headers(token=None):
    """
    Genera headers con autenticación para las solicitudes.
    
    Args:
        token (str, optional): Token JWT. Si es None, se obtendrá uno nuevo.
        
    Returns:
        dict: Headers para las solicitudes.
    """
    if token is None:
        token = get_auth_token()
        
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def make_request(method, endpoint, data=None, params=None, token=None):
    """
    Realiza una solicitud HTTP al API Gateway.
    
    Args:
        method (str): Método HTTP ('GET', 'POST', 'PUT', 'DELETE').
        endpoint (str): Endpoint relativo.
        data (dict, optional): Datos para la solicitud.
        params (dict, optional): Parámetros de consulta.
        token (str, optional): Token JWT. Si es None, se obtendrá uno nuevo.
        
    Returns:
        Response: Objeto de respuesta.
    """
    url = f"{BASE_URL}{endpoint}"
    headers = get_headers(token)
    
    if method.upper() == 'GET':
        return requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
    elif method.upper() == 'POST':
        return requests.post(url, headers=headers, json=data, timeout=REQUEST_TIMEOUT)
    elif method.upper() == 'PUT':
        return requests.put(url, headers=headers, json=data, timeout=REQUEST_TIMEOUT)
    elif method.upper() == 'DELETE':
        return requests.delete(url, headers=headers, timeout=REQUEST_TIMEOUT)
    else:
        raise ValueError(f"Método HTTP no soportado: {method}")

def validate_response_schema(response, schema):
    """
    Valida que la respuesta cumpla con un esquema esperado.
    
    Args:
        response (Response): Respuesta HTTP.
        schema (dict): Esquema esperado con tipos de datos.
        
    Returns:
        bool: True si la validación es exitosa, False en caso contrario.
    """
    try:
        response_data = response.json()
        
        # Si es una lista, validamos el primer elemento
        if isinstance(response_data, list) and len(response_data) > 0:
            response_data = response_data[0]
            
        for key, expected_type in schema.items():
            if key not in response_data:
                print(f"La clave '{key}' no está presente en la respuesta")
                return False
                
            if not isinstance(response_data[key], expected_type):
                print(f"La clave '{key}' no es del tipo esperado {expected_type}")
                return False
                
        return True
    except Exception as e:
        print(f"Error al validar el esquema: {e}")
        return False
