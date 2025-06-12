"""
Usuarios administradores que gestionan el catálogo y usuarios.
"""

import random
import logging
import json
from locust import task, tag
from faker import Faker
from locustfiles.base_user import BaseUser
from config import settings

logger = logging.getLogger(__name__)
fake = Faker()

class AdminUser(BaseUser):
    """
    Usuario administrador que gestiona catálogo y usuarios.
    Requiere autenticación.
    """
    
    auth_required = True
    weight = settings.ADMIN_USER_WEIGHT
    username = settings.ADMIN_USERNAME
    password = settings.ADMIN_PASSWORD
    
    @tag('admin', 'users')
    @task(5)
    def view_all_users(self):
        """Ver todos los usuarios."""
        with self.make_request_with_retry(
            'get',
            settings.ENDPOINTS['users'],
            name="Admin - View All Users"
        ) as response:
            if response.status_code == 200:
                users = response.json()
                logger.debug(f"Obtenidos {len(users)} usuarios")
    
    @tag('admin', 'users')
    @task(3)
    def view_user_details(self):
        """Ver detalles de un usuario aleatorio."""
        # Primero obtenemos todos los usuarios
        with self.make_request_with_retry(
            'get',
            settings.ENDPOINTS['users'],
            name="Admin - Get Users For Detail"
        ) as response:
            if response.status_code == 200:
                users = response.json()
                if users:
                    # Seleccionamos un usuario aleatorio
                    user = random.choice(users)
                    user_id = user.get('id')
                    
                    # Obtenemos los detalles del usuario
                    with self.make_request_with_retry(
                        'get',
                        f"{settings.ENDPOINTS['users']}/{user_id}",
                        name="Admin - View User Details"
                    ) as detail_response:
                        if detail_response.status_code == 200:
                            logger.debug(f"Visto usuario {user_id}")
    
    @tag('admin', 'products')
    @task(10)
    def manage_products(self):
        """Gestionar productos (crear, actualizar, eliminar)."""
        # 1. Crear un producto
        product_data = {
            "name": fake.word() + " " + fake.word().capitalize(),
            "description": fake.paragraph(),
            "price": round(random.uniform(10.0, 1000.0), 2),
            "stock": random.randint(1, 100),
            "categoryId": random.randint(1, 5)
        }
        
        with self.make_request_with_retry(
            'post',
            settings.ENDPOINTS['products'],
            json=product_data,
            name="Admin - Create Product"
        ) as response:
            if response.status_code in (200, 201):
                product = response.json()
                product_id = product.get('id')
                logger.debug(f"Producto {product_id} creado")
                
                # 2. Actualizar el producto
                update_data = {
                    "id": product_id,
                    "name": product.get('name') + " (Updated)",
                    "price": product.get('price') + 10.0,
                    "stock": product.get('stock') + 5
                }
                
                with self.make_request_with_retry(
                    'put',
                    f"{settings.ENDPOINTS['products']}/{product_id}",
                    json=update_data,
                    name="Admin - Update Product"
                ) as update_response:
                    if update_response.status_code == 200:
                        logger.debug(f"Producto {product_id} actualizado")
                
                # 3. Eliminar el producto
                with self.make_request_with_retry(
                    'delete',
                    f"{settings.ENDPOINTS['products']}/{product_id}",
                    name="Admin - Delete Product"
                ) as delete_response:
                    if delete_response.status_code in (200, 204):
                        logger.debug(f"Producto {product_id} eliminado")
    
    @tag('admin', 'categories')
    @task(3)
    def manage_categories(self):
        """Gestionar categorías (crear, actualizar)."""
        # 1. Crear una categoría
        category_data = {
            "name": fake.word().capitalize() + " Category",
            "description": fake.sentence()
        }
        
        with self.make_request_with_retry(
            'post',
            settings.ENDPOINTS['categories'],
            json=category_data,
            name="Admin - Create Category"
        ) as response:
            if response.status_code in (200, 201):
                category = response.json()
                category_id = category.get('id')
                logger.debug(f"Categoría {category_id} creada")
                
                # 2. Actualizar la categoría
                update_data = {
                    "id": category_id,
                    "name": category.get('name') + " (Updated)",
                    "description": category.get('description') + " Updated description."
                }
                
                with self.make_request_with_retry(
                    'put',
                    f"{settings.ENDPOINTS['categories']}/{category_id}",
                    json=update_data,
                    name="Admin - Update Category"
                ) as update_response:
                    if update_response.status_code == 200:
                        logger.debug(f"Categoría {category_id} actualizada")
    
    @tag('admin', 'orders')
    @task(5)
    def view_and_update_orders(self):
        """Ver y actualizar órdenes."""
        # Obtener todas las órdenes
        with self.make_request_with_retry(
            'get',
            settings.ENDPOINTS['orders'],
            name="Admin - View All Orders"
        ) as response:
            if response.status_code == 200:
                orders = response.json()
                if orders:
                    # Seleccionar una orden aleatoria
                    order = random.choice(orders)
                    order_id = order.get('id')
                    
                    # Actualizar estado de la orden
                    statuses = ["PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"]
                    update_data = {
                        "id": order_id,
                        "status": random.choice(statuses)
                    }
                    
                    with self.make_request_with_retry(
                        'put',
                        f"{settings.ENDPOINTS['orders']}/{order_id}",
                        json=update_data,
                        name="Admin - Update Order Status"
                    ) as update_response:
                        if update_response.status_code == 200:
                            logger.debug(f"Orden {order_id} actualizada a {update_data['status']}")
