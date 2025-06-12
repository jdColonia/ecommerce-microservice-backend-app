"""
Prueba E2E del flujo completo de compra.
"""

import pytest
import logging
from utils.api_client import ApiClient
from utils.assertions import assert_status_code, assert_contains_keys, assert_order_status
from flows.checkout_flow import CheckoutFlow
from fixtures.user_fixtures import test_user_with_address, authenticated_api_client
from fixtures.product_fixtures import test_product

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def checkout_flow(authenticated_api_client):
    """Fixture para el flujo de checkout."""
    return CheckoutFlow(authenticated_api_client)

def test_complete_purchase_flow(authenticated_api_client, checkout_flow, test_user_with_address, test_product):
    """
    Prueba E2E: flujo completo de compra.
    
    Este test verifica que un usuario pueda:
    1. Añadir productos al carrito
    2. Crear una orden
    3. Procesar un pago
    4. Recibir confirmación de envío
    """
    logger.info("Iniciando prueba de flujo completo de compra")
    
    user = test_user_with_address
    product = test_product
    user_id = user.get("id")
    product_id = product.get("id")
    shipping_address_id = user.get("address", {}).get("id")
    
    # Configurar método de pago para la prueba
    payment_method = {
        "method": "CREDIT_CARD",
        "amount": product.get("price"),
        "details": {
            "cardNumber": "4111111111111111",
            "expiryMonth": "12",
            "expiryYear": "2030",
            "cvv": "123"
        }
    }
    
    # Ejecutar flujo completo de checkout
    result = checkout_flow.complete_checkout(
        user_id=user_id,
        product_id=product_id,
        quantity=1,
        shipping_address_id=shipping_address_id,
        payment_method=payment_method
    )
    
    # Verificar resultados
    assert "cart" in result, "El carrito no se creó correctamente"
    assert "order" in result, "La orden no se creó correctamente"
    assert "payment" in result, "El pago no se procesó correctamente"
    assert "shipping" in result, "El envío no se creó correctamente"
    
    # Verificar detalles del carrito
    cart = result.get("cart")
    assert_contains_keys(cart, ["id", "userId", "items"])
    
    # Verificar detalles de la orden
    order = result.get("order")
    order_id = order.get("id")
    assert_contains_keys(order, ["id", "userId", "totalAmount", "status"])
    
    # Verificar estado de la orden
    order_response = authenticated_api_client.request("GET", f"/api/orders/{order_id}")
    assert_status_code(order_response, 200)
    
    # Verificar que el estado haya cambiado a PAID o similar
    order_status = order_response.json().get("status")
    assert order_status in ["PAID", "PROCESSING", "SHIPPED"], f"Estado de orden inesperado: {order_status}"
    
    logger.info(f"Prueba de flujo completo de compra finalizada con éxito: Orden {order_id}")

def test_add_product_to_cart(authenticated_api_client, checkout_flow, test_product):
    """
    Prueba E2E: añadir producto al carrito.
    """
    logger.info("Iniciando prueba de añadir producto al carrito")
    
    product_id = test_product.get("id")
    quantity = 2
    
    # Añadir producto al carrito
    cart = checkout_flow.add_product_to_cart(product_id, quantity)
    
    # Verificar que el producto se haya añadido correctamente
    assert_contains_keys(cart, ["id", "items"])
    
    # Verificar que el carrito contiene el producto con la cantidad correcta
    items = cart.get("items", [])
    assert len(items) > 0, "El carrito no tiene items"
    
    product_in_cart = False
    for item in items:
        if item.get("productId") == product_id:
            assert item.get("quantity") == quantity, f"Cantidad incorrecta: {item.get('quantity')} != {quantity}"
            product_in_cart = True
            break
    
    assert product_in_cart, f"El producto {product_id} no se encontró en el carrito"
    
    logger.info("Prueba de añadir producto al carrito finalizada con éxito")

def test_update_cart_quantity(authenticated_api_client, checkout_flow, test_product):
    """
    Prueba E2E: actualizar cantidad en el carrito.
    """
    logger.info("Iniciando prueba de actualizar cantidad en el carrito")
    
    product_id = test_product.get("id")
    initial_quantity = 1
    updated_quantity = 3
    
    # Añadir producto al carrito
    cart = checkout_flow.add_product_to_cart(product_id, initial_quantity)
    cart_id = cart.get("id")
    
    # Actualizar cantidad
    updated_cart = checkout_flow.update_cart_quantity(cart_id, product_id, updated_quantity)
    
    # Verificar que la cantidad se haya actualizado correctamente
    items = updated_cart.get("items", [])
    
    product_updated = False
    for item in items:
        if item.get("productId") == product_id:
            assert item.get("quantity") == updated_quantity, \
                f"Cantidad no actualizada: {item.get('quantity')} != {updated_quantity}"
            product_updated = True
            break
    
    assert product_updated, f"El producto {product_id} no se encontró en el carrito actualizado"
    
    logger.info("Prueba de actualizar cantidad en el carrito finalizada con éxito")
