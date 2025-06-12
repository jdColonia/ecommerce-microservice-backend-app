"""
Pruebas de integración para el servicio de usuarios.
"""

import pytest
import uuid
from utils.api_utils import make_request, set_current_service


class TestUserServiceComplete:
    """
    Pruebas para todos los métodos del user-service.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("user-service")

    # ==================== PRUEBAS PARA USUARIOS ====================

    @pytest.fixture
    def create_test_user(self):
        """Fixture para crear un usuario de prueba."""
        unique_suffix = uuid.uuid4().hex[:8]
        user_data = {
            "firstName": f"Test_{unique_suffix}",
            "lastName": "Test",
            "email": f"test_{unique_suffix}@example.com",
            "phone": "+57123456789",
            "imageUrl": "https://example.com/avatar.jpg",
        }

        response = make_request("POST", "/api/users", data=user_data)
        assert response.status_code == 200, f"Error al crear usuario: {response.text}"

        created_user = response.json()
        user_id = created_user.get("userId")

        yield {"id": user_id, "data": created_user}

        make_request("DELETE", f"/api/users/{user_id}")

    def test_user_find_all(self):
        """Prueba para obtener todos los usuarios."""
        response = make_request("GET", "/api/users")

        assert response.status_code == 200
        result = response.json()
        assert "collection" in result
        assert isinstance(result["collection"], list)

    def test_user_find_by_id(self, create_test_user):
        """Prueba para obtener usuario por ID."""
        user = create_test_user
        response = make_request("GET", f'/api/users/{user["id"]}')

        assert response.status_code == 200
        result = response.json()
        assert result["userId"] == user["id"]
        assert result["firstName"] == user["data"]["firstName"]

    def test_user_find_by_username(self):
        """Prueba para obtener usuario por username."""
        response = make_request("GET", "/api/users/username/selimhorri")

        assert response.status_code == 200
        result = response.json()
        assert "userId" in result
        assert "firstName" in result

    def test_user_save(self):
        """Prueba para crear un nuevo usuario."""
        unique_suffix = uuid.uuid4().hex[:8]
        user_data = {
            "firstName": f"Save_{unique_suffix}",
            "lastName": "Test",
            "email": f"save_{unique_suffix}@example.com",
            "phone": "+57987654321",
        }

        response = make_request("POST", "/api/users", data=user_data)

        assert response.status_code == 200
        result = response.json()
        assert result["firstName"] == user_data["firstName"]
        assert "userId" in result

        make_request("DELETE", f'/api/users/{result["userId"]}')

    def test_user_update(self, create_test_user):
        """Prueba para actualizar usuario."""
        user = create_test_user
        updated_data = user["data"].copy()
        updated_data["firstName"] = f"Updated_{uuid.uuid4().hex[:6]}"

        response = make_request("PUT", "/api/users", data=updated_data)

        assert response.status_code == 200
        result = response.json()
        assert result["firstName"] == updated_data["firstName"]

    def test_user_update_by_id(self, create_test_user):
        """Prueba para actualizar usuario por ID."""
        user = create_test_user
        updated_data = {
            "firstName": f"UpdatedById_{uuid.uuid4().hex[:6]}",
            "lastName": user["data"]["lastName"],
            "email": user["data"]["email"],
            "phone": user["data"]["phone"],
        }

        response = make_request("PUT", f'/api/users/{user["id"]}', data=updated_data)

        assert response.status_code == 200

    def test_user_delete_by_id(self):
        """Prueba para eliminar usuario."""
        unique_suffix = uuid.uuid4().hex[:8]
        user_data = {
            "firstName": f"Delete_{unique_suffix}",
            "lastName": "Test",
            "email": f"delete_{unique_suffix}@example.com",
            "phone": "+57555555555",
        }

        create_response = make_request("POST", "/api/users", data=user_data)
        assert create_response.status_code == 200
        user_id = create_response.json()["userId"]

        delete_response = make_request("DELETE", f"/api/users/{user_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() is True

    # ==================== PRUEBAS PARA DIRECCIONES ====================

    @pytest.fixture
    def create_test_address(self, create_test_user):
        """Fixture para crear una dirección de prueba."""
        user = create_test_user
        address_data = {
            "fullAddress": f"Test Address {uuid.uuid4().hex[:6]}",
            "postalCode": "54321",
            "city": "Test City",
            "userDto": {"userId": user["id"]},
        }

        response = make_request("POST", "/api/address", data=address_data)
        assert response.status_code == 200, f"Error al crear dirección: {response.text}"

        created_address = response.json()
        address_id = created_address.get("addressId")

        yield {"id": address_id, "data": created_address}

        make_request("DELETE", f"/api/address/{address_id}")

    def test_address_find_all(self):
        """Prueba para obtener todas las direcciones."""
        response = make_request("GET", "/api/address")

        assert response.status_code == 200
        result = response.json()
        assert "collection" in result
        assert isinstance(result["collection"], list)

    def test_address_find_by_id(self, create_test_address):
        """Prueba para obtener dirección por ID."""
        address = create_test_address
        response = make_request("GET", f'/api/address/{address["id"]}')

        assert response.status_code == 200
        result = response.json()
        assert result["addressId"] == address["id"]

    def test_address_save(self, create_test_user):
        """Prueba para crear una nueva dirección."""
        user = create_test_user
        address_data = {
            "fullAddress": f"Save Address {uuid.uuid4().hex[:6]}",
            "postalCode": "98765",
            "city": "Save City",
            "userDto": {"userId": user["id"]},
        }

        response = make_request("POST", "/api/address", data=address_data)

        assert response.status_code == 200
        result = response.json()
        assert result["fullAddress"] == address_data["fullAddress"]
        assert "addressId" in result

        make_request("DELETE", f'/api/address/{result["addressId"]}')

    def test_address_update(self, create_test_address):
        """Prueba para actualizar dirección."""
        address = create_test_address
        updated_data = address["data"].copy()
        updated_data["city"] = f"Updated_City_{uuid.uuid4().hex[:6]}"

        response = make_request("PUT", "/api/address", data=updated_data)

        assert response.status_code == 200
        result = response.json()
        assert result["city"] == updated_data["city"]

    def test_address_update_by_id(self, create_test_address):
        """Prueba para actualizar dirección por ID."""
        address = create_test_address
        updated_data = {
            "fullAddress": address["data"]["fullAddress"],
            "postalCode": "11111",
            "city": f"UpdatedById_City_{uuid.uuid4().hex[:6]}",
        }

        response = make_request(
            "PUT", f'/api/address/{address["id"]}', data=updated_data
        )

        assert response.status_code == 200

    def test_address_delete_by_id(self, create_test_user):
        """Prueba para eliminar dirección."""
        user = create_test_user
        address_data = {
            "fullAddress": f"Delete Address {uuid.uuid4().hex[:6]}",
            "postalCode": "99999",
            "city": "Delete City",
            "userDto": {"userId": user["id"]},
        }

        create_response = make_request("POST", "/api/address", data=address_data)
        assert create_response.status_code == 200
        address_id = create_response.json()["addressId"]

        delete_response = make_request("DELETE", f"/api/address/{address_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() is True

    # ==================== PRUEBAS PARA CREDENCIALES ====================

    @pytest.fixture
    def create_test_credential(self, create_test_user):
        """Fixture para crear una credencial de prueba."""
        user = create_test_user
        unique_suffix = uuid.uuid4().hex[:8]
        credential_data = {
            "username": f"test_cred_{unique_suffix}",
            "password": "$2a$10$LK9Oiyv1vw3fIAHDrRGdXuIfizqoov6xGfq7QQFG1xzGyXwEy0z8u",
            "roleBasedAuthority": "ROLE_USER",
            "isEnabled": True,
            "isAccountNonExpired": True,
            "isAccountNonLocked": True,
            "isCredentialsNonExpired": True,
            "userDto": {"userId": user["id"]},
        }

        response = make_request("POST", "/api/credentials", data=credential_data)
        assert (
            response.status_code == 200
        ), f"Error al crear credencial: {response.text}"

        created_credential = response.json()
        credential_id = created_credential.get("credentialId")

        yield {"id": credential_id, "data": created_credential}

        make_request("DELETE", f"/api/credentials/{credential_id}")

    def test_credential_find_all(self):
        """Prueba para obtener todas las credenciales."""
        response = make_request("GET", "/api/credentials")

        assert response.status_code == 200
        result = response.json()
        assert "collection" in result
        assert isinstance(result["collection"], list)

    def test_credential_find_by_id(self, create_test_credential):
        """Prueba para obtener credencial por ID."""
        credential = create_test_credential
        response = make_request("GET", f'/api/credentials/{credential["id"]}')

        assert response.status_code == 200
        result = response.json()
        assert result["credentialId"] == credential["id"]

    def test_credential_find_by_username(self):
        """Prueba para obtener credencial por username."""
        response = make_request("GET", "/api/credentials/username/selimhorri")

        assert response.status_code == 200
        result = response.json()
        assert "credentialId" in result
        assert result["username"] == "selimhorri"

    def test_credential_save(self, create_test_user):
        """Prueba para crear una nueva credencial."""
        user = create_test_user
        unique_suffix = uuid.uuid4().hex[:8]
        credential_data = {
            "username": f"save_cred_{unique_suffix}",
            "password": "$2a$10$LK9Oiyv1vw3fIAHDrRGdXuIfizqoov6xGfq7QQFG1xzGyXwEy0z8u",
            "roleBasedAuthority": "ROLE_USER",
            "isEnabled": True,
            "isAccountNonExpired": True,
            "isAccountNonLocked": True,
            "isCredentialsNonExpired": True,
            "userDto": {"userId": user["id"]},
        }

        response = make_request("POST", "/api/credentials", data=credential_data)

        assert response.status_code == 200
        result = response.json()
        assert result["username"] == credential_data["username"]
        assert "credentialId" in result

        make_request("DELETE", f'/api/credentials/{result["credentialId"]}')

    def test_credential_update(self, create_test_credential):
        """Prueba para actualizar credencial."""
        credential = create_test_credential
        updated_data = credential["data"].copy()
        updated_data["isEnabled"] = False

        response = make_request("PUT", "/api/credentials", data=updated_data)

        assert response.status_code == 200
        result = response.json()
        assert result["isEnabled"] == False

    def test_credential_update_by_id(self, create_test_credential):
        """Prueba para actualizar credencial por ID."""
        credential = create_test_credential
        updated_data = {
            "username": credential["data"]["username"],
            "password": credential["data"]["password"],
            "roleBasedAuthority": "ROLE_ADMIN",
            "isEnabled": True,
            "isAccountNonExpired": True,
            "isAccountNonLocked": True,
            "isCredentialsNonExpired": True,
        }

        response = make_request(
            "PUT", f'/api/credentials/{credential["id"]}', data=updated_data
        )

        assert response.status_code == 200

    def test_credential_delete_by_id(self, create_test_user):
        """Prueba para eliminar credencial."""
        user = create_test_user
        unique_suffix = uuid.uuid4().hex[:8]
        credential_data = {
            "username": f"delete_cred_{unique_suffix}",
            "password": "$2a$10$LK9Oiyv1vw3fIAHDrRGdXuIfizqoov6xGfq7QQFG1xzGyXwEy0z8u",
            "roleBasedAuthority": "ROLE_USER",
            "isEnabled": True,
            "isAccountNonExpired": True,
            "isAccountNonLocked": True,
            "isCredentialsNonExpired": True,
            "userDto": {"userId": user["id"]},
        }

        create_response = make_request("POST", "/api/credentials", data=credential_data)
        assert create_response.status_code == 200
        credential_id = create_response.json()["credentialId"]

        delete_response = make_request("DELETE", f"/api/credentials/{credential_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() is True

    # ==================== PRUEBAS PARA TOKENS DE VERIFICACIÓN ====================

    @pytest.fixture
    def create_test_verification_token(self, create_test_credential):
        """Fixture para crear un token de verificación de prueba."""
        credential = create_test_credential
        token_data = {
            "token": f"test_token_{uuid.uuid4().hex[:8]}",
            "expireDate": "31-12-2024",
            "credentialDto": {"credentialId": credential["id"]},
        }

        response = make_request("POST", "/api/verificationTokens", data=token_data)
        assert response.status_code == 200, f"Error al crear token: {response.text}"

        created_token = response.json()
        token_id = created_token.get("verificationTokenId")

        yield {"id": token_id, "data": created_token}

        make_request("DELETE", f"/api/verificationTokens/{token_id}")

    def test_verification_token_find_all(self):
        """Prueba para obtener todos los tokens de verificación."""
        response = make_request("GET", "/api/verificationTokens")

        assert response.status_code == 200
        result = response.json()
        assert "collection" in result
        assert isinstance(result["collection"], list)

    def test_verification_token_find_by_id(self, create_test_verification_token):
        """Prueba para obtener token por ID."""
        token = create_test_verification_token
        response = make_request("GET", f'/api/verificationTokens/{token["id"]}')

        assert response.status_code == 200
        result = response.json()
        assert result["verificationTokenId"] == token["id"]

    def test_verification_token_save(self, create_test_credential):
        """Prueba para crear un nuevo token de verificación."""
        credential = create_test_credential
        token_data = {
            "token": f"save_token_{uuid.uuid4().hex[:8]}",
            "expireDate": "31-01-2025",
            "credentialDto": {"credentialId": credential["id"]},
        }

        response = make_request("POST", "/api/verificationTokens", data=token_data)

        assert response.status_code == 200
        result = response.json()
        assert result["token"] == token_data["token"]
        assert "verificationTokenId" in result

        make_request(
            "DELETE", f'/api/verificationTokens/{result["verificationTokenId"]}'
        )

    def test_verification_token_update(self, create_test_verification_token):
        """Prueba para actualizar token de verificación."""
        token = create_test_verification_token
        updated_data = token["data"].copy()
        updated_data["expireDate"] = "28-02-2025"

        response = make_request("PUT", "/api/verificationTokens", data=updated_data)

        assert response.status_code == 200
        result = response.json()
        assert result["expireDate"] == "28-02-2025"

    def test_verification_token_update_by_id(self, create_test_verification_token):
        """Prueba para actualizar token por ID."""
        token = create_test_verification_token
        updated_data = {
            "token": f"updated_token_{uuid.uuid4().hex[:6]}",
            "expireDate": "30-06-2025",
        }

        response = make_request(
            "PUT", f'/api/verificationTokens/{token["id"]}', data=updated_data
        )

        assert response.status_code == 200

    def test_verification_token_delete_by_id(self, create_test_credential):
        """Prueba para eliminar token de verificación."""
        credential = create_test_credential
        token_data = {
            "token": f"delete_token_{uuid.uuid4().hex[:8]}",
            "expireDate": "31-03-2025",
            "credentialDto": {"credentialId": credential["id"]},
        }

        create_response = make_request(
            "POST", "/api/verificationTokens", data=token_data
        )
        assert create_response.status_code == 200
        token_id = create_response.json()["verificationTokenId"]

        delete_response = make_request("DELETE", f"/api/verificationTokens/{token_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() is True
