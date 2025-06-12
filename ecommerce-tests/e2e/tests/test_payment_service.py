"""
Pruebas E2E para el Payment Service.
"""

import pytest
from conftest import make_request, set_current_service, generate_unique_id


class TestPaymentServiceE2E:
    """
    Pruebas End-to-End para el Payment Service.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("payment-service")

    def test_e2e_complete_payment_lifecycle(self, cleanup_resources):
        """
        E2E Test 1: Ciclo de vida completo de un pago.
        Crea pago -> Obtiene pago -> Actualiza estado -> Completa pago.
        """
        unique_id = generate_unique_id()

        # 1. Crear pago inicial
        payment_data = {
            "isPayed": False,
            "paymentStatus": "NOT_STARTED",
            "order": {"orderId": 1},
        }

        create_response = make_request("POST", "/api/payments", data=payment_data)
        assert create_response.status_code == 200
        created_payment = create_response.json()
        payment_id = created_payment["paymentId"]
        cleanup_resources["payments"].append(payment_id)

        # Verificar datos del pago creado
        assert created_payment["isPayed"] is False
        assert created_payment["paymentStatus"] == "NOT_STARTED"
        assert "paymentId" in created_payment

        # 2. Obtener pago por ID
        get_response = make_request("GET", f"/api/payments/{payment_id}")
        assert get_response.status_code == 200
        retrieved_payment = get_response.json()
        assert retrieved_payment["paymentId"] == payment_id
        assert retrieved_payment["isPayed"] is False

        # 3. Actualizar estado a "EN PROGRESO"
        updated_data = created_payment.copy()
        updated_data["paymentStatus"] = "IN_PROGRESS"

        update_response = make_request("PUT", "/api/payments", data=updated_data)
        assert update_response.status_code == 200
        updated_payment = update_response.json()
        assert updated_payment["paymentStatus"] == "IN_PROGRESS"
        assert updated_payment["isPayed"] is False

        # 4. Completar pago
        final_data = updated_payment.copy()
        final_data["isPayed"] = True
        final_data["paymentStatus"] = "COMPLETED"

        final_response = make_request("PUT", "/api/payments", data=final_data)
        assert final_response.status_code == 200
        final_payment = final_response.json()
        assert final_payment["isPayed"] is True
        assert final_payment["paymentStatus"] == "COMPLETED"

    def test_e2e_payment_status_transitions(self, cleanup_resources):
        """
        E2E Test 2: Transiciones de estado de pago.
        NOT_STARTED -> IN_PROGRESS -> COMPLETED.
        """
        unique_id = generate_unique_id()

        # 1. Crear pago en estado inicial
        payment_data = {
            "isPayed": False,
            "paymentStatus": "NOT_STARTED",
            "order": {"orderId": 2},
        }

        payment_response = make_request("POST", "/api/payments", data=payment_data)
        assert payment_response.status_code == 200
        payment = payment_response.json()
        payment_id = payment["paymentId"]
        cleanup_resources["payments"].append(payment_id)

        # 2. Transición a IN_PROGRESS
        payment["paymentStatus"] = "IN_PROGRESS"

        progress_response = make_request("PUT", "/api/payments", data=payment)
        assert progress_response.status_code == 200
        progress_payment = progress_response.json()
        assert progress_payment["paymentStatus"] == "IN_PROGRESS"
        assert progress_payment["isPayed"] is False

        # 3. Saltar estado PROCESSING
        progress_payment["isPayed"] = True
        progress_payment["paymentStatus"] = "COMPLETED"

        completed_response = make_request("PUT", "/api/payments", data=progress_payment)
        assert completed_response.status_code == 200
        completed_payment = completed_response.json()
        assert completed_payment["paymentStatus"] == "COMPLETED"
        assert completed_payment["isPayed"] is True

        # 5. Verificar estado final
        final_check_response = make_request("GET", f"/api/payments/{payment_id}")
        assert final_check_response.status_code == 200
        final_payment = final_check_response.json()
        # Verificar que el pago existe y es accesible
        assert "paymentId" in final_payment
        assert final_payment["paymentId"] == payment_id

    def test_e2e_multiple_payments_for_orders(self, cleanup_resources):
        """
        E2E Test 3: Múltiples pagos para diferentes órdenes.
        Crea múltiples pagos -> Procesa cada uno -> Lista todos -> Verifica estados.
        """
        unique_id = generate_unique_id()

        # 1. Crear múltiples pagos para diferentes órdenes
        payments_data = [
            {
                "isPayed": False,
                "paymentStatus": "NOT_STARTED",
                "order": {"orderId": 1},
            },
            {
                "isPayed": False,
                "paymentStatus": "NOT_STARTED",
                "order": {"orderId": 2},
            },
            {
                "isPayed": False,
                "paymentStatus": "NOT_STARTED",
                "order": {"orderId": 3},
            },
        ]

        created_payments = []
        for payment_data in payments_data:
            response = make_request("POST", "/api/payments", data=payment_data)
            assert response.status_code == 200
            payment = response.json()
            created_payments.append(payment)
            cleanup_resources["payments"].append(payment["paymentId"])

        # 2. Procesar cada pago hasta completion
        for i, payment in enumerate(created_payments):
            # Transición a IN_PROGRESS
            payment["paymentStatus"] = "IN_PROGRESS"
            progress_response = make_request("PUT", "/api/payments", data=payment)
            assert progress_response.status_code == 200

            # Transición a COMPLETED
            updated_payment = progress_response.json()
            updated_payment["isPayed"] = True
            updated_payment["paymentStatus"] = "COMPLETED"

            completed_response = make_request(
                "PUT", "/api/payments", data=updated_payment
            )
            assert completed_response.status_code == 200
            final_payment = completed_response.json()
            assert final_payment["isPayed"] is True
            assert final_payment["paymentStatus"] == "COMPLETED"

        # 3. Listar todos los pagos
        all_payments_response = make_request("GET", "/api/payments")
        assert all_payments_response.status_code == 200
        payments_collection = all_payments_response.json()
        assert "collection" in payments_collection
        assert isinstance(payments_collection["collection"], list)

        # 4. Verificar que todos los pagos creados están en la lista
        all_payment_ids = [
            payment["paymentId"] for payment in payments_collection["collection"]
        ]
        for created_payment in created_payments:
            assert created_payment["paymentId"] in all_payment_ids

        # 5. Verificar que todos los pagos están completados
        for created_payment in created_payments:
            specific_payment_response = make_request(
                "GET", f"/api/payments/{created_payment['paymentId']}"
            )
            assert specific_payment_response.status_code == 200
            retrieved_payment = specific_payment_response.json()
            assert retrieved_payment["isPayed"] is True
            assert retrieved_payment["paymentStatus"] == "COMPLETED"

    def test_e2e_payment_failure_and_retry(self, cleanup_resources):
        """
        E2E Test 4: Simulación de reintento de pago (simplificado).
        Crea pago -> Progresa -> Reinicia -> Completa exitosamente.
        """
        unique_id = generate_unique_id()

        # 1. Crear pago inicial
        payment_data = {
            "isPayed": False,
            "paymentStatus": "NOT_STARTED",
            "order": {"orderId": 3},
        }

        payment_response = make_request("POST", "/api/payments", data=payment_data)
        assert payment_response.status_code == 200
        payment = payment_response.json()
        payment_id = payment["paymentId"]
        cleanup_resources["payments"].append(payment_id)

        # 2. Transición a IN_PROGRESS
        payment["paymentStatus"] = "IN_PROGRESS"

        progress_response = make_request("PUT", "/api/payments", data=payment)
        assert progress_response.status_code == 200
        progress_payment = progress_response.json()

        # 3. Simular reintento
        # Volver directamente a NOT_STARTED para simular reintento
        progress_payment["paymentStatus"] = "NOT_STARTED"
        progress_payment["isPayed"] = False

        retry_response = make_request("PUT", "/api/payments", data=progress_payment)
        assert retry_response.status_code == 200
        retry_payment = retry_response.json()
        assert retry_payment["paymentStatus"] == "NOT_STARTED"
        assert retry_payment["isPayed"] is False

        # 4. Segundo intento exitoso
        retry_payment["paymentStatus"] = "IN_PROGRESS"
        second_attempt_response = make_request(
            "PUT", "/api/payments", data=retry_payment
        )
        assert second_attempt_response.status_code == 200

        second_attempt_payment = second_attempt_response.json()
        second_attempt_payment["isPayed"] = True
        second_attempt_payment["paymentStatus"] = "COMPLETED"

        success_response = make_request(
            "PUT", "/api/payments", data=second_attempt_payment
        )
        assert success_response.status_code == 200
        success_payment = success_response.json()
        assert success_payment["isPayed"] is True
        assert success_payment["paymentStatus"] == "COMPLETED"

    def test_e2e_payment_bulk_processing(self, cleanup_resources):
        """
        E2E Test 5: Procesamiento en lote de pagos.
        Crea múltiples pagos -> Procesa en lote -> Verifica resultados -> Genera reportes.
        """
        unique_id = generate_unique_id()

        # 1. Crear múltiples pagos para procesamiento en lote
        order_ids = [1, 2, 3]
        payment_statuses = ["NOT_STARTED", "IN_PROGRESS", "NOT_STARTED"]

        created_payments = []
        for i, order_id in enumerate(order_ids):
            payment_data = {
                "isPayed": False,
                "paymentStatus": payment_statuses[i],
                "order": {"orderId": order_id},
            }

            response = make_request("POST", "/api/payments", data=payment_data)
            assert response.status_code == 200
            payment = response.json()
            created_payments.append(payment)
            cleanup_resources["payments"].append(payment["paymentId"])

        # 2. Procesar pagos en diferentes estados
        # Procesar los que están en NOT_STARTED
        not_started_payments = [
            p for p in created_payments if p["paymentStatus"] == "NOT_STARTED"
        ]
        for payment in not_started_payments:
            payment["paymentStatus"] = "IN_PROGRESS"
            response = make_request("PUT", "/api/payments", data=payment)
            assert response.status_code == 200

        # 3. Completar todos los pagos que están en IN_PROGRESS
        all_payments_response = make_request("GET", "/api/payments")
        assert all_payments_response.status_code == 200
        all_payments = all_payments_response.json()["collection"]

        # Filtrar solo nuestros pagos creados
        our_payment_ids = [p["paymentId"] for p in created_payments]
        our_payments = [p for p in all_payments if p["paymentId"] in our_payment_ids]

        for payment in our_payments:
            if payment["paymentStatus"] == "IN_PROGRESS":
                payment["isPayed"] = True
                payment["paymentStatus"] = "COMPLETED"
                response = make_request("PUT", "/api/payments", data=payment)
                assert response.status_code == 200

        # 4. Verificar que todos los pagos están completados
        for payment_id in our_payment_ids:
            check_response = make_request("GET", f"/api/payments/{payment_id}")
            assert check_response.status_code == 200
            checked_payment = check_response.json()
            assert checked_payment["isPayed"] is True
            assert checked_payment["paymentStatus"] == "COMPLETED"

        # 5. Generar "reporte" listando todos los pagos completados
        final_payments_response = make_request("GET", "/api/payments")
        assert final_payments_response.status_code == 200
        final_payments = final_payments_response.json()["collection"]

        # Contar pagos completados de nuestro lote
        completed_payments = [
            p
            for p in final_payments
            if p["paymentId"] in our_payment_ids and p["paymentStatus"] == "COMPLETED"
        ]

        # Verificar que todos nuestros pagos están completados
        assert len(completed_payments) == len(created_payments)

        # Verificar que cada pago completado tiene isPayed = True
        for payment in completed_payments:
            assert payment["isPayed"] is True
            assert payment["paymentStatus"] == "COMPLETED"
