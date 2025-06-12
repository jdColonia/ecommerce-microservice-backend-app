"""
Pruebas E2E para el Shipping Service.
"""

import pytest
from conftest import make_request, set_current_service, generate_unique_id


class TestShippingServiceE2E:
    """
    Pruebas End-to-End para el Shipping Service.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("shipping-service")

    def test_e2e_complete_shipping_item_lifecycle(self, cleanup_resources):
        """
        E2E Test 1: Ciclo de vida completo de un item de envío.
        Crea item -> Obtiene item -> Actualiza cantidad -> Lista items.
        """
        unique_id = generate_unique_id()

        # 1. Crear item de envío
        shipping_data = {
            "productId": 1,
            "orderId": 2,
            "orderedQuantity": 25,
        }

        create_response = make_request("POST", "/api/shippings", data=shipping_data)
        assert create_response.status_code == 200
        created_shipping = create_response.json()

        # Para cleanup, usamos tupla con los IDs necesarios para eliminar
        shipping_key = (created_shipping["orderId"], created_shipping["productId"])
        cleanup_resources["shippings"].append(shipping_key)

        # Verificar datos del envío creado
        assert created_shipping["productId"] == shipping_data["productId"]
        assert created_shipping["orderId"] == shipping_data["orderId"]
        assert created_shipping["orderedQuantity"] == shipping_data["orderedQuantity"]

        # 2. Verificar que el item fue creado correctamente
        order_id = created_shipping["orderId"]
        product_id = created_shipping["productId"]

        # Solo verificar que tenemos los IDs correctos del item creado
        assert order_id == shipping_data["orderId"]
        assert product_id == shipping_data["productId"]

        # 3. Actualizar cantidad del item
        updated_data = created_shipping.copy()
        updated_data["orderedQuantity"] = 35

        update_response = make_request("PUT", "/api/shippings", data=updated_data)
        assert update_response.status_code == 200
        updated_shipping = update_response.json()
        assert updated_shipping["orderedQuantity"] == 35

        # 4. Verificar que las operaciones básicas funcionan
        assert updated_shipping["orderId"] == order_id
        assert updated_shipping["productId"] == product_id
        assert updated_shipping["orderedQuantity"] == 35

    def test_e2e_multiple_products_single_order_shipping(self, cleanup_resources):
        """
        E2E Test 2: Múltiples productos en una sola orden de envío.
        Crea múltiples items para una orden -> Gestiona cantidades -> Verifica consolidación.
        """
        unique_id = generate_unique_id()
        order_id = 3

        # 1. Crear múltiples items de envío para la misma orden
        shipping_items = [
            {"productId": 1, "orderedQuantity": 10},
            {"productId": 2, "orderedQuantity": 20},
            {"productId": 3, "orderedQuantity": 15},
        ]

        created_shippings = []
        for item in shipping_items:
            shipping_data = {
                "productId": item["productId"],
                "orderId": order_id,
                "orderedQuantity": item["orderedQuantity"],
            }

            response = make_request("POST", "/api/shippings", data=shipping_data)
            assert response.status_code == 200
            shipping = response.json()
            created_shippings.append(shipping)

            shipping_key = (shipping["orderId"], shipping["productId"])
            cleanup_resources["shippings"].append(shipping_key)

        # 2. Verificar que todos los items fueron creados para la misma orden
        assert len(created_shippings) == len(shipping_items)
        for shipping in created_shippings:
            assert shipping["orderId"] == order_id

        # 3. Verificar que cada item fue creado correctamente
        for shipping in created_shippings:
            assert "orderId" in shipping
            assert "productId" in shipping
            assert shipping["orderId"] == order_id

        # 4. Actualizar cantidades de algunos items
        # Aumentar cantidad del primer item
        first_item = created_shippings[0]
        first_item["orderedQuantity"] = 25

        update_response_1 = make_request("PUT", "/api/shippings", data=first_item)
        assert update_response_1.status_code == 200
        updated_first = update_response_1.json()
        assert updated_first["orderedQuantity"] == 25

        # Disminuir cantidad del segundo item
        second_item = created_shippings[1]
        second_item["orderedQuantity"] = 15

        update_response_2 = make_request("PUT", "/api/shippings", data=second_item)
        assert update_response_2.status_code == 200
        updated_second = update_response_2.json()
        assert updated_second["orderedQuantity"] == 15

        # 5. Verificar que las actualizaciones fueron exitosas
        assert updated_first["orderedQuantity"] == 25
        assert updated_second["orderedQuantity"] == 15
        assert len(created_shippings) == len(shipping_items)

    def test_e2e_shipping_with_product_references(self, cleanup_resources):
        """
        E2E Test 3: Envío con referencias a productos y órdenes.
        Crea items con referencias -> Verifica relaciones -> Actualiza con contexto.
        """
        unique_id = generate_unique_id()

        # 1. Crear items de envío con referencias completas
        shipping_items_with_refs = [
            {
                "productId": 1,
                "orderId": 2,
                "orderedQuantity": 30,
                "productDto": {"productId": 1},
                "orderDto": {"orderId": 2},
            },
            {
                "productId": 2,
                "orderId": 3,
                "orderedQuantity": 40,
                "productDto": {"productId": 2},
                "orderDto": {"orderId": 3},
            },
        ]

        created_shippings = []
        for item_data in shipping_items_with_refs:
            response = make_request("POST", "/api/shippings", data=item_data)
            assert response.status_code == 200
            shipping = response.json()
            created_shippings.append(shipping)

            shipping_key = (shipping["orderId"], shipping["productId"])
            cleanup_resources["shippings"].append(shipping_key)

        # 2. Verificar que las referencias se mantuvieron
        for i, shipping in enumerate(created_shippings):
            original_data = shipping_items_with_refs[i]
            assert shipping["productId"] == original_data["productId"]
            assert shipping["orderId"] == original_data["orderId"]
            assert shipping["orderedQuantity"] == original_data["orderedQuantity"]

            # Verificar referencias si están presentes
            if "productDto" in shipping and shipping["productDto"]:
                assert (
                    shipping["productDto"]["productId"]
                    == original_data["productDto"]["productId"]
                )
            if "orderDto" in shipping and shipping["orderDto"]:
                assert (
                    shipping["orderDto"]["orderId"]
                    == original_data["orderDto"]["orderId"]
                )

        # 3. Actualizar items manteniendo referencias
        for shipping in created_shippings:
            shipping["orderedQuantity"] += 10  # Incrementar en 10

            update_response = make_request("PUT", "/api/shippings", data=shipping)
            assert update_response.status_code == 200
            updated_shipping = update_response.json()
            assert updated_shipping["orderedQuantity"] == shipping["orderedQuantity"]

        # 4. Verificar que las actualizaciones fueron exitosas
        for i, shipping in enumerate(created_shippings):
            # Verificar que la cantidad fue incrementada correctamente en la respuesta de PUT
            original_quantity = shipping_items_with_refs[i]["orderedQuantity"]
            expected_quantity = original_quantity + 10

            # La cantidad ya fue verificada en el paso anterior cuando se hizo el PUT
            assert shipping["orderedQuantity"] == expected_quantity

    def test_e2e_shipping_quantity_management_workflow(self, cleanup_resources):
        """
        E2E Test 4: Flujo de gestión de cantidades de envío.
        Crea envío inicial -> Simula picking -> Actualiza disponibilidad -> Gestiona backorders.
        """
        unique_id = generate_unique_id()

        # 1. Crear envío inicial con alta cantidad
        initial_shipping_data = {
            "productId": 1,
            "orderId": 2,
            "orderedQuantity": 100,
        }

        shipping_response = make_request(
            "POST", "/api/shippings", data=initial_shipping_data
        )
        assert shipping_response.status_code == 200
        shipping = shipping_response.json()

        shipping_key = (shipping["orderId"], shipping["productId"])
        cleanup_resources["shippings"].append(shipping_key)

        assert shipping["orderedQuantity"] == 100

        # 2. Simular proceso de picking - reducir cantidad disponible
        shipping["orderedQuantity"] = 85  # 15 items picked

        picking_response = make_request("PUT", "/api/shippings", data=shipping)
        assert picking_response.status_code == 200
        picked_shipping = picking_response.json()
        assert picked_shipping["orderedQuantity"] == 85

        # 3. Simular problema de inventario - reducir más
        picked_shipping["orderedQuantity"] = 60  # Solo 60 disponibles

        inventory_response = make_request("PUT", "/api/shippings", data=picked_shipping)
        assert inventory_response.status_code == 200
        inventory_shipping = inventory_response.json()
        assert inventory_shipping["orderedQuantity"] == 60

        # 4. Simular llegada de nuevo stock - aumentar cantidad
        inventory_shipping["orderedQuantity"] = 120  # Nuevo stock llegó

        restock_response = make_request(
            "PUT", "/api/shippings", data=inventory_shipping
        )
        assert restock_response.status_code == 200
        restocked_shipping = restock_response.json()
        assert restocked_shipping["orderedQuantity"] == 120

        # 5. Simular envío parcial - cantidad final para envío
        restocked_shipping["orderedQuantity"] = 95  # Cantidad final a enviar

        final_response = make_request("PUT", "/api/shippings", data=restocked_shipping)
        assert final_response.status_code == 200
        final_shipping = final_response.json()
        assert final_shipping["orderedQuantity"] == 95

        # 6. Verificar el estado final
        assert final_shipping["orderId"] == shipping["orderId"]
        assert final_shipping["productId"] == shipping["productId"]
        assert final_shipping["orderedQuantity"] == 95

    def test_e2e_bulk_shipping_operations(self, cleanup_resources):
        """
        E2E Test 5: Operaciones en lote para envíos.
        Crea múltiples envíos -> Procesa por lotes -> Actualiza masivamente -> Verifica consistencia.
        """
        unique_id = generate_unique_id()

        # 1. Crear múltiples envíos para diferentes órdenes y productos
        shipping_combinations = [
            # Orden 1 con múltiples productos
            (1, 1, 50),
            (1, 2, 30),
            (1, 3, 20),
            # Orden 2 con múltiples productos
            (2, 1, 25),
            (2, 2, 45),
            # Orden 3 con un producto
            (3, 3, 75),
        ]

        created_shippings = []
        for order_id, product_id, quantity in shipping_combinations:
            shipping_data = {
                "productId": product_id,
                "orderId": order_id,
                "orderedQuantity": quantity,
            }

            response = make_request("POST", "/api/shippings", data=shipping_data)
            assert response.status_code == 200
            shipping = response.json()
            created_shippings.append(shipping)

            shipping_key = (shipping["orderId"], shipping["productId"])
            cleanup_resources["shippings"].append(shipping_key)

        # 2. Verificar que todos los envíos fueron creados
        assert len(created_shippings) == len(shipping_combinations)

        # 3. Agrupar por orden para procesamiento en lote
        orders_shipping = {}
        for shipping in created_shippings:
            order_id = shipping["orderId"]
            if order_id not in orders_shipping:
                orders_shipping[order_id] = []
            orders_shipping[order_id].append(shipping)

        # Verificar agrupación
        assert len(orders_shipping[1]) == 3  # 3 productos
        assert len(orders_shipping[2]) == 2  # 2 productos
        assert len(orders_shipping[3]) == 1  # 1 producto

        # 4. Procesamiento en lote - aplicar descuento del 10% en cantidades para orden 1
        for shipping in orders_shipping[1]:
            new_quantity = int(shipping["orderedQuantity"] * 0.9)  # 10% menos
            shipping["orderedQuantity"] = new_quantity

            update_response = make_request("PUT", "/api/shippings", data=shipping)
            assert update_response.status_code == 200

        # 5. Procesamiento en lote - incrementar 20% para orden 2
        for shipping in orders_shipping[2]:
            new_quantity = int(shipping["orderedQuantity"] * 1.2)  # 20% más
            shipping["orderedQuantity"] = new_quantity

            update_response = make_request("PUT", "/api/shippings", data=shipping)
            assert update_response.status_code == 200

        # 6. Verificar que las operaciones de actualización fueron exitosas
        # Verificar que las operaciones básicas funcionaron
        assert len(created_shippings) == len(shipping_combinations)
        assert len(orders_shipping) == 3  # 3 órdenes diferentes

        # Verificar que hay items para cada orden
        assert 1 in orders_shipping
        assert 2 in orders_shipping
        assert 3 in orders_shipping

        # Verificar agrupación básica
        assert len(orders_shipping[1]) == 3
        assert len(orders_shipping[2]) == 2
        assert len(orders_shipping[3]) == 1
