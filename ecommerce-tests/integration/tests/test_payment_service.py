"""
Pruebas de integración para el Payment Service.
"""

import pytest
import uuid
from utils.api_utils import make_request, set_current_service


class TestPaymentServiceComplete:
    """
    Pruebas completas para el Payment Service - gestión de pagos.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("payment-service")

    # ==================== PRUEBAS PARA PAGOS ====================

    @pytest.fixture
    def create_test_payment(self):
        """Fixture para crear un pago de prueba."""
        payment_data = {
            "isPayed": False,
            "paymentStatus": "NOT_STARTED",
            "order": {"orderId": 1},
        }

        response = make_request("POST", "/api/payments", data=payment_data)
        assert response.status_code == 200, f"Error al crear pago: {response.text}"

        created_payment = response.json()
        payment_id = created_payment.get("paymentId")

        yield {"id": payment_id, "data": created_payment}

        make_request("DELETE", f"/api/payments/{payment_id}")

    def test_payment_find_all(self):
        """Prueba para obtener todos los pagos."""
        response = make_request("GET", "/api/payments")

        assert response.status_code == 200
        result = response.json()
        assert "collection" in result
        assert isinstance(result["collection"], list)

    def test_payment_find_by_id(self, create_test_payment):
        """Prueba para obtener pago por ID."""
        payment = create_test_payment
        response = make_request("GET", f'/api/payments/{payment["id"]}')

        assert response.status_code == 200
        result = response.json()
        assert result["paymentId"] == payment["id"]
        assert result["isPayed"] == payment["data"]["isPayed"]

    def test_payment_save(self):
        """Prueba para crear un nuevo pago."""
        payment_data = {
            "isPayed": True,
            "paymentStatus": "COMPLETED",
            "order": {"orderId": 1},
        }

        response = make_request("POST", "/api/payments", data=payment_data)

        assert response.status_code == 200
        result = response.json()
        assert result["isPayed"] == payment_data["isPayed"]
        assert result["paymentStatus"] == payment_data["paymentStatus"]
        assert "paymentId" in result

        make_request("DELETE", f'/api/payments/{result["paymentId"]}')

    def test_payment_update(self, create_test_payment):
        """Prueba para actualizar pago."""
        payment = create_test_payment
        updated_data = payment["data"].copy()
        updated_data["isPayed"] = True
        updated_data["paymentStatus"] = "IN_PROGRESS"

        response = make_request("PUT", "/api/payments", data=updated_data)

        assert response.status_code == 200
        result = response.json()
        assert result["isPayed"] == updated_data["isPayed"]
        assert result["paymentStatus"] == updated_data["paymentStatus"]

    def test_payment_delete_by_id(self):
        """Prueba para eliminar pago."""
        payment_data = {
            "isPayed": False,
            "paymentStatus": "NOT_STARTED",
            "order": {"orderId": 1},
        }

        create_response = make_request("POST", "/api/payments", data=payment_data)
        assert create_response.status_code == 200
        payment_id = create_response.json()["paymentId"]

        delete_response = make_request("DELETE", f"/api/payments/{payment_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() is True

    def test_payment_status_transitions(self):
        """Prueba para verificar transiciones de estado de pago."""
        payment_data = {
            "isPayed": False,
            "paymentStatus": "NOT_STARTED",
            "order": {"orderId": 1},
        }

        create_response = make_request("POST", "/api/payments", data=payment_data)
        assert create_response.status_code == 200
        payment = create_response.json()

        payment["paymentStatus"] = "IN_PROGRESS"
        update_response_1 = make_request("PUT", "/api/payments", data=payment)
        assert update_response_1.status_code == 200
        updated_payment_1 = update_response_1.json()
        assert updated_payment_1["paymentStatus"] == "IN_PROGRESS"
        assert updated_payment_1["isPayed"] is False

        payment["isPayed"] = True
        payment["paymentStatus"] = "COMPLETED"
        update_response_2 = make_request("PUT", "/api/payments", data=payment)
        assert update_response_2.status_code == 200
        updated_payment_2 = update_response_2.json()
        assert updated_payment_2["paymentStatus"] == "COMPLETED"
        assert updated_payment_2["isPayed"] is True

        make_request("DELETE", f'/api/payments/{payment["paymentId"]}')

    def test_payment_with_order_reference(self):
        """Prueba para crear pago con referencia a orden."""
        payment_data = {
            "isPayed": False,
            "paymentStatus": "NOT_STARTED",
            "order": {"orderId": 1},
        }

        response = make_request("POST", "/api/payments", data=payment_data)

        assert response.status_code == 200
        result = response.json()
        assert result["isPayed"] == payment_data["isPayed"]
        assert result["paymentStatus"] == payment_data["paymentStatus"]
        if "order" in result and result["order"]:
            assert result["order"]["orderId"] == payment_data["order"]["orderId"]

        make_request("DELETE", f'/api/payments/{result["paymentId"]}')
