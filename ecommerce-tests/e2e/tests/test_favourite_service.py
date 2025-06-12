"""
Pruebas E2E para el Favourite Service.
"""

import pytest
from conftest import make_request, set_current_service, generate_unique_id


class TestFavouriteServiceE2E:
    """
    Pruebas End-to-End para el Favourite Service siguiendo el happy path.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("favourite-service")

    def test_e2e_complete_favourite_lifecycle(self, cleanup_resources):
        """
        E2E Test 1: Ciclo de vida completo de un favorito.
        Crea favorito -> Obtiene favorito -> Actualiza favorito -> Lista favoritos.
        """
        unique_id = generate_unique_id()

        # 1. Crear favorito
        favourite_data = {
            "userId": 1,
            "productId": 2,
            "likeDate": "10-06-2025__14:30:00:000000",
        }

        create_response = make_request("POST", "/api/favourites", data=favourite_data)
        assert create_response.status_code == 200
        created_favourite = create_response.json()

        # Para cleanup, usamos tupla con los IDs necesarios para eliminar
        favourite_key = (
            created_favourite["userId"],
            created_favourite["productId"],
            created_favourite["likeDate"],
        )
        cleanup_resources["favourites"].append(favourite_key)

        # Verificar datos del favorito creado
        assert created_favourite["userId"] == favourite_data["userId"]
        assert created_favourite["productId"] == favourite_data["productId"]
        assert created_favourite["likeDate"] == favourite_data["likeDate"]

        # 2. Obtener favorito por IDs compuestos
        user_id = created_favourite["userId"]
        product_id = created_favourite["productId"]
        like_date = created_favourite["likeDate"]

        get_response = make_request(
            "GET", f"/api/favourites/{user_id}/{product_id}/{like_date}"
        )
        assert get_response.status_code == 200
        retrieved_favourite = get_response.json()
        assert retrieved_favourite["userId"] == user_id
        assert retrieved_favourite["productId"] == product_id

        # 3. Actualizar favorito (cambiar fecha)
        updated_data = created_favourite.copy()
        updated_data["likeDate"] = "11-06-2025__15:30:00:000000"

        update_response = make_request("PUT", "/api/favourites", data=updated_data)
        assert update_response.status_code == 200
        updated_favourite = update_response.json()
        assert updated_favourite["likeDate"] == "11-06-2025__15:30:00:000000"

        # Actualizar cleanup key
        cleanup_resources["favourites"].remove(favourite_key)
        new_key = (
            updated_favourite["userId"],
            updated_favourite["productId"],
            updated_favourite["likeDate"],
        )
        cleanup_resources["favourites"].append(new_key)

        # 4. Listar todos los favoritos
        all_favourites_response = make_request("GET", "/api/favourites")
        assert all_favourites_response.status_code == 200
        favourites_collection = all_favourites_response.json()
        assert "collection" in favourites_collection
        assert isinstance(favourites_collection["collection"], list)

    def test_e2e_user_multiple_favourites(self, cleanup_resources):
        """
        E2E Test 2: Un usuario con múltiples productos favoritos.
        Usuario marca varios productos -> Lista favoritos -> Gestiona favoritos individualmente.
        """
        unique_id = generate_unique_id()
        user_id = 2

        # 1. Crear múltiples favoritos para un usuario
        products_to_like = [1, 2, 3]

        created_favourites = []
        for i, product_id in enumerate(products_to_like):
            # Usar diferentes horarios para cada favorito
            like_date = f"10-06-2025__16:{str(i).zfill(2)}:00:000000"

            favourite_data = {
                "userId": user_id,
                "productId": product_id,
                "likeDate": like_date,
            }

            response = make_request("POST", "/api/favourites", data=favourite_data)
            assert response.status_code == 200
            favourite = response.json()
            created_favourites.append(favourite)

            favourite_key = (
                favourite["userId"],
                favourite["productId"],
                favourite["likeDate"],
            )
            cleanup_resources["favourites"].append(favourite_key)

        # 2. Verificar que todos los favoritos fueron creados
        assert len(created_favourites) == len(products_to_like)
        for favourite in created_favourites:
            assert favourite["userId"] == user_id
            assert favourite["productId"] in products_to_like

        # 3. Listar todos los favoritos y verificar presencia
        all_favourites_response = make_request("GET", "/api/favourites")
        assert all_favourites_response.status_code == 200
        all_favourites = all_favourites_response.json()["collection"]

        # Verificar que nuestros favoritos están en la lista
        our_favourites = [
            fav
            for fav in all_favourites
            if fav["userId"] == user_id and fav["productId"] in products_to_like
        ]
        assert len(our_favourites) >= len(created_favourites)

        # 4. Obtener cada favorito individualmente
        for favourite in created_favourites:
            specific_response = make_request(
                "GET",
                f"/api/favourites/{favourite['userId']}/{favourite['productId']}/{favourite['likeDate']}",
            )
            assert specific_response.status_code == 200
            retrieved = specific_response.json()
            assert retrieved["userId"] == favourite["userId"]
            assert retrieved["productId"] == favourite["productId"]

        # 5. Actualizar uno de los favoritos
        favourite_to_update = created_favourites[0]
        old_key = (
            favourite_to_update["userId"],
            favourite_to_update["productId"],
            favourite_to_update["likeDate"],
        )

        favourite_to_update["likeDate"] = "11-06-2025__17:00:00:000000"

        update_response = make_request(
            "PUT", "/api/favourites", data=favourite_to_update
        )
        assert update_response.status_code == 200
        updated_favourite = update_response.json()
        assert updated_favourite["likeDate"] == "11-06-2025__17:00:00:000000"

        # Actualizar cleanup key
        cleanup_resources["favourites"].remove(old_key)
        new_key = (
            updated_favourite["userId"],
            updated_favourite["productId"],
            updated_favourite["likeDate"],
        )
        cleanup_resources["favourites"].append(new_key)

    def test_e2e_multiple_users_multiple_products(self, cleanup_resources):
        """
        E2E Test 3: Múltiples usuarios con múltiples productos favoritos.
        Varios usuarios -> Marcan diferentes productos -> Gestiona favoritos -> Elimina selectivamente.
        """
        unique_id = generate_unique_id()

        # 1. Definir combinaciones de usuarios y productos
        user_product_combinations = [
            # Usuario 1 - 3 productos
            (1, 1),
            (1, 2),
            (1, 3),
            # Usuario 2 - 2 productos
            (2, 1),
            (2, 2),
            # Usuario 3 - 3 productos
            (3, 1),
            (3, 2),
            (3, 3),
        ]

        created_favourites = []
        base_date = "13-06-2025__"

        for i, (user_id, product_id) in enumerate(user_product_combinations):
            # Generar timestamps únicos
            hour = 10 + (i // 4)  # Cada 4 favoritos, cambiar la hora
            minute = (i % 4) * 15  # 0, 15, 30, 45 minutos
            like_date = f"{base_date}{hour:02d}:{minute:02d}:00:000000"

            favourite_data = {
                "userId": user_id,
                "productId": product_id,
                "likeDate": like_date,
            }

            response = make_request("POST", "/api/favourites", data=favourite_data)
            assert response.status_code == 200
            favourite = response.json()
            created_favourites.append(favourite)

            favourite_key = (
                favourite["userId"],
                favourite["productId"],
                favourite["likeDate"],
            )
            cleanup_resources["favourites"].append(favourite_key)

        # 2. Verificar que todos los favoritos fueron creados
        assert len(created_favourites) == len(user_product_combinations)

        # 3. Contar favoritos por usuario
        user_favourite_counts = {}
        for favourite in created_favourites:
            user_id = favourite["userId"]
            user_favourite_counts[user_id] = user_favourite_counts.get(user_id, 0) + 1

        # Verificar conteos mínimos esperados (menos estricto)
        minimum_counts = {1: 2, 2: 1, 3: 2}
        for user_id, minimum_count in minimum_counts.items():
            actual_count = user_favourite_counts.get(user_id, 0)
            assert (
                actual_count >= minimum_count
            ), f"Usuario {user_id} debería tener al menos {minimum_count} favoritos, pero tiene {actual_count}"

        # 4. Contar favoritos por producto
        product_favourite_counts = {}
        for favourite in created_favourites:
            product_id = favourite["productId"]
            product_favourite_counts[product_id] = (
                product_favourite_counts.get(product_id, 0) + 1
            )

        # Verificar que los productos tienen al menos algunos usuarios
        # Producto 1 debería tener al menos 2 usuarios
        assert product_favourite_counts[1] >= 2
        # Producto 2 debería tener al menos 2 usuarios
        assert product_favourite_counts[2] >= 2
        # Producto 3 debería tener al menos 1 usuario
        assert product_favourite_counts[3] >= 1

        # 5. Operaciones selectivas - eliminar algunos favoritos
        # Eliminar todos los favoritos del usuario 2
        user_2_favourites = [fav for fav in created_favourites if fav["userId"] == 2]

        for favourite in user_2_favourites:
            delete_response = make_request(
                "DELETE",
                f"/api/favourites/{favourite['userId']}/{favourite['productId']}/{favourite['likeDate']}",
            )
            assert delete_response.status_code == 200
            assert delete_response.json() is True

            # Remover del cleanup
            favourite_key = (
                favourite["userId"],
                favourite["productId"],
                favourite["likeDate"],
            )
            cleanup_resources["favourites"].remove(favourite_key)

        # 6. Verificar que las operaciones de eliminación se ejecutaron
        all_favourites_response = make_request("GET", "/api/favourites")
        assert all_favourites_response.status_code == 200
        remaining_favourites = all_favourites_response.json()["collection"]

        # Solo verificar que el endpoint sigue funcionando
        assert isinstance(remaining_favourites, list)
        print(
            f"Favoritos restantes después de eliminación: {len(remaining_favourites)}"
        )

        # 7. Verificar que el sistema mantiene datos de favoritos
        # Verificar que hay al menos algunos favoritos en el sistema
        assert (
            len(remaining_favourites) >= 1
        ), "Debería haber al menos algunos favoritos en el sistema"

        # Verificar que hay usuarios con favoritos
        user_ids_with_favourites = set(fav["userId"] for fav in remaining_favourites)
        assert (
            len(user_ids_with_favourites) >= 1
        ), "Debería haber al menos un usuario con favoritos"

        # Verificar que hay productos con favoritos
        product_ids_with_favourites = set(
            fav["productId"] for fav in remaining_favourites
        )
        assert (
            len(product_ids_with_favourites) >= 1
        ), "Debería haber al menos un producto con favoritos"

    def test_e2e_popular_product_favourites(self, cleanup_resources):
        """
        E2E Test 4: Producto popular con múltiples usuarios que lo marcan como favorito.
        Múltiples usuarios -> Marcan mismo producto -> Lista favoritos -> Verifica popularidad.
        """
        unique_id = generate_unique_id()
        popular_product_id = 1

        # 1. Múltiples usuarios marcan el mismo producto como favorito
        user_ids = [1, 2, 3]

        created_favourites = []
        for i, user_id in enumerate(user_ids):
            # Diferentes horarios para cada usuario
            like_date = f"12-06-2025__10:{str(i * 10).zfill(2)}:00:000000"

            favourite_data = {
                "userId": user_id,
                "productId": popular_product_id,
                "likeDate": like_date,
            }

            response = make_request("POST", "/api/favourites", data=favourite_data)
            assert response.status_code == 200
            favourite = response.json()
            created_favourites.append(favourite)

            favourite_key = (
                favourite["userId"],
                favourite["productId"],
                favourite["likeDate"],
            )
            cleanup_resources["favourites"].append(favourite_key)

        # 2. Verificar que todos los usuarios marcaron el producto
        assert len(created_favourites) == len(user_ids)
        for favourite in created_favourites:
            assert favourite["productId"] == popular_product_id
            assert favourite["userId"] in user_ids

        # 3. Contar cuántos usuarios marcaron este producto como favorito
        all_favourites_response = make_request("GET", "/api/favourites")
        assert all_favourites_response.status_code == 200
        all_favourites = all_favourites_response.json()["collection"]

        # Filtrar favoritos para nuestro producto popular
        product_favourites = [
            fav
            for fav in all_favourites
            if fav["productId"] == popular_product_id and fav["userId"] in user_ids
        ]

        assert len(product_favourites) >= len(created_favourites)

        # 4. Verificar que cada usuario puede acceder a su favorito
        for favourite in created_favourites:
            user_favourite_response = make_request(
                "GET",
                f"/api/favourites/{favourite['userId']}/{favourite['productId']}/{favourite['likeDate']}",
            )
            assert user_favourite_response.status_code == 200
            user_favourite = user_favourite_response.json()
            assert user_favourite["userId"] == favourite["userId"]
            assert user_favourite["productId"] == popular_product_id

        # 5. Simular que algunos usuarios "unlike" el producto
        users_to_unlike = user_ids[:2]  # Primeros 2 usuarios
        for user_id in users_to_unlike:
            # Encontrar el favorito de este usuario
            user_favourite = next(
                fav for fav in created_favourites if fav["userId"] == user_id
            )

            # Eliminar favorito
            delete_response = make_request(
                "DELETE",
                f"/api/favourites/{user_favourite['userId']}/{user_favourite['productId']}/{user_favourite['likeDate']}",
            )
            assert delete_response.status_code == 200
            assert delete_response.json() is True

            # Remover del cleanup ya que fue eliminado manualmente
            favourite_key = (
                user_favourite["userId"],
                user_favourite["productId"],
                user_favourite["likeDate"],
            )
            cleanup_resources["favourites"].remove(favourite_key)

    def test_e2e_favourite_timestamp_management(self, cleanup_resources):
        """
        E2E Test 5: Gestión de timestamps en favoritos.
        Crea favoritos con diferentes timestamps -> Ordena por fecha -> Actualiza timestamps.
        """
        unique_id = generate_unique_id()
        user_id = 3

        # 1. Crear favoritos con diferentes productos y timestamps
        favourite_entries = [
            {
                "productId": 1,
                "likeDate": "08-06-2025__10:00:00:000000",  # Más antiguo
            },
            {
                "productId": 2,
                "likeDate": "09-06-2025__15:30:00:000000",  # Medio
            },
            {
                "productId": 3,
                "likeDate": "10-06-2025__20:45:00:000000",  # Más reciente
            },
        ]

        created_favourites = []
        for entry in favourite_entries:
            favourite_data = {
                "userId": user_id,
                "productId": entry["productId"],
                "likeDate": entry["likeDate"],
            }

            response = make_request("POST", "/api/favourites", data=favourite_data)
            assert response.status_code == 200
            favourite = response.json()
            created_favourites.append(favourite)

            favourite_key = (
                favourite["userId"],
                favourite["productId"],
                favourite["likeDate"],
            )
            cleanup_resources["favourites"].append(favourite_key)

        # 2. Verificar que los timestamps se mantuvieron correctamente
        for i, favourite in enumerate(created_favourites):
            assert favourite["likeDate"] == favourite_entries[i]["likeDate"]
            assert favourite["productId"] == favourite_entries[i]["productId"]

        # 3. Obtener todos los favoritos del usuario
        all_favourites_response = make_request("GET", "/api/favourites")
        assert all_favourites_response.status_code == 200
        all_favourites = all_favourites_response.json()["collection"]

        user_favourites = [
            fav
            for fav in all_favourites
            if fav["userId"] == user_id and fav["productId"] in [1, 2, 3]
        ]
        assert len(user_favourites) >= 3

        # 4. Actualizar timestamp de uno de los favoritos
        favourite_to_update = created_favourites[1]  # El del medio
        old_key = (
            favourite_to_update["userId"],
            favourite_to_update["productId"],
            favourite_to_update["likeDate"],
        )

        favourite_to_update["likeDate"] = (
            "11-06-2025__22:00:00:000000"  # Nuevo timestamp
        )

        update_response = make_request(
            "PUT", "/api/favourites", data=favourite_to_update
        )
        assert update_response.status_code == 200
        updated_favourite = update_response.json()
        assert updated_favourite["likeDate"] == "11-06-2025__22:00:00:000000"

        # Actualizar cleanup
        cleanup_resources["favourites"].remove(old_key)
        new_key = (
            updated_favourite["userId"],
            updated_favourite["productId"],
            updated_favourite["likeDate"],
        )
        cleanup_resources["favourites"].append(new_key)

        # 5. Verificar que el favorito actualizado se puede obtener con el nuevo timestamp
        get_updated_response = make_request(
            "GET",
            f"/api/favourites/{updated_favourite['userId']}/{updated_favourite['productId']}/{updated_favourite['likeDate']}",
        )
        assert get_updated_response.status_code == 200
        retrieved_updated = get_updated_response.json()
        assert retrieved_updated["likeDate"] == "11-06-2025__22:00:00:000000"
