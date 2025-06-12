"""
Prueba E2E de la gestión de inventario.
"""

import pytest
import logging
from utils.api_client import ApiClient
from utils.assertions import assert_status_code, assert_contains_keys
from utils.data_generator import generate_product_data
from flows.product_catalog import ProductCatalogFlow
from fixtures.product_fixtures import test_category, test_product
from fixtures.user_fixtures import authenticated_api_client

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module")
def product_flow(authenticated_api_client):
    """Fixture para el flujo de gestión de catálogo."""
    return ProductCatalogFlow(authenticated_api_client)

def test_product_lifecycle(authenticated_api_client, product_flow, test_category):
    """
    Prueba E2E: ciclo de vida completo de un producto.
    
    Este test verifica que se pueda:
    1. Crear un producto
    2. Actualizar sus datos
    3. Eliminarlo
    """
    logger.info("Iniciando prueba de ciclo de vida de producto")
    
    category_id = test_category.get("id")
    
    # Ejecutar el ciclo de vida completo
    result = product_flow.complete_product_lifecycle(category_id)
    
    # Verificar resultados
    assert "created" in result, "El producto no se creó correctamente"
    assert "updated" in result, "El producto no se actualizó correctamente"
    assert "deleted" in result, "El producto no se eliminó correctamente"
    
    created_product = result.get("created")
    updated_product = result.get("updated")
    
    # Verificar que la creación fue correcta
    assert_contains_keys(created_product, ["id", "name", "price", "stock", "categoryId"])
    assert created_product.get("categoryId") == category_id, "La categoría no coincide"
    
    # Verificar que la actualización fue correcta
    assert updated_product.get("id") == created_product.get("id"), "El ID del producto cambió"
    assert updated_product.get("name") != created_product.get("name"), "El nombre no se actualizó"
    assert updated_product.get("price") > created_product.get("price"), "El precio no aumentó"
    
    # Verificar que la eliminación fue correcta
    assert result.get("deleted") is True, "El producto no se eliminó correctamente"
    
    # Verificar que el producto ya no existe
    get_response = authenticated_api_client.request("GET", f"/api/products/{created_product.get('id')}")
    assert get_response.status_code == 404, "El producto no se eliminó correctamente"
    
    logger.info("Prueba de ciclo de vida de producto finalizada con éxito")

def test_product_inventory_update(authenticated_api_client, product_flow, test_product):
    """
    Prueba E2E: actualización de inventario.
    
    Este test verifica que se pueda:
    1. Actualizar el stock de un producto
    2. Verificar que el cambio persiste
    """
    logger.info("Iniciando prueba de actualización de inventario")
    
    product_id = test_product.get("id")
    current_stock = test_product.get("stock")
    new_stock = current_stock + 20
    
    # Actualizar stock
    update_data = {
        "stock": new_stock
    }
    
    updated_product = product_flow.update_product(product_id, update_data)
    
    # Verificar actualización
    assert updated_product.get("stock") == new_stock, f"Stock no actualizado: {updated_product.get('stock')} != {new_stock}"
    
    # Verificar que el cambio persiste
    get_response = authenticated_api_client.request("GET", f"/api/products/{product_id}")
    assert_status_code(get_response, 200)
    
    retrieved_product = get_response.json()
    assert retrieved_product.get("stock") == new_stock, "El stock no se actualizó correctamente en la base de datos"
    
    logger.info("Prueba de actualización de inventario finalizada con éxito")

def test_product_category_filtering(authenticated_api_client, product_flow, test_category):
    """
    Prueba E2E: filtrado de productos por categoría.
    
    Este test verifica que se pueda:
    1. Crear varios productos en la misma categoría
    2. Filtrar productos por categoría
    """
    logger.info("Iniciando prueba de filtrado por categoría")
    
    category_id = test_category.get("id")
    
    # Crear 3 productos en la misma categoría
    products = []
    for i in range(3):
        product_data = generate_product_data()
        product_data["name"] = f"Producto Test Categoría {i+1}"
        product_data["categoryId"] = category_id
        
        product = product_flow.create_product(product_data)
        products.append(product)
    
    try:
        # Filtrar por categoría
        filtered_products = product_flow.search_products_by_category(category_id)
        
        # Verificar que se encuentren al menos los 3 productos creados
        assert len(filtered_products) >= 3, f"No se encontraron suficientes productos en la categoría {category_id}"
        
        # Verificar que los productos creados estén en los resultados
        product_ids = [p.get("id") for p in products]
        found_products = [p for p in filtered_products if p.get("id") in product_ids]
        
        assert len(found_products) == len(products), "No se encontraron todos los productos creados"
        
        # Verificar que todos pertenecen a la categoría correcta
        for product in filtered_products:
            assert product.get("categoryId") == category_id, f"Producto {product.get('id')} con categoría incorrecta"
        
        logger.info("Prueba de filtrado por categoría finalizada con éxito")
    
    finally:
        # Limpiar: eliminar productos creados
        for product in products:
            product_id = product.get("id")
            logger.info(f"Eliminando producto de prueba: {product_id}")
            product_flow.delete_product(product_id)

def test_add_product_to_favorites(authenticated_api_client, product_flow, test_product):
    """
    Prueba E2E: añadir producto a favoritos.
    
    Este test verifica que un usuario pueda:
    1. Añadir un producto a favoritos
    2. Eliminarlo de favoritos
    """
    logger.info("Iniciando prueba de gestión de favoritos")
    
    # Obtener ID del usuario actual (suponiendo que hay un endpoint para esto)
    user_response = authenticated_api_client.request("GET", "/api/users/me")
    assert_status_code(user_response, 200)
    
    user_id = user_response.json().get("id")
    product_id = test_product.get("id")
    
    # Añadir a favoritos
    favourite = product_flow.add_product_to_favorites(user_id, product_id)
    
    # Verificar que se añadió correctamente
    assert_contains_keys(favourite, ["userId", "productId", "likeDate"])
    assert favourite.get("userId") == user_id, "Usuario incorrecto"
    assert favourite.get("productId") == product_id, "Producto incorrecto"
    
    # Verificar que aparece en la lista de favoritos
    favourites_response = authenticated_api_client.request("GET", "/api/favourites")
    assert_status_code(favourites_response, 200)
    
    favourites = favourites_response.json()
    assert isinstance(favourites, list), "Se esperaba una lista de favoritos"
    
    found = False
    for fav in favourites:
        if fav.get("userId") == user_id and fav.get("productId") == product_id:
            found = True
            break
    
    assert found, "El favorito no se encontró en la lista"
    
    # Eliminar de favoritos
    like_date = favourite.get("likeDate")
    removed = product_flow.remove_product_from_favorites(user_id, product_id, like_date)
    
    # Verificar que se eliminó correctamente
    assert removed, "No se pudo eliminar el favorito"
    
    # Verificar que ya no aparece en la lista
    updated_favourites_response = authenticated_api_client.request("GET", "/api/favourites")
    updated_favourites = updated_favourites_response.json()
    
    not_found = True
    for fav in updated_favourites:
        if fav.get("userId") == user_id and fav.get("productId") == product_id:
            not_found = False
            break
    
    assert not_found, "El favorito sigue apareciendo en la lista después de eliminarlo"
    
    logger.info("Prueba de gestión de favoritos finalizada con éxito")
