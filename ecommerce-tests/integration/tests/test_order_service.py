"""
Pruebas de integración para el Order Service.
"""

import pytest
import uuid
from datetime import datetime
from utils.api_utils import make_request, set_current_service


class TestOrderServiceComplete:
    """
    Pruebas completas para el Order Service - carritos y órdenes.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("order-service")

    # ==================== PRUEBAS PARA CARRITOS ====================

    @pytest.fixture
    def create_test_cart(self):
        """Fixture para crear un carrito de prueba."""
        unique_suffix = uuid.uuid4().hex[:8]
        cart_data = {"userId": 1}

        response = make_request("POST", "/api/carts", data=cart_data)
        assert response.status_code == 200, f"Error al crear carrito: {response.text}"

        created_cart = response.json()
        cart_id = created_cart.get("cartId")

        yield {"id": cart_id, "data": created_cart}

        make_request("DELETE", f"/api/carts/{cart_id}")

    def test_cart_find_all(self):
        """Prueba para obtener todos los carritos."""
        response = make_request("GET", "/api/carts")

        assert response.status_code == 200
        result = response.json()
        assert "collection" in result
        assert isinstance(result["collection"], list)

    def test_cart_find_by_id(self, create_test_cart):
        """Prueba para obtener carrito por ID."""
        cart = create_test_cart
        response = make_request("GET", f'/api/carts/{cart["id"]}')

        assert response.status_code == 200
        result = response.json()
        assert result["cartId"] == cart["id"]

    def test_cart_save(self):
        """Prueba para crear un nuevo carrito."""
        cart_data = {"userId": 2}

        response = make_request("POST", "/api/carts", data=cart_data)

        assert response.status_code == 200
        result = response.json()
        assert result["userId"] == cart_data["userId"]
        assert "cartId" in result

        make_request("DELETE", f'/api/carts/{result["cartId"]}')

    def test_cart_update(self, create_test_cart):
        """Prueba para actualizar carrito."""
        cart = create_test_cart
        updated_data = cart["data"].copy()
        updated_data["userId"] = 999

        response = make_request("PUT", "/api/carts", data=updated_data)

        assert response.status_code == 200
        result = response.json()
        assert result["userId"] == updated_data["userId"]

    def test_cart_update_by_id(self, create_test_cart):
        """Prueba para actualizar carrito por ID."""
        cart = create_test_cart
        updated_data = {"userId": 888}

        response = make_request("PUT", f'/api/carts/{cart["id"]}', data=updated_data)

        assert response.status_code == 200

    def test_cart_delete_by_id(self):
        """Prueba para eliminar carrito."""
        cart_data = {"userId": 555}

        create_response = make_request("POST", "/api/carts", data=cart_data)
        assert create_response.status_code == 200
        cart_id = create_response.json()["cartId"]

        delete_response = make_request("DELETE", f"/api/carts/{cart_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() is True

    # ==================== PRUEBAS PARA ÓRDENES ====================

    @pytest.fixture
    def create_test_order(self, create_test_cart):
        """Fixture para crear una orden de prueba."""
        cart = create_test_cart
        unique_suffix = uuid.uuid4().hex[:8]
        order_data = {
            "orderDesc": f"Test_Order_{unique_suffix}",
            "orderFee": 199.99,
            "cartDto": {"cartId": cart["id"]},
        }

        response = make_request("POST", "/api/orders", data=order_data)
        assert response.status_code == 200, f"Error al crear orden: {response.text}"

        created_order = response.json()
        order_id = created_order.get("orderId")

        yield {"id": order_id, "data": created_order}

        make_request("DELETE", f"/api/orders/{order_id}")

    def test_order_find_all(self):
        """Prueba para obtener todas las órdenes."""
        response = make_request("GET", "/api/orders")

        assert response.status_code == 200
        result = response.json()
        assert "collection" in result
        assert isinstance(result["collection"], list)

    def test_order_find_by_id(self, create_test_order):
        """Prueba para obtener orden por ID."""
        order = create_test_order
        response = make_request("GET", f'/api/orders/{order["id"]}')

        assert response.status_code == 200
        result = response.json()
        assert result["orderId"] == order["id"]
        assert result["orderDesc"] == order["data"]["orderDesc"]

    def test_order_save(self, create_test_cart):
        """Prueba para crear una nueva orden."""
        cart = create_test_cart
        unique_suffix = uuid.uuid4().hex[:8]
        order_data = {
            "orderDesc": f"Save_Order_{unique_suffix}",
            "orderFee": 299.99,
            "cartDto": {"cartId": cart["id"]},
        }

        response = make_request("POST", "/api/orders", data=order_data)

        assert response.status_code == 200
        result = response.json()
        assert result["orderDesc"] == order_data["orderDesc"]
        assert result["orderFee"] == order_data["orderFee"]
        assert "orderId" in result

        make_request("DELETE", f'/api/orders/{result["orderId"]}')

    def test_order_update(self, create_test_order):
        """Prueba para actualizar orden."""
        order = create_test_order
        updated_data = order["data"].copy()
        updated_data["orderDesc"] = f"Updated_Order_{uuid.uuid4().hex[:6]}"
        updated_data["orderFee"] = 399.99

        response = make_request("PUT", "/api/orders", data=updated_data)

        assert response.status_code == 200
        result = response.json()
        assert result["orderDesc"] == updated_data["orderDesc"]
        assert result["orderFee"] == updated_data["orderFee"]

    def test_order_update_by_id(self, create_test_order):
        """Prueba para actualizar orden por ID."""
        order = create_test_order
        updated_data = {
            "orderDesc": f"UpdatedById_Order_{uuid.uuid4().hex[:6]}",
            "orderFee": 499.99,
        }

        response = make_request("PUT", f'/api/orders/{order["id"]}', data=updated_data)

        assert response.status_code == 200

    def test_order_delete_by_id(self, create_test_cart):
        """Prueba para eliminar orden."""
        cart = create_test_cart
        unique_suffix = uuid.uuid4().hex[:8]
        order_data = {
            "orderDesc": f"Delete_Order_{unique_suffix}",
            "orderFee": 99.99,
            "cartDto": {"cartId": cart["id"]},
        }

        create_response = make_request("POST", "/api/orders", data=order_data)
        assert create_response.status_code == 200
        order_id = create_response.json()["orderId"]

        delete_response = make_request("DELETE", f"/api/orders/{order_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() is True
