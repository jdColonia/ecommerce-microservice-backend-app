"""
Pruebas de integración para el Product Service.
"""

import pytest
import uuid
from utils.api_utils import make_request, set_current_service


class TestProductServiceComplete:
    """
    Pruebas completas para el Product Service - categorías y productos.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("product-service")

    @pytest.fixture(autouse=True)
    def setup_and_cleanup(self):
        self.created_category_ids = []
        self.created_product_ids = []
        yield
        for product_id in self.created_product_ids:
            try:
                make_request("DELETE", f"api/products/{product_id}")
            except:
                pass
        for category_id in self.created_category_ids:
            try:
                make_request("DELETE", f"api/categories/{category_id}")
            except:
                pass

    # ==================== PRUEBAS PARA CATEGORÍAS ====================

    @pytest.fixture
    def create_test_category(self):
        """Fixture para crear una categoría de prueba."""
        unique_suffix = uuid.uuid4().hex[:8]
        category_data = {
            "categoryTitle": f"Test_Category_{unique_suffix}",
            "imageUrl": "https://example.com/test-category.jpg",
        }

        response = make_request("POST", "/api/categories", data=category_data)
        assert response.status_code == 200, f"Error al crear categoría: {response.text}"

        created_category = response.json()
        category_id = created_category.get("categoryId")

        yield {"id": category_id, "data": created_category}

        make_request("DELETE", f"/api/categories/{category_id}")

    def test_category_find_all(self):
        """Prueba para obtener todas las categorías."""
        response = make_request("GET", "/api/categories")

        assert response.status_code == 200
        result = response.json()
        assert "collection" in result
        assert isinstance(result["collection"], list)

    def test_category_find_by_id(self, create_test_category):
        """Prueba para obtener categoría por ID."""
        category = create_test_category
        response = make_request("GET", f'/api/categories/{category["id"]}')

        assert response.status_code == 200
        result = response.json()
        assert result["categoryId"] == category["id"]
        assert result["categoryTitle"] == category["data"]["categoryTitle"]

    def test_category_save(self):
        """Prueba para crear una nueva categoría."""
        unique_suffix = uuid.uuid4().hex[:8]
        category_data = {
            "categoryTitle": f"Save_Category_{unique_suffix}",
            "imageUrl": "https://example.com/save-category.jpg",
        }

        response = make_request("POST", "/api/categories", data=category_data)

        assert response.status_code == 200
        result = response.json()
        assert result["categoryTitle"] == category_data["categoryTitle"]
        assert "categoryId" in result

        make_request("DELETE", f'/api/categories/{result["categoryId"]}')

    def test_category_update(self, create_test_category):
        """Prueba para actualizar categoría."""
        category = create_test_category
        updated_data = category["data"].copy()
        updated_data["categoryTitle"] = f"Updated_{uuid.uuid4().hex[:6]}"

        response = make_request("PUT", "/api/categories", data=updated_data)

        assert response.status_code == 200
        result = response.json()
        assert result["categoryTitle"] == updated_data["categoryTitle"]

    def test_category_update_by_id(self, create_test_category):
        """Prueba para actualizar categoría por ID."""
        category = create_test_category
        updated_data = {
            "categoryTitle": f"UpdatedById_{uuid.uuid4().hex[:6]}",
            "imageUrl": "https://example.com/updated-category.jpg",
        }

        response = make_request(
            "PUT", f'/api/categories/{category["id"]}', data=updated_data
        )

        assert response.status_code == 200

    def test_category_delete_by_id(self):
        """Prueba para eliminar categoría."""
        unique_suffix = uuid.uuid4().hex[:8]
        category_data = {
            "categoryTitle": f"Delete_Category_{unique_suffix}",
            "imageUrl": "https://example.com/delete-category.jpg",
        }

        create_response = make_request("POST", "/api/categories", data=category_data)
        assert create_response.status_code == 200
        category_id = create_response.json()["categoryId"]

        delete_response = make_request("DELETE", f"/api/categories/{category_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() is True

    # ==================== PRUEBAS PARA PRODUCTOS ====================

    @pytest.fixture
    def create_test_product(self, create_test_category):
        """Fixture para crear un producto de prueba."""
        category = create_test_category
        unique_suffix = uuid.uuid4().hex[:8]
        product_data = {
            "productTitle": f"Test_Product_{unique_suffix}",
            "imageUrl": "https://example.com/test-product.jpg",
            "sku": f"SKU-{unique_suffix}",
            "priceUnit": 99.99,
            "quantity": 50,
            "categoryDto": {"categoryId": category["id"]},
        }

        response = make_request("POST", "/api/products", data=product_data)
        assert response.status_code == 200, f"Error al crear producto: {response.text}"

        created_product = response.json()
        product_id = created_product.get("productId")

        yield {"id": product_id, "data": created_product}

        make_request("DELETE", f"/api/products/{product_id}")

    def test_product_find_all(self):
        """Prueba para obtener todos los productos."""
        response = make_request("GET", "/api/products")

        assert response.status_code == 200
        result = response.json()
        assert "collection" in result
        assert isinstance(result["collection"], list)

    def test_product_find_by_id(self, create_test_product):
        """Prueba para obtener producto por ID."""
        product = create_test_product
        response = make_request("GET", f'/api/products/{product["id"]}')

        assert response.status_code == 200
        result = response.json()
        assert result["productId"] == product["id"]
        assert result["productTitle"] == product["data"]["productTitle"]

    def test_product_save(self, create_test_category):
        """Prueba para crear un nuevo producto."""
        category = create_test_category
        unique_suffix = uuid.uuid4().hex[:8]
        product_data = {
            "productTitle": f"Save_Product_{unique_suffix}",
            "imageUrl": "https://example.com/save-product.jpg",
            "sku": f"SAVE-SKU-{unique_suffix}",
            "priceUnit": 199.99,
            "quantity": 25,
            "categoryDto": {"categoryId": category["id"]},
        }

        response = make_request("POST", "/api/products", data=product_data)

        assert response.status_code == 200
        result = response.json()
        assert result["productTitle"] == product_data["productTitle"]
        assert result["sku"] == product_data["sku"]
        assert result["priceUnit"] == product_data["priceUnit"]
        assert "productId" in result

        make_request("DELETE", f'/api/products/{result["productId"]}')

    def test_product_update(self, create_test_product):
        """Prueba para actualizar producto."""
        product = create_test_product
        updated_data = product["data"].copy()
        updated_data["productTitle"] = f"Updated_Product_{uuid.uuid4().hex[:6]}"
        updated_data["priceUnit"] = 149.99

        response = make_request("PUT", "/api/products", data=updated_data)

        assert response.status_code == 200
        result = response.json()
        assert result["productTitle"] == updated_data["productTitle"]
        assert result["priceUnit"] == updated_data["priceUnit"]

    def test_product_update_by_id(self, create_test_product):
        """Prueba para actualizar producto por ID."""
        product = create_test_product
        updated_data = {
            "productTitle": f"UpdatedById_Product_{uuid.uuid4().hex[:6]}",
            "imageUrl": "https://example.com/updated-product.jpg",
            "sku": product["data"]["sku"],
            "priceUnit": 299.99,
            "quantity": 75,
        }

        response = make_request(
            "PUT", f'/api/products/{product["id"]}', data=updated_data
        )

        assert response.status_code == 200

    def test_product_delete_by_id(self, create_test_category):
        """Prueba para eliminar producto."""
        category = create_test_category
        unique_suffix = uuid.uuid4().hex[:8]
        product_data = {
            "productTitle": f"Delete_Product_{unique_suffix}",
            "imageUrl": "https://example.com/delete-product.jpg",
            "sku": f"DELETE-SKU-{unique_suffix}",
            "priceUnit": 79.99,
            "quantity": 10,
            "categoryDto": {"categoryId": category["id"]},
        }

        create_response = make_request("POST", "/api/products", data=product_data)
        assert create_response.status_code == 200
        product_id = create_response.json()["productId"]

        delete_response = make_request("DELETE", f"/api/products/{product_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() is True
