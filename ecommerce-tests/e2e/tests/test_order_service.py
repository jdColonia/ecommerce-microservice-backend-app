"""
Pruebas E2E para el Order Service.
"""

import pytest
from conftest import make_request, set_current_service, generate_unique_id


class TestOrderServiceE2E:
    """
    Pruebas End-to-End para el Order Service.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("order-service")

    def test_e2e_complete_cart_lifecycle(self, cleanup_resources):
        """
        E2E Test 1: Ciclo de vida completo de un carrito.
        Crea carrito -> Obtiene carrito -> Actualiza carrito -> Lista carritos.
        """
        unique_id = generate_unique_id()

        # 1. Crear carrito
        cart_data = {"userId": 1}

        create_response = make_request("POST", "/api/carts", data=cart_data)
        assert create_response.status_code == 200
        created_cart = create_response.json()
        cart_id = created_cart["cartId"]
        cleanup_resources["carts"].append(cart_id)

        # Verificar datos del carrito creado
        assert created_cart["userId"] == cart_data["userId"]
        assert "cartId" in created_cart

        # 2. Obtener carrito por ID
        get_response = make_request("GET", f"/api/carts/{cart_id}")
        assert get_response.status_code == 200
        retrieved_cart = get_response.json()
        assert retrieved_cart["cartId"] == cart_id
        assert retrieved_cart["userId"] == cart_data["userId"]

        # 3. Actualizar carrito
        updated_data = created_cart.copy()
        updated_data["userId"] = 2

        update_response = make_request("PUT", "/api/carts", data=updated_data)
        assert update_response.status_code == 200
        updated_cart = update_response.json()
        assert updated_cart["userId"] == 2
        assert updated_cart["cartId"] == cart_id

        # 4. Listar todos los carritos
        all_carts_response = make_request("GET", "/api/carts")
        assert all_carts_response.status_code == 200
        carts_collection = all_carts_response.json()
        assert "collection" in carts_collection
        assert isinstance(carts_collection["collection"], list)

        # Verificar que nuestro carrito está en la lista
        cart_ids = [cart["cartId"] for cart in carts_collection["collection"]]
        assert cart_id in cart_ids

    def test_e2e_order_from_cart_workflow(self, cleanup_resources):
        """
        E2E Test 2: Flujo completo de orden desde carrito.
        Crea carrito -> Crea orden del carrito -> Obtiene orden -> Actualiza orden.
        """
        unique_id = generate_unique_id()

        # 1. Crear carrito primero
        cart_data = {"userId": 2001}

        cart_response = make_request("POST", "/api/carts", data=cart_data)
        assert cart_response.status_code == 200
        cart = cart_response.json()
        cart_id = cart["cartId"]
        cleanup_resources["carts"].append(cart_id)

        # 2. Crear orden del carrito
        order_data = {
            "orderDesc": f"Order_from_Cart_{unique_id}",
            "orderFee": 299.99,
            "cartDto": {"cartId": cart_id},
        }

        order_response = make_request("POST", "/api/orders", data=order_data)
        assert order_response.status_code == 200
        order = order_response.json()
        order_id = order["orderId"]
        cleanup_resources["orders"].append(order_id)

        # Verificar que la orden está asociada al carrito
        assert order["orderDesc"] == order_data["orderDesc"]
        assert order["orderFee"] == order_data["orderFee"]

        # 3. Obtener orden por ID
        get_order_response = make_request("GET", f"/api/orders/{order_id}")
        assert get_order_response.status_code == 200
        retrieved_order = get_order_response.json()
        assert retrieved_order["orderId"] == order_id
        assert retrieved_order["orderDesc"] == order_data["orderDesc"]

        # 4. Actualizar orden
        updated_order = order.copy()
        updated_order["orderDesc"] = f"Updated_Order_{unique_id}"
        updated_order["orderFee"] = 349.99

        update_order_response = make_request("PUT", "/api/orders", data=updated_order)
        assert update_order_response.status_code == 200
        final_order = update_order_response.json()
        assert final_order["orderDesc"] == f"Updated_Order_{unique_id}"
        assert final_order["orderFee"] == 349.99

    def test_e2e_multiple_orders_management(self, cleanup_resources):
        """
        E2E Test 3: Gestión de múltiples órdenes.
        Crea múltiples carritos -> Crea múltiples órdenes -> Lista órdenes -> Verifica órdenes.
        """
        unique_id = generate_unique_id()

        # 1. Crear múltiples carritos
        carts_data = [{"userId": 1}, {"userId": 2}, {"userId": 3}]

        created_carts = []
        for cart_data in carts_data:
            response = make_request("POST", "/api/carts", data=cart_data)
            assert response.status_code == 200
            cart = response.json()
            created_carts.append(cart)
            cleanup_resources["carts"].append(cart["cartId"])

        # 2. Crear órdenes para cada carrito
        orders_data = [
            {
                "orderDesc": f"Electronics_Order_{unique_id}",
                "orderFee": 599.99,
                "cartDto": {"cartId": created_carts[0]["cartId"]},
            },
            {
                "orderDesc": f"Books_Order_{unique_id}",
                "orderFee": 79.99,
                "cartDto": {"cartId": created_carts[1]["cartId"]},
            },
            {
                "orderDesc": f"Clothing_Order_{unique_id}",
                "orderFee": 199.99,
                "cartDto": {"cartId": created_carts[2]["cartId"]},
            },
        ]

        created_orders = []
        for order_data in orders_data:
            response = make_request("POST", "/api/orders", data=order_data)
            assert response.status_code == 200
            order = response.json()
            created_orders.append(order)
            cleanup_resources["orders"].append(order["orderId"])

        # 3. Listar todas las órdenes
        all_orders_response = make_request("GET", "/api/orders")
        assert all_orders_response.status_code == 200
        orders_collection = all_orders_response.json()
        assert "collection" in orders_collection
        assert isinstance(orders_collection["collection"], list)

        # 4. Verificar que todas las órdenes creadas están en la lista
        all_order_ids = [order["orderId"] for order in orders_collection["collection"]]
        for created_order in created_orders:
            assert created_order["orderId"] in all_order_ids

        # 5. Verificar órdenes individualmente
        for created_order in created_orders:
            specific_order_response = make_request(
                "GET", f"/api/orders/{created_order['orderId']}"
            )
            assert specific_order_response.status_code == 200
            retrieved_order = specific_order_response.json()
            assert retrieved_order["orderId"] == created_order["orderId"]
            assert retrieved_order["orderDesc"] == created_order["orderDesc"]

    def test_e2e_order_fee_calculations(self, cleanup_resources):
        """
        E2E Test 4: Cálculos y gestión de tarifas de órdenes.
        Crea carrito y orden -> Actualiza tarifas -> Simula descuentos -> Verifica totales.
        """
        unique_id = generate_unique_id()

        # 1. Crear carrito
        cart_data = {"userId": 4}

        cart_response = make_request("POST", "/api/carts", data=cart_data)
        assert cart_response.status_code == 200
        cart = cart_response.json()
        cart_id = cart["cartId"]
        cleanup_resources["carts"].append(cart_id)

        # 2. Crear orden con tarifa inicial
        order_data = {
            "orderDesc": f"Initial_Order_{unique_id}",
            "orderFee": 100.00,
            "cartDto": {"cartId": cart_id},
        }

        order_response = make_request("POST", "/api/orders", data=order_data)
        assert order_response.status_code == 200
        order = order_response.json()
        order_id = order["orderId"]
        cleanup_resources["orders"].append(order_id)

        # Verificar tarifa inicial
        assert order["orderFee"] == 100.00

        # 3. Simular agregar más productos (aumentar tarifa)
        updated_order = order.copy()
        updated_order["orderFee"] = 150.00
        updated_order["orderDesc"] = f"Added_Products_{unique_id}"

        update_response = make_request("PUT", "/api/orders", data=updated_order)
        assert update_response.status_code == 200
        updated_order_result = update_response.json()
        assert updated_order_result["orderFee"] == 150.00

        # 4. Aplicar descuento
        discount_order = updated_order_result.copy()
        discount_order["orderFee"] = 120.00  # 20% descuento
        discount_order["orderDesc"] = f"Discounted_Order_{unique_id}"

        discount_response = make_request("PUT", "/api/orders", data=discount_order)
        assert discount_response.status_code == 200
        discounted_order = discount_response.json()
        assert discounted_order["orderFee"] == 120.00
        assert discounted_order["orderDesc"] == f"Discounted_Order_{unique_id}"

        # 5. Agregar impuestos y tarifas de envío
        final_order = discounted_order.copy()
        final_order["orderFee"] = 135.00  # Agregar 15.00 de impuestos y envío
        final_order["orderDesc"] = f"Final_Order_{unique_id}"

        final_response = make_request("PUT", "/api/orders", data=final_order)
        assert final_response.status_code == 200
        final_order_result = final_response.json()
        assert final_order_result["orderFee"] == 135.00

    def test_e2e_cart_and_order_bulk_operations(self, cleanup_resources):
        """
        E2E Test 5: Operaciones en lote con carritos y órdenes.
        Crea múltiples carritos -> Crea órdenes por lotes -> Actualiza por ID -> Elimina selectivamente.
        """
        unique_id = generate_unique_id()

        # 1. Crear múltiples carritos para diferentes usuarios
        user_ids = [1, 2, 3]
        created_carts = []

        for user_id in user_ids:
            cart_data = {"userId": user_id}
            response = make_request("POST", "/api/carts", data=cart_data)
            assert response.status_code == 200
            cart = response.json()
            created_carts.append(cart)
            cleanup_resources["carts"].append(cart["cartId"])

        # 2. Crear órdenes para cada carrito
        order_descriptions = [
            f"Electronics_Bulk_{unique_id}",
            f"Home_Garden_Bulk_{unique_id}",
            f"Sports_Outdoor_Bulk_{unique_id}",
            f"Health_Beauty_Bulk_{unique_id}",
            f"Automotive_Bulk_{unique_id}",
        ]

        order_fees = [299.99, 149.99, 199.99]

        created_orders = []
        for i, cart in enumerate(created_carts):
            order_data = {
                "orderDesc": order_descriptions[i],
                "orderFee": order_fees[i],
                "cartDto": {"cartId": cart["cartId"]},
            }

            response = make_request("POST", "/api/orders", data=order_data)
            assert response.status_code == 200
            order = response.json()
            created_orders.append(order)
            cleanup_resources["orders"].append(order["orderId"])

        # 3. Actualizar algunas órdenes usando updateById
        for i in range(1, 2):
            order = created_orders[i]
            original_fee = order["orderFee"]
            update_data = {
                "orderDesc": f"Updated_{order['orderDesc']}",
                "orderFee": original_fee + 50.00,  # Agregar 50.00 a cada orden
            }

            update_response = make_request(
                "PUT", f"/api/orders/{order['orderId']}", data=update_data
            )
            assert update_response.status_code == 200

            # Verificar que la respuesta de actualización es válida
            updated_order_response = update_response.json()
            assert "orderId" in updated_order_response
            assert updated_order_response["orderId"] == order["orderId"]

        # 4. Actualizar algunos carritos usando updateById
        for i in range(1, 2):
            cart = created_carts[i]
            new_user_id = cart["userId"] + 1  # Cambiar a nuevo usuario

            update_data = {"userId": new_user_id}

            update_response = make_request(
                "PUT", f"/api/carts/{cart['cartId']}", data=update_data
            )
            assert update_response.status_code == 200

        # 5. Verificar todas las órdenes y carritos
        # Verificar órdenes
        all_orders_response = make_request("GET", "/api/orders")
        assert all_orders_response.status_code == 200
        orders_collection = all_orders_response.json()

        order_ids_in_response = [
            order["orderId"] for order in orders_collection["collection"]
        ]
        for created_order in created_orders:
            assert created_order["orderId"] in order_ids_in_response

        # Verificar carritos
        all_carts_response = make_request("GET", "/api/carts")
        assert all_carts_response.status_code == 200
        carts_collection = all_carts_response.json()

        cart_ids_in_response = [
            cart["cartId"] for cart in carts_collection["collection"]
        ]
        for created_cart in created_carts:
            assert created_cart["cartId"] in cart_ids_in_response

        # 6. Verificar que las órdenes y carritos siguen siendo accesibles
        for i in range(1, 2):
            order_id = created_orders[i]["orderId"]
            check_response = make_request("GET", f"/api/orders/{order_id}")
            assert check_response.status_code == 200
            checked_order = check_response.json()

            # Solo verificar que la orden existe y es accesible
            assert "orderId" in checked_order
            assert checked_order["orderId"] == order_id

            # Verificar que los carritos también siguen siendo accesibles
            cart_id = created_carts[i]["cartId"]
            cart_check_response = make_request("GET", f"/api/carts/{cart_id}")
            assert cart_check_response.status_code == 200
            checked_cart = cart_check_response.json()
            assert "cartId" in checked_cart
            assert checked_cart["cartId"] == cart_id
