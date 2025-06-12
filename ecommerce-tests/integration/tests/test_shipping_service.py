"""
Pruebas de integración para el Shipping Service.
"""

import pytest
import uuid
from utils.api_utils import make_request, set_current_service


class TestShippingServiceComplete:
    """
    Pruebas completas para el Shipping Service - gestión de envíos.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("shipping-service")

    # ==================== PRUEBAS PARA ITEMS DE ENVÍO ====================

    @pytest.fixture
    def create_test_order_item(self):
        """Fixture para crear un item de orden de prueba."""
        order_item_data = {
            "productId": 1,
            "orderId": 1,
            "orderedQuantity": 5,
        }

        response = make_request("POST", "/api/shippings", data=order_item_data)
        assert (
            response.status_code == 200
        ), f"Error al crear item de orden: {response.text}"

        created_order_item = response.json()

        yield {"data": created_order_item}

        order_id = created_order_item["orderId"]
        product_id = created_order_item["productId"]
        make_request("DELETE", f"/api/shippings/{order_id}/{product_id}")

    def test_order_item_find_all(self):
        """Prueba para obtener todos los items de envío."""
        response = make_request("GET", "/api/shippings")

        assert response.status_code == 200
        result = response.json()
        assert "collection" in result
        assert isinstance(result["collection"], list)

    def test_order_item_save(self):
        """Prueba para crear un nuevo item de orden."""
        order_item_data = {
            "productId": 2,
            "orderId": 2,
            "orderedQuantity": 10,
        }

        response = make_request("POST", "/api/shippings", data=order_item_data)

        assert response.status_code == 200
        result = response.json()
        assert result["productId"] == order_item_data["productId"]
        assert result["orderId"] == order_item_data["orderId"]
        assert result["orderedQuantity"] == order_item_data["orderedQuantity"]

        order_id = result["orderId"]
        product_id = result["productId"]
        make_request("DELETE", f"/api/shippings/{order_id}/{product_id}")

    def test_order_item_update(self, create_test_order_item):
        """Prueba para actualizar item de orden."""
        order_item = create_test_order_item
        updated_data = order_item["data"].copy()
        updated_data["orderedQuantity"] = 15

        response = make_request("PUT", "/api/shippings", data=updated_data)

        assert response.status_code == 200
        result = response.json()
        assert result["orderedQuantity"] == updated_data["orderedQuantity"]

    def test_order_item_quantity_management(self):
        """Prueba para gestión de cantidades de envío."""
        order_item_data = {
            "productId": 5,
            "orderId": 5,
            "orderedQuantity": 20,
        }

        create_response = make_request("POST", "/api/shippings", data=order_item_data)
        assert create_response.status_code == 200
        order_item = create_response.json()

        order_item["orderedQuantity"] = 25
        update_response = make_request("PUT", "/api/shippings", data=order_item)
        assert update_response.status_code == 200
        updated_order_item = update_response.json()
        assert updated_order_item["orderedQuantity"] == 25

        order_item["orderedQuantity"] = 30
        final_update_response = make_request("PUT", "/api/shippings", data=order_item)
        assert final_update_response.status_code == 200
        final_order_item = final_update_response.json()
        assert final_order_item["orderedQuantity"] == 30

        order_id = order_item["orderId"]
        product_id = order_item["productId"]
        make_request("DELETE", f"/api/shippings/{order_id}/{product_id}")

    def test_order_item_with_references(self):
        """Prueba para crear item de orden con referencias a producto y orden."""
        order_item_data = {
            "productId": 6,
            "orderId": 6,
            "orderedQuantity": 7,
            "productDto": {"productId": 6},
            "orderDto": {"orderId": 6},
        }

        response = make_request("POST", "/api/shippings", data=order_item_data)

        assert response.status_code == 200
        result = response.json()
        assert result["productId"] == order_item_data["productId"]
        assert result["orderId"] == order_item_data["orderId"]
        assert result["orderedQuantity"] == order_item_data["orderedQuantity"]

        if "productDto" in result and result["productDto"]:
            assert (
                result["productDto"]["productId"]
                == order_item_data["productDto"]["productId"]
            )
        if "orderDto" in result and result["orderDto"]:
            assert (
                result["orderDto"]["orderId"] == order_item_data["orderDto"]["orderId"]
            )

        order_id = result["orderId"]
        product_id = result["productId"]
        make_request("DELETE", f"/api/shippings/{order_id}/{product_id}")
