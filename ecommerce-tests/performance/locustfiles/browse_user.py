"""
Usuarios que solo navegan por productos y categorías.
"""

import random
import logging
from locust import task, tag
from faker import Faker
from locustfiles.base_user import BaseUser
from config import settings

logger = logging.getLogger(__name__)
fake = Faker()

class BrowseUser(BaseUser):
    """
    Usuario que solo navega por productos y categorías.
    No requiere autenticación.
    """
    
    auth_required = False
    weight = settings.BROWSE_USER_WEIGHT
    
    @tag('browse', 'products')
    @task(5)
    def view_all_products(self):
        """Ver todos los productos."""
        with self.make_request_with_retry(
            'get',
            settings.ENDPOINTS['products'],
            name="View All Products"
        ) as response:
            if response.status_code == 200:
                products = response.json()
                logger.debug(f"Obtenidos {len(products)} productos")
    
    @tag('browse', 'products')
    @task(10)
    def view_product_details(self):
        """Ver detalles de un producto aleatorio."""
        # Primero obtenemos todos los productos
        with self.make_request_with_retry(
            'get',
            settings.ENDPOINTS['products'],
            name="Get Products For Detail View"
        ) as response:
            if response.status_code == 200:
                products = response.json()
                if products:
                    # Seleccionamos un producto aleatorio
                    product = random.choice(products)
                    product_id = product.get('id')
                    
                    # Obtenemos los detalles del producto
                    with self.make_request_with_retry(
                        'get',
                        f"{settings.ENDPOINTS['products']}/{product_id}",
                        name="View Product Details"
                    ) as detail_response:
                        if detail_response.status_code == 200:
                            logger.debug(f"Visto producto {product_id}")
    
    @tag('browse', 'categories')
    @task(3)
    def view_all_categories(self):
        """Ver todas las categorías."""
        with self.make_request_with_retry(
            'get',
            settings.ENDPOINTS['categories'],
            name="View All Categories"
        ) as response:
            if response.status_code == 200:
                categories = response.json()
                logger.debug(f"Obtenidas {len(categories)} categorías")
    
    @tag('browse', 'categories', 'products')
    @task(7)
    def view_products_by_category(self):
        """Ver productos por categoría."""
        # Primero obtenemos todas las categorías
        with self.make_request_with_retry(
            'get',
            settings.ENDPOINTS['categories'],
            name="Get Categories"
        ) as response:
            if response.status_code == 200:
                categories = response.json()
                if categories:
                    # Seleccionamos una categoría aleatoria
                    category = random.choice(categories)
                    category_id = category.get('id')
                    
                    # Obtenemos los productos de la categoría
                    with self.make_request_with_retry(
                        'get',
                        f"{settings.ENDPOINTS['products']}?categoryId={category_id}",
                        name="View Products By Category"
                    ) as products_response:
                        if products_response.status_code == 200:
                            products = products_response.json()
                            logger.debug(f"Obtenidos {len(products)} productos de categoría {category_id}")
    
    @tag('search')
    @task(5)
    def search_products(self):
        """Buscar productos por término."""
        search_terms = ["laptop", "phone", "headphones", "camera", "tablet", "watch"]
        term = random.choice(search_terms)
        
        with self.make_request_with_retry(
            'get',
            f"{settings.ENDPOINTS['products']}?search={term}",
            name="Search Products"
        ) as response:
            if response.status_code == 200:
                products = response.json()
                logger.debug(f"Búsqueda '{term}' devolvió {len(products)} productos")
