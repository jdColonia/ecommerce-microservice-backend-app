"""
Flujo de gestión del catálogo de productos.
"""

import logging
from typing import Dict, Any, List, Optional
from utils.api_client import ApiClient
from utils.data_generator import generate_product_data

logger = logging.getLogger(__name__)

class ProductCatalogFlow:
    """Implementa el flujo de gestión del catálogo de productos."""
    
    def __init__(self, api_client: ApiClient):
        self.api = api_client
    
    def create_category(self, category_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una nueva categoría.
        
        Args:
            category_data (dict): Datos de la categoría
            
        Returns:
            dict: Datos de la categoría creada
        """
        logger.info(f"Creando categoría: {category_data.get('name')}")
        
        response = self.api.request(
            method="POST",
            endpoint="/api/categories",
            data=category_data
        )
        response.raise_for_status()
        category = response.json()
        
        logger.info(f"Categoría creada con ID {category.get('id')}")
        return category
    
    def create_product(self, product_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Crea un nuevo producto.
        
        Args:
            product_data (dict, optional): Datos del producto. Si es None, se generan automáticamente.
            
        Returns:
            dict: Datos del producto creado
        """
        if product_data is None:
            product_data = generate_product_data()
        
        logger.info(f"Creando producto: {product_data.get('name')}")
        
        response = self.api.request(
            method="POST",
            endpoint="/api/products",
            data=product_data
        )
        response.raise_for_status()
        product = response.json()
        
        logger.info(f"Producto creado con ID {product.get('id')}")
        return product
    
    def update_product(self, product_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza un producto existente.
        
        Args:
            product_id (int): ID del producto
            update_data (dict): Datos a actualizar
            
        Returns:
            dict: Datos actualizados del producto
        """
        logger.info(f"Actualizando producto {product_id}")
        
        # Asegurarse de que el ID esté en los datos
        update_data["id"] = product_id
        
        response = self.api.request(
            method="PUT",
            endpoint=f"/api/products/{product_id}",
            data=update_data
        )
        response.raise_for_status()
        updated_product = response.json()
        
        logger.info(f"Producto {product_id} actualizado")
        return updated_product
    
    def add_product_to_favorites(self, user_id: int, product_id: int) -> Dict[str, Any]:
        """
        Añade un producto a favoritos.
        
        Args:
            user_id (int): ID del usuario
            product_id (int): ID del producto
            
        Returns:
            dict: Datos del favorito creado
        """
        logger.info(f"Añadiendo producto {product_id} a favoritos del usuario {user_id}")
        
        favourite_data = {
            "userId": user_id,
            "productId": product_id,
            "likeDate": "2025-05-30T12:00:00Z"  # Fecha actual
        }
        
        response = self.api.request(
            method="POST",
            endpoint="/api/favourites",
            data=favourite_data
        )
        response.raise_for_status()
        favourite = response.json()
        
        logger.info(f"Producto {product_id} añadido a favoritos del usuario {user_id}")
        return favourite
    
    def remove_product_from_favorites(self, user_id: int, product_id: int, like_date: str) -> bool:
        """
        Elimina un producto de favoritos.
        
        Args:
            user_id (int): ID del usuario
            product_id (int): ID del producto
            like_date (str): Fecha del like
            
        Returns:
            bool: True si se eliminó correctamente
        """
        logger.info(f"Eliminando producto {product_id} de favoritos del usuario {user_id}")
        
        response = self.api.request(
            method="DELETE",
            endpoint=f"/api/favourites/{user_id}/{product_id}/{like_date}"
        )
        
        success = response.status_code in (200, 204)
        if success:
            logger.info(f"Producto {product_id} eliminado de favoritos del usuario {user_id}")
        else:
            logger.error(f"Error al eliminar favorito: {response.text}")
        
        return success
    
    def delete_product(self, product_id: int) -> bool:
        """
        Elimina un producto.
        
        Args:
            product_id (int): ID del producto
            
        Returns:
            bool: True si se eliminó correctamente
        """
        logger.info(f"Eliminando producto {product_id}")
        
        response = self.api.request(
            method="DELETE",
            endpoint=f"/api/products/{product_id}"
        )
        
        success = response.status_code in (200, 204)
        if success:
            logger.info(f"Producto {product_id} eliminado correctamente")
        else:
            logger.error(f"Error al eliminar producto {product_id}: {response.text}")
        
        return success
    
    def search_products_by_category(self, category_id: int) -> List[Dict[str, Any]]:
        """
        Busca productos por categoría.
        
        Args:
            category_id (int): ID de la categoría
            
        Returns:
            list: Lista de productos
        """
        logger.info(f"Buscando productos de la categoría {category_id}")
        
        # Suponiendo que hay un endpoint para filtrar por categoría
        response = self.api.request(
            method="GET",
            endpoint="/api/products",
            params={"categoryId": category_id}
        )
        response.raise_for_status()
        products = response.json()
        
        logger.info(f"Se encontraron {len(products)} productos en la categoría {category_id}")
        return products
    
    def complete_product_lifecycle(self, category_id: int = None) -> Dict[str, Any]:
        """
        Realiza el ciclo de vida completo de un producto: creación, actualización, eliminación.
        
        Args:
            category_id (int, optional): ID de la categoría
            
        Returns:
            dict: Resultados del ciclo de vida
        """
        logger.info("Iniciando ciclo de vida completo de producto")
        
        # 1. Crear categoría si es necesario
        if category_id is None:
            category = self.create_category({
                "name": f"Categoría Test {generate_product_data()['name']}",
                "description": "Categoría para pruebas E2E"
            })
            category_id = category.get("id")
        
        # 2. Crear producto
        product_data = generate_product_data()
        product_data["categoryId"] = category_id
        product = self.create_product(product_data)
        product_id = product.get("id")
        
        # 3. Actualizar producto
        updated_product = self.update_product(product_id, {
            "name": f"{product.get('name')} (Actualizado)",
            "price": product.get("price") + 10.0,
            "stock": product.get("stock") + 5,
            "categoryId": category_id
        })
        
        # 4. Eliminar producto
        deleted = self.delete_product(product_id)
        
        logger.info(f"Ciclo de vida de producto {product_id} completado")
        return {
            "created": product,
            "updated": updated_product,
            "deleted": deleted,
            "categoryId": category_id
        }
