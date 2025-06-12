"""
Usuarios que realizan compras completas.
"""

import random
import logging
import json
from locust import task, tag, SequentialTaskSet
from faker import Faker
from locustfiles.base_user import BaseUser
from config import settings

logger = logging.getLogger(__name__)
fake = Faker()

class BuyerUser(BaseUser):
    """
    Usuario que realiza compras completas.
    Requiere autenticación.
    """
    
    auth_required = True
    weight = settings.BUYER_USER_WEIGHT
    username = settings.USER_USERNAME
    password = settings.USER_PASSWORD
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cart_id = None
        self.product_id = None
        self.address_id = None
        self.order_id = None
    
    @tag('user', 'address')
    @task(1)
    def view_addresses(self):
        """Ver direcciones del usuario."""
        with self.make_request_with_retry(
            'get',
            f"{settings.ENDPOINTS['users']}/{self.user_id}/addresses",
            name="View User Addresses"
        ) as response:
            if response.status_code == 200:
                addresses = response.json()
                if addresses:
                    self.address_id = addresses[0].get('id')
                    logger.debug(f"Obtenidas {len(addresses)} direcciones")
    
    @tag('user', 'profile')
    @task(1)
    def view_profile(self):
        """Ver perfil del usuario."""
        with self.make_request_with_retry(
            'get',
            f"{settings.ENDPOINTS['users']}/{self.user_id}",
            name="View User Profile"
        ) as response:
            if response.status_code == 200:
                profile = response.json()
                logger.debug(f"Visto perfil de usuario {self.user_id}")
    
    @tag('cart')
    @task(3)
    def view_cart(self):
        """Ver carrito del usuario."""
        with self.make_request_with_retry(
            'get',
            f"{settings.ENDPOINTS['carts']}?userId={self.user_id}",
            name="View Cart"
        ) as response:
            if response.status_code == 200:
                carts = response.json()
                if carts:
                    self.cart_id = carts[0].get('id')
                    logger.debug(f"Visto carrito {self.cart_id}")
    
    @tag('orders')
    @task(2)
    def view_orders(self):
        """Ver órdenes del usuario."""
        with self.make_request_with_retry(
            'get',
            f"{settings.ENDPOINTS['orders']}?userId={self.user_id}",
            name="View Orders"
        ) as response:
            if response.status_code == 200:
                orders = response.json()
                logger.debug(f"Obtenidas {len(orders)} órdenes")
    
    @tag('checkout')
    @task(5)
    def complete_purchase(self):
        """Realizar una compra completa."""
        self.schedule_task(CheckoutProcess)
    
    @tag('favorites')
    @task(2)
    def manage_favorites(self):
        """Gestionar favoritos."""
        # Obtener productos
        with self.make_request_with_retry(
            'get',
            settings.ENDPOINTS['products'],
            name="Get Products For Favorites"
        ) as response:
            if response.status_code == 200:
                products = response.json()
                if products:
                    # Seleccionar un producto aleatorio
                    product = random.choice(products)
                    product_id = product.get('id')
                    
                    # Añadir a favoritos
                    favourite_data = {
                        "userId": self.user_id,
                        "productId": product_id,
                        "likeDate": "2025-05-30T12:00:00Z"
                    }
                    
                    with self.make_request_with_retry(
                        'post',
                        settings.ENDPOINTS['favorites'],
                        json=favourite_data,
                        name="Add To Favorites"
                    ) as add_response:
                        if add_response.status_code in (200, 201):
                            logger.debug(f"Producto {product_id} añadido a favoritos")
                            
                            # Eliminar de favoritos
                            with self.make_request_with_retry(
                                'delete',
                                f"{settings.ENDPOINTS['favorites']}/delete",
                                json=favourite_data,
                                name="Remove From Favorites"
                            ) as delete_response:
                                if delete_response.status_code in (200, 204):
                                    logger.debug(f"Producto {product_id} eliminado de favoritos")


class CheckoutProcess(SequentialTaskSet):
    """
    Secuencia de tareas para realizar una compra completa.
    """
    
    @task
    def add_to_cart(self):
        """Añadir producto al carrito."""
        # Obtener productos
        with self.parent.make_request_with_retry(
            'get',
            settings.ENDPOINTS['products'],
            name="Get Products For Cart"
        ) as response:
            if response.status_code == 200:
                products = response.json()
                if products:
                    # Seleccionar un producto aleatorio
                    product = random.choice(products)
                    self.parent.product_id = product.get('id')
                    
                    # Añadir al carrito
                    cart_data = {
                        "userId": self.parent.user_id,
                        "productId": self.parent.product_id,
                        "quantity": random.randint(1, 5)
                    }
                    
                    with self.parent.make_request_with_retry(
                        'post',
                        settings.ENDPOINTS['carts'],
                        json=cart_data,
                        name="Add To Cart"
                    ) as cart_response:
                        if cart_response.status_code in (200, 201):
                            cart = cart_response.json()
                            self.parent.cart_id = cart.get('id')
                            logger.debug(f"Producto {self.parent.product_id} añadido al carrito {self.parent.cart_id}")
    
    @task
    def create_order(self):
        """Crear orden desde el carrito."""
        if not self.parent.cart_id or not self.parent.address_id:
            # Obtener direcciones si no tenemos una
            if not self.parent.address_id:
                with self.parent.make_request_with_retry(
                    'get',
                    f"{settings.ENDPOINTS['users']}/{self.parent.user_id}/addresses",
                    name="Get Addresses For Order"
                ) as addr_response:
                    if addr_response.status_code == 200:
                        addresses = addr_response.json()
                        if addresses:
                            self.parent.address_id = addresses[0].get('id')
            
            # Si aún no tenemos dirección o carrito, cancelamos
            if not self.parent.cart_id or not self.parent.address_id:
                logger.error("No se puede crear orden: falta carrito o dirección")
                return
        
        # Crear orden
        order_data = {
            "userId": self.parent.user_id,
            "cartId": self.parent.cart_id,
            "shippingAddressId": self.parent.address_id,
            "status": "PENDING"
        }
        
        with self.parent.make_request_with_retry(
            'post',
            settings.ENDPOINTS['orders'],
            json=order_data,
            name="Create Order"
        ) as order_response:
            if order_response.status_code in (200, 201):
                order = order_response.json()
                self.parent.order_id = order.get('id')
                logger.debug(f"Orden {self.parent.order_id} creada desde carrito {self.parent.cart_id}")
    
    @task
    def process_payment(self):
        """Procesar pago."""
        if not self.parent.order_id:
            logger.error("No se puede procesar pago: falta orden")
            return
        
        # Procesar pago
        payment_data = {
            "orderId": self.parent.order_id,
            "method": "CREDIT_CARD",
            "amount": 99.99,  # Esto debería venir de la orden
            "details": {
                "cardNumber": "4111111111111111",
                "expiryMonth": "12",
                "expiryYear": "2030",
                "cvv": "123"
            }
        }
        
        with self.parent.make_request_with_retry(
            'post',
            settings.ENDPOINTS['payments'],
            json=payment_data,
            name="Process Payment"
        ) as payment_response:
            if payment_response.status_code in (200, 201):
                payment = payment_response.json()
                logger.debug(f"Pago procesado para orden {self.parent.order_id}")
    
    @task
    def create_shipping(self):
        """Crear envío."""
        if not self.parent.order_id:
            logger.error("No se puede crear envío: falta orden")
            return
        
        # Crear envío
        shipping_data = {
            "orderId": self.parent.order_id,
            "method": "STANDARD",
            "trackingNumber": f"TRACK-{random.randint(10000, 99999)}"
        }
        
        with self.parent.make_request_with_retry(
            'post',
            settings.ENDPOINTS['shipping'],
            json=shipping_data,
            name="Create Shipping"
        ) as shipping_response:
            if shipping_response.status_code in (200, 201):
                shipping = shipping_response.json()
                logger.debug(f"Envío creado para orden {self.parent.order_id}")
                
                # Limpiar variables para próxima compra
                self.parent.cart_id = None
                self.parent.product_id = None
                self.parent.order_id = None
