"""
Pruebas de integración para el servicio de órdenes.
"""

import pytest
import uuid
from utils.api_utils import make_request, validate_response_schema
from config.config import TEST_ORDER

# Esquema esperado para una orden
ORDER_SCHEMA = {
    "id": int,
    "userId": int,
    "totalAmount": float,
    "status": str
}

class TestOrderService:
    """
    Pruebas para el servicio de órdenes.
    """
    
    @pytest.fixture
    def create_test_user(self):
        """
        Fixture para crear un usuario de prueba.
        """
        unique_username = f"order_test_user_{uuid.uuid4().hex[:8]}"
        user_data = {
            "username": unique_username,
            "email": f"{unique_username}@example.com",
            "password": "Test@1234"
        }
        
        # Creamos el usuario
        response = make_request('POST', '/api/users', data=user_data)
        assert response.status_code == 201, f"Error al crear usuario: {response.text}"
        
        created_user = response.json()
        user_id = created_user.get('id')
        
        yield user_id
        
        # Limpieza: eliminamos el usuario
        make_request('DELETE', f'/api/users/{user_id}')
    
    @pytest.fixture
    def create_test_order(self, create_test_user):
        """
        Fixture para crear una orden de prueba.
        """
        user_id = create_test_user
        
        order_data = {
            "userId": user_id,
            "totalAmount": TEST_ORDER["totalAmount"],
            "status": TEST_ORDER["status"]
        }
        
        # Creamos la orden
        response = make_request('POST', '/api/orders', data=order_data)
        
        # Verificamos que se haya creado correctamente
        assert response.status_code == 201, f"Error al crear orden: {response.text}"
        
        created_order = response.json()
        order_id = created_order.get('id')
        
        yield {
            "id": order_id,
            "userId": user_id,
            "totalAmount": TEST_ORDER["totalAmount"],
            "status": TEST_ORDER["status"]
        }
        
        # Limpieza: eliminamos la orden
        make_request('DELETE', f'/api/orders/{order_id}')
    
    def test_get_all_orders(self):
        """
        Prueba para obtener todas las órdenes.
        """
        response = make_request('GET', '/api/orders')
        
        assert response.status_code == 200, f"Error: {response.text}"
        assert isinstance(response.json(), list), "Se esperaba una lista de órdenes"
        
        # Si hay órdenes, validamos el esquema de la primera
        if len(response.json()) > 0:
            assert validate_response_schema(response, ORDER_SCHEMA), "El esquema no es válido"
    
    def test_get_order_by_id(self, create_test_order):
        """
        Prueba para obtener una orden por ID.
        """
        order = create_test_order
        response = make_request('GET', f'/api/orders/{order["id"]}')
        
        assert response.status_code == 200, f"Error: {response.text}"
        assert response.json().get('id') == order['id'], "El ID no coincide"
        assert validate_response_schema(response, ORDER_SCHEMA), "El esquema no es válido"
    
    def test_create_order(self, create_test_user):
        """
        Prueba para crear una nueva orden.
        """
        user_id = create_test_user
        
        order_data = {
            "userId": user_id,
            "totalAmount": 199.99,
            "status": "PROCESSING"
        }
        
        response = make_request('POST', '/api/orders', data=order_data)
        
        assert response.status_code == 201, f"Error al crear orden: {response.text}"
        created_order = response.json()
        
        # Limpieza
        make_request('DELETE', f'/api/orders/{created_order.get("id")}')
    
    def test_update_order(self, create_test_order):
        """
        Prueba para actualizar una orden existente.
        """
        order = create_test_order
        updated_status = "COMPLETED"
        
        update_data = {
            "id": order['id'],
            "userId": order['userId'],
            "totalAmount": order['totalAmount'],
            "status": updated_status
        }
        
        # Actualizamos con el endpoint que requiere el ID en el cuerpo
        response = make_request('PUT', '/api/orders', data=update_data)
        
        assert response.status_code == 200, f"Error al actualizar orden: {response.text}"
        assert response.json().get('status') == updated_status, "El estado no se actualizó correctamente"
    
    def test_update_order_by_id(self, create_test_order):
        """
        Prueba para actualizar una orden específica por ID.
        """
        order = create_test_order
        updated_amount = order['totalAmount'] + 50.0
        
        update_data = {
            "userId": order['userId'],
            "totalAmount": updated_amount,
            "status": order['status']
        }
        
        # Actualizamos con el endpoint que incluye el ID en la URL
        response = make_request('PUT', f'/api/orders/{order["id"]}', data=update_data)
        
        assert response.status_code == 200, f"Error al actualizar orden: {response.text}"
        assert response.json().get('totalAmount') == updated_amount, "El monto total no se actualizó correctamente"
    
    def test_delete_order(self, create_test_user):
        """
        Prueba para eliminar una orden.
        """
        user_id = create_test_user
        
        # Creamos una orden para luego eliminarla
        order_data = {
            "userId": user_id,
            "totalAmount": 49.99,
            "status": "PENDING"
        }
        
        create_response = make_request('POST', '/api/orders', data=order_data)
        assert create_response.status_code == 201, f"Error al crear orden: {create_response.text}"
        
        order_id = create_response.json().get('id')
        
        # Eliminamos la orden
        delete_response = make_request('DELETE', f'/api/orders/{order_id}')
        assert delete_response.status_code == 204, f"Error al eliminar orden: {delete_response.text}"
        
        # Verificamos que ya no exista
        get_response = make_request('GET', f'/api/orders/{order_id}')
        assert get_response.status_code == 404, "La orden no se eliminó correctamente"
