"""
Pruebas de integración para el servicio de productos.
"""

import pytest
import uuid
from utils.api_utils import make_request, validate_response_schema
from config.config import TEST_PRODUCT

# Esquema esperado para un producto
PRODUCT_SCHEMA = {
    "id": int,
    "name": str,
    "description": str,
    "price": float,
    "stock": int,
    "categoryId": int
}

class TestProductService:
    """
    Pruebas para el servicio de productos.
    """
    
    @pytest.fixture
    def create_test_product(self):
        """
        Fixture para crear un producto de prueba.
        """
        # Generamos un nombre único para evitar conflictos
        unique_name = f"Test Product {uuid.uuid4().hex[:8]}"
        
        product_data = {
            "name": unique_name,
            "description": TEST_PRODUCT["description"],
            "price": TEST_PRODUCT["price"],
            "stock": TEST_PRODUCT["stock"],
            "categoryId": TEST_PRODUCT["categoryId"]
        }
        
        # Creamos el producto
        response = make_request('POST', '/api/products', data=product_data)
        
        # Verificamos que se haya creado correctamente
        assert response.status_code == 201, f"Error al crear producto: {response.text}"
        
        created_product = response.json()
        product_id = created_product.get('id')
        
        yield {
            "id": product_id,
            "name": unique_name,
            "description": TEST_PRODUCT["description"],
            "price": TEST_PRODUCT["price"],
            "stock": TEST_PRODUCT["stock"],
            "categoryId": TEST_PRODUCT["categoryId"]
        }
        
        # Limpieza: eliminamos el producto
        make_request('DELETE', f'/api/products/{product_id}')
    
    def test_get_all_products(self):
        """
        Prueba para obtener todos los productos.
        """
        response = make_request('GET', '/api/products')
        
        assert response.status_code == 200, f"Error: {response.text}"
        assert isinstance(response.json(), list), "Se esperaba una lista de productos"
        
        # Si hay productos, validamos el esquema del primero
        if len(response.json()) > 0:
            assert validate_response_schema(response, PRODUCT_SCHEMA), "El esquema no es válido"
    
    def test_get_product_by_id(self, create_test_product):
        """
        Prueba para obtener un producto por ID.
        """
        product = create_test_product
        response = make_request('GET', f'/api/products/{product["id"]}')
        
        assert response.status_code == 200, f"Error: {response.text}"
        assert response.json().get('id') == product['id'], "El ID no coincide"
        assert validate_response_schema(response, PRODUCT_SCHEMA), "El esquema no es válido"
    
    def test_create_product(self):
        """
        Prueba para crear un nuevo producto.
        """
        unique_name = f"Create Product {uuid.uuid4().hex[:8]}"
        product_data = {
            "name": unique_name,
            "description": "Producto para prueba de creación",
            "price": 149.99,
            "stock": 50,
            "categoryId": TEST_PRODUCT["categoryId"]
        }
        
        response = make_request('POST', '/api/products', data=product_data)
        
        assert response.status_code == 201, f"Error al crear producto: {response.text}"
        created_product = response.json()
        
        # Limpieza
        make_request('DELETE', f'/api/products/{created_product.get("id")}')
    
    def test_update_product(self, create_test_product):
        """
        Prueba para actualizar un producto existente.
        """
        product = create_test_product
        updated_price = product['price'] + 10.0
        
        update_data = {
            "id": product['id'],
            "name": product['name'],
            "description": product['description'],
            "price": updated_price,
            "stock": product['stock'],
            "categoryId": product['categoryId']
        }
        
        # Actualizamos con el endpoint que requiere el ID en el cuerpo
        response = make_request('PUT', '/api/products', data=update_data)
        
        assert response.status_code == 200, f"Error al actualizar producto: {response.text}"
        assert response.json().get('price') == updated_price, "El precio no se actualizó correctamente"
    
    def test_update_product_by_id(self, create_test_product):
        """
        Prueba para actualizar un producto específico por ID.
        """
        product = create_test_product
        updated_stock = product['stock'] - 10
        
        update_data = {
            "name": product['name'],
            "description": product['description'],
            "price": product['price'],
            "stock": updated_stock,
            "categoryId": product['categoryId']
        }
        
        # Actualizamos con el endpoint que incluye el ID en la URL
        response = make_request('PUT', f'/api/products/{product["id"]}', data=update_data)
        
        assert response.status_code == 200, f"Error al actualizar producto: {response.text}"
        assert response.json().get('stock') == updated_stock, "El stock no se actualizó correctamente"
    
    def test_delete_product(self):
        """
        Prueba para eliminar un producto.
        """
        # Creamos un producto para luego eliminarlo
        unique_name = f"Delete Product {uuid.uuid4().hex[:8]}"
        product_data = {
            "name": unique_name,
            "description": "Producto para prueba de eliminación",
            "price": 79.99,
            "stock": 25,
            "categoryId": TEST_PRODUCT["categoryId"]
        }
        
        create_response = make_request('POST', '/api/products', data=product_data)
        assert create_response.status_code == 201, f"Error al crear producto: {create_response.text}"
        
        product_id = create_response.json().get('id')
        
        # Eliminamos el producto
        delete_response = make_request('DELETE', f'/api/products/{product_id}')
        assert delete_response.status_code == 204, f"Error al eliminar producto: {delete_response.text}"
        
        # Verificamos que ya no exista
        get_response = make_request('GET', f'/api/products/{product_id}')
        assert get_response.status_code == 404, "El producto no se eliminó correctamente"
