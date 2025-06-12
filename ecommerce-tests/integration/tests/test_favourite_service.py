"""
Pruebas de integración para el Favourite Service.
"""

import pytest
import uuid
from utils.api_utils import make_request, set_current_service


class TestFavouriteServiceComplete:
    """
    Pruebas completas para el Favourite Service - gestión de favoritos.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("favourite-service")

    # ==================== PRUEBAS PARA FAVORITOS ====================

    @pytest.fixture
    def create_test_favourite(self):
        """Fixture para crear un favorito de prueba."""
        favourite_data = {
            "userId": 1,
            "productId": 1,
            "likeDate": "10-06-2025__14:30:00:000000",
        }

        response = make_request("POST", "/api/favourites", data=favourite_data)
        assert response.status_code == 200, f"Error al crear favorito: {response.text}"

        created_favourite = response.json()

        yield {"data": created_favourite}

        user_id = created_favourite["userId"]
        product_id = created_favourite["productId"]
        like_date = created_favourite["likeDate"]
        make_request("DELETE", f"/api/favourites/{user_id}/{product_id}/{like_date}")

    def test_favourite_find_all(self):
        """Prueba para obtener todos los favoritos."""
        response = make_request("GET", "/api/favourites")

        assert response.status_code == 200
        result = response.json()
        assert "collection" in result
        assert isinstance(result["collection"], list)

    def test_favourite_find_by_id_with_path_params(self, create_test_favourite):
        """Prueba para obtener favorito por ID usando parámetros del path."""
        favourite = create_test_favourite
        user_id = favourite["data"]["userId"]
        product_id = favourite["data"]["productId"]
        like_date = favourite["data"]["likeDate"]

        response = make_request(
            "GET", f"/api/favourites/{user_id}/{product_id}/{like_date}"
        )

        assert response.status_code == 200
        result = response.json()
        assert result["userId"] == user_id
        assert result["productId"] == product_id

    def test_favourite_save(self):
        """Prueba para crear un nuevo favorito."""
        favourite_data = {
            "userId": 2,
            "productId": 2,
            "likeDate": "10-06-2025__14:30:00:000000",
        }

        response = make_request("POST", "/api/favourites", data=favourite_data)

        assert response.status_code == 200
        result = response.json()
        assert result["userId"] == favourite_data["userId"]
        assert result["productId"] == favourite_data["productId"]

        user_id = result["userId"]
        product_id = result["productId"]
        like_date = result["likeDate"]
        make_request("DELETE", f"/api/favourites/{user_id}/{product_id}/{like_date}")

    def test_favourite_update(self, create_test_favourite):
        """Prueba para actualizar favorito."""
        favourite = create_test_favourite
        updated_data = favourite["data"].copy()
        updated_data["likeDate"] = "10-06-2025__14:30:00:000000"

        response = make_request("PUT", "/api/favourites", data=updated_data)

        assert response.status_code == 200
        result = response.json()
        assert result["likeDate"] == updated_data["likeDate"]

    def test_favourite_delete_by_id_with_path_params(self):
        """Prueba para eliminar favorito usando parámetros del path."""
        favourite_data = {
            "userId": 3,
            "productId": 3,
            "likeDate": "10-06-2025__14:30:00:000000",
        }

        create_response = make_request("POST", "/api/favourites", data=favourite_data)
        assert create_response.status_code == 200
        created_favourite = create_response.json()

        user_id = created_favourite["userId"]
        product_id = created_favourite["productId"]
        like_date = created_favourite["likeDate"]

        delete_response = make_request(
            "DELETE", f"/api/favourites/{user_id}/{product_id}/{like_date}"
        )
        assert delete_response.status_code == 200
        assert delete_response.json() is True

    def test_favourite_with_different_users_same_product(self):
        """Prueba para verificar que múltiples usuarios pueden marcar como favorito el mismo producto."""
        product_id = 5
        like_date = "10-06-2025__14:30:00:000000"

        favourite_data_1 = {
            "userId": 10,
            "productId": product_id,
            "likeDate": like_date,
        }

        response_1 = make_request("POST", "/api/favourites", data=favourite_data_1)
        assert response_1.status_code == 200

        favourite_data_2 = {
            "userId": 11,
            "productId": product_id,
            "likeDate": "10-06-2025__14:30:00:000000",
        }

        response_2 = make_request("POST", "/api/favourites", data=favourite_data_2)
        assert response_2.status_code == 200

        favourite_1 = response_1.json()
        favourite_2 = response_2.json()

        assert favourite_1["userId"] != favourite_2["userId"]
        assert favourite_1["productId"] == favourite_2["productId"]

        make_request(
            "DELETE",
            f"/api/favourites/{favourite_1['userId']}/{favourite_1['productId']}/{favourite_1['likeDate']}",
        )
        make_request(
            "DELETE",
            f"/api/favourites/{favourite_2['userId']}/{favourite_2['productId']}/{favourite_2['likeDate']}",
        )
