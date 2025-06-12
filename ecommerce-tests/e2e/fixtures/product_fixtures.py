"""
Fixtures para pruebas E2E relacionadas con productos.
"""

import pytest
import logging
from typing import Dict, Any, List
from utils.api_client import ApiClient
from utils.data_generator import generate_product_data
from flows.product_catalog import ProductCatalogFlow

logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def test_category(api_client: ApiClient) -> Dict[str, Any]:
    """
    Fixture que crea una categoría de prueba.
    
    Args:
        api_client (ApiClient): Cliente API
        
    Returns:
        dict: Datos de la categoría creada
    """
    product_flow = ProductCatalogFlow(api_client)
    
    # Crear categoría
    category_data = {
        "name": f"Categoría de Prueba E2E {generate_product_data()['name']}",
        "description": "Esta es una categoría para pruebas E2E"
    }
    
    category = product_flow.create_category(category_data)
    category_id = category.get("id")
    
    logger.info(f"Categoría de prueba creada: {category_id}")
    
    yield category
    
    # No eliminamos la categoría porque puede tener productos asociados
    # y no conocemos la lógica de eliminación en cascada del backend

@pytest.fixture(scope="function")
def test_product(api_client: ApiClient, test_category: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fixture que crea un producto de prueba y lo elimina al finalizar.
    
    Args:
        api_client (ApiClient): Cliente API
        test_category (dict): Categoría de prueba
        
    Returns:
        dict: Datos del producto creado
    """
    product_flow = ProductCatalogFlow(api_client)
    
    # Crear producto
    product_data = generate_product_data()
    product_data["categoryId"] = test_category.get("id")
    
    product = product_flow.create_product(product_data)
    product_id = product.get("id")
    
    logger.info(f"Producto de prueba creado: {product_id}")
    
    yield product
    
    # Limpiar: eliminar producto
    logger.info(f"Eliminando producto de prueba: {product_id}")
    product_flow.delete_product(product_id)

@pytest.fixture(scope="function")
def test_products(api_client: ApiClient, test_category: Dict[str, Any], count: int = 3) -> List[Dict[str, Any]]:
    """
    Fixture que crea múltiples productos de prueba y los elimina al finalizar.
    
    Args:
        api_client (ApiClient): Cliente API
        test_category (dict): Categoría de prueba
        count (int): Número de productos a crear
        
    Returns:
        list: Lista de productos creados
    """
    product_flow = ProductCatalogFlow(api_client)
    products = []
    
    # Crear productos
    for i in range(count):
        product_data = generate_product_data()
        product_data["categoryId"] = test_category.get("id")
        product_data["name"] = f"{product_data['name']} #{i+1}"
        
        product = product_flow.create_product(product_data)
        products.append(product)
    
    product_ids = [p.get("id") for p in products]
    logger.info(f"Productos de prueba creados: {product_ids}")
    
    yield products
    
    # Limpiar: eliminar productos
    for product in products:
        product_id = product.get("id")
        logger.info(f"Eliminando producto de prueba: {product_id}")
        product_flow.delete_product(product_id)
