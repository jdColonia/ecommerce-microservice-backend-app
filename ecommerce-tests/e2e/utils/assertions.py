"""
Funciones de aserción personalizadas para pruebas E2E.
"""

import logging
import time
from typing import Dict, Any, List, Optional, Callable, Union
import requests

logger = logging.getLogger(__name__)

def assert_status_code(response: requests.Response, expected_code: int) -> None:
    """
    Verifica que el código de estado sea el esperado.
    
    Args:
        response (Response): Respuesta HTTP
        expected_code (int): Código de estado esperado
        
    Raises:
        AssertionError: Si el código de estado no coincide
    """
    assert response.status_code == expected_code, \
        f"Status code esperado {expected_code}, pero se recibió {response.status_code}. Respuesta: {response.text}"

def assert_contains_keys(data: Dict[str, Any], expected_keys: List[str]) -> None:
    """
    Verifica que un diccionario contenga todas las claves esperadas.
    
    Args:
        data (dict): Diccionario a verificar
        expected_keys (list): Lista de claves esperadas
        
    Raises:
        AssertionError: Si falta alguna clave
    """
    missing_keys = [key for key in expected_keys if key not in data]
    assert not missing_keys, f"Faltan las siguientes claves en la respuesta: {missing_keys}"

def assert_entity_values(entity: Dict[str, Any], expected_values: Dict[str, Any]) -> None:
    """
    Verifica que una entidad tenga los valores esperados.
    
    Args:
        entity (dict): Entidad a verificar
        expected_values (dict): Valores esperados
        
    Raises:
        AssertionError: Si algún valor no coincide
    """
    for key, expected_value in expected_values.items():
        assert key in entity, f"La clave '{key}' no está presente en la entidad"
        assert entity[key] == expected_value, \
            f"Valor esperado para '{key}': {expected_value}, pero se recibió: {entity[key]}"

def assert_entity_exists(
    get_function: Callable[[Union[int, str]], Optional[Dict[str, Any]]], 
    entity_id: Union[int, str], 
    timeout: int = 10
) -> Dict[str, Any]:
    """
    Verifica que una entidad exista, con reintentos.
    
    Args:
        get_function (callable): Función para obtener la entidad
        entity_id (int|str): ID de la entidad
        timeout (int): Tiempo máximo de espera en segundos
        
    Returns:
        dict: La entidad encontrada
        
    Raises:
        AssertionError: Si la entidad no existe después del timeout
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        entity = get_function(entity_id)
        if entity:
            return entity
        time.sleep(1)
    
    assert False, f"La entidad con ID {entity_id} no fue encontrada después de {timeout} segundos"
    return {}  # Para satisfacer el type checker, nunca se ejecuta

def assert_entity_deleted(
    get_function: Callable[[Union[int, str]], Optional[Dict[str, Any]]], 
    entity_id: Union[int, str], 
    timeout: int = 10
) -> None:
    """
    Verifica que una entidad haya sido eliminada, con reintentos.
    
    Args:
        get_function (callable): Función para obtener la entidad
        entity_id (int|str): ID de la entidad
        timeout (int): Tiempo máximo de espera en segundos
        
    Raises:
        AssertionError: Si la entidad sigue existiendo después del timeout
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        entity = get_function(entity_id)
        if entity is None:
            return
        time.sleep(1)
    
    assert False, f"La entidad con ID {entity_id} sigue existiendo después de {timeout} segundos"

def assert_order_status(
    get_order_function: Callable[[int], Optional[Dict[str, Any]]], 
    order_id: int, 
    expected_status: str, 
    timeout: int = 30
) -> None:
    """
    Verifica que una orden tenga el estado esperado, con reintentos.
    
    Args:
        get_order_function (callable): Función para obtener la orden
        order_id (int): ID de la orden
        expected_status (str): Estado esperado
        timeout (int): Tiempo máximo de espera en segundos
        
    Raises:
        AssertionError: Si la orden no tiene el estado esperado después del timeout
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        order = get_order_function(order_id)
        if order and order.get("status") == expected_status:
            return
        time.sleep(2)
    
    order = get_order_function(order_id)
    actual_status = order.get("status") if order else "UNKNOWN"
    assert False, f"La orden {order_id} tiene estado {actual_status}, esperaba {expected_status}"
