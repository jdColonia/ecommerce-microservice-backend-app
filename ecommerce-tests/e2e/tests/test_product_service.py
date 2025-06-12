"""
Pruebas E2E para el Product Service.
"""

import pytest
from conftest import make_request, set_current_service, generate_unique_id


class TestProductServiceE2E:
    """
    Pruebas End-to-End para el Product Service.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("product-service")

    def test_e2e_complete_category_lifecycle(self, cleanup_resources):
        """
        E2E Test 1: Ciclo de vida completo de una categoría.
        Crea categoría -> Obtiene categoría -> Actualiza categoría -> Lista categorías.
        """
        unique_id = generate_unique_id()

        # 1. Crear categoría
        category_data = {
            "categoryTitle": f"Electronics_{unique_id}",
            "imageUrl": f"https://example.com/electronics_{unique_id}.jpg",
        }

        create_response = make_request("POST", "/api/categories", data=category_data)
        assert create_response.status_code == 200
        created_category = create_response.json()
        category_id = created_category["categoryId"]
        cleanup_resources["categories"].append(category_id)

        # Verificar datos de la categoría creada
        assert created_category["categoryTitle"] == category_data["categoryTitle"]
        assert created_category["imageUrl"] == category_data["imageUrl"]

        # 2. Obtener categoría por ID
        get_response = make_request("GET", f"/api/categories/{category_id}")
        assert get_response.status_code == 200
        retrieved_category = get_response.json()
        assert retrieved_category["categoryId"] == category_id
        assert retrieved_category["categoryTitle"] == category_data["categoryTitle"]

        # 3. Actualizar categoría
        updated_data = created_category.copy()
        updated_data["categoryTitle"] = f"Updated_Electronics_{unique_id}"
        updated_data["imageUrl"] = (
            f"https://example.com/updated_electronics_{unique_id}.jpg"
        )

        update_response = make_request("PUT", "/api/categories", data=updated_data)
        assert update_response.status_code == 200
        updated_category = update_response.json()
        assert updated_category["categoryTitle"] == f"Updated_Electronics_{unique_id}"

        # 4. Listar todas las categorías
        all_categories_response = make_request("GET", "/api/categories")
        assert all_categories_response.status_code == 200
        categories_collection = all_categories_response.json()
        assert "collection" in categories_collection
        assert isinstance(categories_collection["collection"], list)

        # Verificar que nuestra categoría está en la lista
        category_ids = [
            cat["categoryId"] for cat in categories_collection["collection"]
        ]
        assert category_id in category_ids

    def test_e2e_product_with_category_workflow(self, cleanup_resources):
        """
        E2E Test 2: Flujo completo de producto con categoría.
        Crea categoría -> Crea producto en categoría -> Obtiene producto -> Actualiza producto.
        """
        unique_id = generate_unique_id()

        # 1. Crear categoría primero
        category_data = {
            "categoryTitle": f"Smartphones_{unique_id}",
            "imageUrl": f"https://example.com/smartphones_{unique_id}.jpg",
        }

        category_response = make_request("POST", "/api/categories", data=category_data)
        assert category_response.status_code == 200
        category = category_response.json()
        category_id = category["categoryId"]
        cleanup_resources["categories"].append(category_id)

        # 2. Crear producto en la categoría
        product_data = {
            "productTitle": f"iPhone_{unique_id}",
            "imageUrl": f"https://example.com/iphone_{unique_id}.jpg",
            "sku": f"IPHONE-{unique_id}",
            "priceUnit": 999.99,
            "quantity": 50,
            "categoryDto": {"categoryId": category_id},
        }

        product_response = make_request("POST", "/api/products", data=product_data)
        assert product_response.status_code == 200
        product = product_response.json()
        product_id = product["productId"]
        cleanup_resources["products"].append(product_id)

        # Verificar que el producto está asociado a la categoría
        assert product["productTitle"] == product_data["productTitle"]
        assert product["sku"] == product_data["sku"]
        assert product["priceUnit"] == product_data["priceUnit"]

        # 3. Obtener producto por ID
        get_product_response = make_request("GET", f"/api/products/{product_id}")
        assert get_product_response.status_code == 200
        retrieved_product = get_product_response.json()
        assert retrieved_product["productId"] == product_id
        assert retrieved_product["productTitle"] == product_data["productTitle"]

        # 4. Actualizar producto
        updated_product = product.copy()
        updated_product["priceUnit"] = 899.99
        updated_product["quantity"] = 75
        updated_product["productTitle"] = f"iPhone_Updated_{unique_id}"

        update_product_response = make_request(
            "PUT", "/api/products", data=updated_product
        )
        assert update_product_response.status_code == 200
        final_product = update_product_response.json()
        assert final_product["priceUnit"] == 899.99
        assert final_product["quantity"] == 75
        assert final_product["productTitle"] == f"iPhone_Updated_{unique_id}"

    def test_e2e_multiple_products_in_category(self, cleanup_resources):
        """
        E2E Test 3: Múltiples productos en una categoría.
        Crea categoría -> Crea múltiples productos -> Lista productos -> Verifica asociación.
        """
        unique_id = generate_unique_id()

        # 1. Crear categoría
        category_data = {
            "categoryTitle": f"Laptops_{unique_id}",
            "imageUrl": f"https://example.com/laptops_{unique_id}.jpg",
        }

        category_response = make_request("POST", "/api/categories", data=category_data)
        assert category_response.status_code == 200
        category = category_response.json()
        category_id = category["categoryId"]
        cleanup_resources["categories"].append(category_id)

        # 2. Crear múltiples productos en la categoría
        products_data = [
            {
                "productTitle": f"MacBook_Pro_{unique_id}",
                "imageUrl": f"https://example.com/macbook_pro_{unique_id}.jpg",
                "sku": f"MBP-{unique_id}-1",
                "priceUnit": 1999.99,
                "quantity": 20,
                "categoryDto": {"categoryId": category_id},
            },
            {
                "productTitle": f"Dell_XPS_{unique_id}",
                "imageUrl": f"https://example.com/dell_xps_{unique_id}.jpg",
                "sku": f"DELL-{unique_id}-2",
                "priceUnit": 1499.99,
                "quantity": 30,
                "categoryDto": {"categoryId": category_id},
            },
            {
                "productTitle": f"ThinkPad_{unique_id}",
                "imageUrl": f"https://example.com/thinkpad_{unique_id}.jpg",
                "sku": f"TP-{unique_id}-3",
                "priceUnit": 1299.99,
                "quantity": 25,
                "categoryDto": {"categoryId": category_id},
            },
        ]

        created_products = []
        for product_data in products_data:
            response = make_request("POST", "/api/products", data=product_data)
            assert response.status_code == 200
            product = response.json()
            created_products.append(product)
            cleanup_resources["products"].append(product["productId"])

        # 3. Listar todos los productos
        all_products_response = make_request("GET", "/api/products")
        assert all_products_response.status_code == 200
        products_collection = all_products_response.json()
        assert "collection" in products_collection
        assert isinstance(products_collection["collection"], list)

        # 4. Verificar que todos los productos creados están en la lista
        all_product_ids = [
            prod["productId"] for prod in products_collection["collection"]
        ]
        for created_product in created_products:
            assert created_product["productId"] in all_product_ids

        # 5. Verificar productos individualmente
        for created_product in created_products:
            specific_product_response = make_request(
                "GET", f"/api/products/{created_product['productId']}"
            )
            assert specific_product_response.status_code == 200
            retrieved_product = specific_product_response.json()
            assert retrieved_product["productId"] == created_product["productId"]
            assert retrieved_product["productTitle"] == created_product["productTitle"]

    def test_e2e_product_inventory_management(self, cleanup_resources):
        """
        E2E Test 4: Gestión de inventario de productos.
        Crea categoría y producto -> Actualiza cantidades -> Verifica stock -> Gestiona precios.
        """
        unique_id = generate_unique_id()

        # 1. Crear categoría
        category_data = {
            "categoryTitle": f"Gaming_{unique_id}",
            "imageUrl": f"https://example.com/gaming_{unique_id}.jpg",
        }

        category_response = make_request("POST", "/api/categories", data=category_data)
        assert category_response.status_code == 200
        category = category_response.json()
        category_id = category["categoryId"]
        cleanup_resources["categories"].append(category_id)

        # 2. Crear producto con inventario inicial
        product_data = {
            "productTitle": f"Gaming_Console_{unique_id}",
            "imageUrl": f"https://example.com/console_{unique_id}.jpg",
            "sku": f"CONSOLE-{unique_id}",
            "priceUnit": 499.99,
            "quantity": 100,
            "categoryDto": {"categoryId": category_id},
        }

        product_response = make_request("POST", "/api/products", data=product_data)
        assert product_response.status_code == 200
        product = product_response.json()
        product_id = product["productId"]
        cleanup_resources["products"].append(product_id)

        # Verificar inventario inicial
        assert product["quantity"] == 100
        assert product["priceUnit"] == 499.99

        # 3. Simular venta - reducir inventario
        updated_product = product.copy()
        updated_product["quantity"] = 85  # Se vendieron 15 unidades

        update_inventory_response = make_request(
            "PUT", "/api/products", data=updated_product
        )
        assert update_inventory_response.status_code == 200
        updated_inventory = update_inventory_response.json()
        assert updated_inventory["quantity"] == 85

        # 4. Actualizar precio del producto
        price_update = updated_inventory.copy()
        price_update["priceUnit"] = 449.99  # Precio promocional

        price_update_response = make_request("PUT", "/api/products", data=price_update)
        assert price_update_response.status_code == 200
        price_updated_product = price_update_response.json()
        assert price_updated_product["priceUnit"] == 449.99
        assert price_updated_product["quantity"] == 85

        # 5. Restock - aumentar inventario
        restock_update = price_updated_product.copy()
        restock_update["quantity"] = 120  # Nuevo stock llegó

        restock_response = make_request("PUT", "/api/products", data=restock_update)
        assert restock_response.status_code == 200
        final_product = restock_response.json()
        assert final_product["quantity"] == 120
        assert final_product["priceUnit"] == 449.99

    def test_e2e_category_and_product_bulk_operations(self, cleanup_resources):
        """
        E2E Test 5: Operaciones en lote con categorías y productos.
        Crea múltiples categorías -> Crea productos en cada categoría -> Actualiza por ID -> Lista todo.
        """
        unique_id = generate_unique_id()

        # 1. Crear múltiples categorías
        categories_data = [
            {
                "categoryTitle": f"Books_{unique_id}",
                "imageUrl": f"https://example.com/books_{unique_id}.jpg",
            },
            {
                "categoryTitle": f"Clothing_{unique_id}",
                "imageUrl": f"https://example.com/clothing_{unique_id}.jpg",
            },
            {
                "categoryTitle": f"Sports_{unique_id}",
                "imageUrl": f"https://example.com/sports_{unique_id}.jpg",
            },
        ]

        created_categories = []
        for category_data in categories_data:
            response = make_request("POST", "/api/categories", data=category_data)
            assert response.status_code == 200
            category = response.json()
            created_categories.append(category)
            cleanup_resources["categories"].append(category["categoryId"])

        # 2. Crear productos en cada categoría
        products_per_category = [
            {
                "categoryIndex": 0,
                "products": [
                    {
                        "productTitle": f"Fiction_Book_{unique_id}",
                        "sku": f"BOOK-FIC-{unique_id}",
                        "priceUnit": 19.99,
                        "quantity": 50,
                    },
                    {
                        "productTitle": f"Science_Book_{unique_id}",
                        "sku": f"BOOK-SCI-{unique_id}",
                        "priceUnit": 29.99,
                        "quantity": 30,
                    },
                ],
            },
            {
                "categoryIndex": 1,
                "products": [
                    {
                        "productTitle": f"T_Shirt_{unique_id}",
                        "sku": f"CLOTH-TSHIRT-{unique_id}",
                        "priceUnit": 24.99,
                        "quantity": 100,
                    }
                ],
            },
            {
                "categoryIndex": 2,
                "products": [
                    {
                        "productTitle": f"Soccer_Ball_{unique_id}",
                        "sku": f"SPORT-BALL-{unique_id}",
                        "priceUnit": 39.99,
                        "quantity": 40,
                    }
                ],
            },
        ]

        created_products = []
        for category_products in products_per_category:
            category_id = created_categories[category_products["categoryIndex"]][
                "categoryId"
            ]

            for product_info in category_products["products"]:
                product_data = {
                    **product_info,
                    "imageUrl": f"https://example.com/{product_info['sku'].lower()}.jpg",
                    "categoryDto": {"categoryId": category_id},
                }

                response = make_request("POST", "/api/products", data=product_data)
                assert response.status_code == 200
                product = response.json()
                created_products.append(product)
                cleanup_resources["products"].append(product["productId"])

        # 3. Actualizar algunos productos usando updateById
        for i, product in enumerate(created_products[:2]):  # Actualizar los primeros 2
            update_data = {
                "productTitle": f"Updated_{product['productTitle']}",
                "imageUrl": product.get("imageUrl", ""),
                "sku": product["sku"],
                "priceUnit": product["priceUnit"] + 5.00,  # Aumentar precio
                "quantity": product["quantity"] + 10,  # Aumentar stock
            }

            update_response = make_request(
                "PUT", f"/api/products/{product['productId']}", data=update_data
            )
            assert update_response.status_code == 200

        # 4. Verificar todas las categorías
        all_categories_response = make_request("GET", "/api/categories")
        assert all_categories_response.status_code == 200
        categories_collection = all_categories_response.json()

        category_ids_in_response = [
            cat["categoryId"] for cat in categories_collection["collection"]
        ]
        for created_category in created_categories:
            assert created_category["categoryId"] in category_ids_in_response

        # 5. Verificar todos los productos
        all_products_response = make_request("GET", "/api/products")
        assert all_products_response.status_code == 200
        products_collection = all_products_response.json()

        product_ids_in_response = [
            prod["productId"] for prod in products_collection["collection"]
        ]
        for created_product in created_products:
            assert created_product["productId"] in product_ids_in_response
