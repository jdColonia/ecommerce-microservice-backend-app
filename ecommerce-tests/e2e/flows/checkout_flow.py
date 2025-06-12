"""
Flujo completo de compra (checkout) desde selección de producto hasta pago.
"""

import logging
import time
from typing import Dict, Any, List, Optional
from utils.api_client import ApiClient

logger = logging.getLogger(__name__)

class CheckoutFlow:
    """Implementa el flujo completo de compra."""
    
    def __init__(self, api_client: ApiClient):
        self.api = api_client
    
    def add_product_to_cart(self, product_id: int, quantity: int = 1) -> Dict[str, Any]:
        """
        Añade un producto al carrito.
        
        Args:
            product_id (int): ID del producto
            quantity (int): Cantidad a añadir
            
        Returns:
            dict: Datos del carrito actualizado
        """
        logger.info(f"Añadiendo producto {product_id} al carrito (cantidad: {quantity})")
        
        response = self.api.request(
            method="POST",
            endpoint="/api/carts",
            data={"productId": product_id, "quantity": quantity}
        )
        response.raise_for_status()
        cart = response.json()
        
        logger.info(f"Producto {product_id} añadido al carrito {cart.get('id')}")
        return cart
    
    def update_cart_quantity(self, cart_id: int, product_id: int, quantity: int) -> Dict[str, Any]:
        """
        Actualiza la cantidad de un producto en el carrito.
        
        Args:
            cart_id (int): ID del carrito
            product_id (int): ID del producto
            quantity (int): Nueva cantidad
            
        Returns:
            dict: Datos del carrito actualizado
        """
        logger.info(f"Actualizando carrito {cart_id}, producto {product_id} a cantidad {quantity}")
        
        response = self.api.request(
            method="PUT",
            endpoint="/api/carts",
            data={"id": cart_id, "productId": product_id, "quantity": quantity}
        )
        response.raise_for_status()
        cart = response.json()
        
        logger.info(f"Carrito {cart_id} actualizado")
        return cart
    
    def create_order(self, cart_id: int, user_id: int, shipping_address_id: int) -> Dict[str, Any]:
        """
        Crea una orden a partir del carrito.
        
        Args:
            cart_id (int): ID del carrito
            user_id (int): ID del usuario
            shipping_address_id (int): ID de la dirección de envío
            
        Returns:
            dict: Datos de la orden creada
        """
        logger.info(f"Creando orden para carrito {cart_id}, usuario {user_id}")
        
        response = self.api.request(
            method="POST",
            endpoint="/api/orders",
            data={
                "cartId": cart_id,
                "userId": user_id,
                "shippingAddressId": shipping_address_id
            }
        )
        response.raise_for_status()
        order = response.json()
        
        logger.info(f"Orden {order.get('id')} creada desde carrito {cart_id}")
        return order
    
    def process_payment(self, order_id: int, payment_method: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa el pago de una orden.
        
        Args:
            order_id (int): ID de la orden
            payment_method (dict): Datos del método de pago
            
        Returns:
            dict: Datos del pago procesado
        """
        logger.info(f"Procesando pago para orden {order_id}")
        
        payment_data = {
            "orderId": order_id,
            "method": payment_method.get("method"),
            "amount": payment_method.get("amount"),
            "details": payment_method.get("details")
        }
        
        response = self.api.request(
            method="POST",
            endpoint="/api/payments",
            data=payment_data
        )
        response.raise_for_status()
        payment = response.json()
        
        logger.info(f"Pago {payment.get('id')} procesado para orden {order_id}")
        return payment
    
    def create_shipping(self, order_id: int) -> Dict[str, Any]:
        """
        Crea un envío para una orden.
        
        Args:
            order_id (int): ID de la orden
            
        Returns:
            dict: Datos del envío creado
        """
        logger.info(f"Creando envío para orden {order_id}")
        
        response = self.api.request(
            method="POST",
            endpoint="/api/shippings",
            data={"orderId": order_id}
        )
        response.raise_for_status()
        shipping = response.json()
        
        logger.info(f"Envío {shipping.get('id')} creado para orden {order_id}")
        return shipping
    
    def complete_checkout(
        self,
        user_id: int,
        product_id: int,
        quantity: int,
        shipping_address_id: int,
        payment_method: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Ejecuta el flujo completo de checkout.
        
        Args:
            user_id (int): ID del usuario
            product_id (int): ID del producto
            quantity (int): Cantidad a comprar
            shipping_address_id (int): ID de la dirección de envío
            payment_method (dict): Datos del método de pago
            
        Returns:
            dict: Resultado del flujo completo
        """
        logger.info(f"Iniciando flujo completo de checkout para usuario {user_id}, producto {product_id}")
        
        # 1. Añadir producto al carrito
        cart = self.add_product_to_cart(product_id, quantity)
        cart_id = cart.get("id")
        
        # 2. Crear orden desde el carrito
        order = self.create_order(cart_id, user_id, shipping_address_id)
        order_id = order.get("id")
        
        # 3. Procesar pago
        payment = self.process_payment(order_id, payment_method)
        
        # 4. Crear envío
        shipping = self.create_shipping(order_id)
        
        # Devolver resultado del flujo completo
        logger.info(f"Flujo de checkout completado: Orden {order_id}")
        
        return {
            "cart": cart,
            "order": order,
            "payment": payment,
            "shipping": shipping
        }
