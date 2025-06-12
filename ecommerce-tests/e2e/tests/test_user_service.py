"""
Pruebas E2E para el User Service.
"""

import pytest
from conftest import make_request, set_current_service, generate_unique_id


class TestUserServiceE2E:
    """
    Pruebas End-to-End para el User Service.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("user-service")

    def test_e2e_complete_user_lifecycle(self, cleanup_resources):
        """
        E2E Test 1: Ciclo de vida completo de un usuario.
        Crea usuario -> Obtiene usuario -> Actualiza usuario -> Elimina usuario.
        """
        unique_id = generate_unique_id()

        # 1. Crear usuario
        user_data = {
            "firstName": f"John_{unique_id}",
            "lastName": "Doe",
            "email": f"john.doe.{unique_id}@example.com",
            "phone": "+57123456789",
            "imageUrl": "https://example.com/avatar.jpg",
        }

        create_response = make_request("POST", "/api/users", data=user_data)
        assert create_response.status_code == 200
        created_user = create_response.json()
        user_id = created_user["userId"]
        cleanup_resources["users"].append(user_id)

        # Verificar datos del usuario creado
        assert created_user["firstName"] == user_data["firstName"]
        assert created_user["email"] == user_data["email"]

        # 2. Obtener usuario por ID
        get_response = make_request("GET", f"/api/users/{user_id}")
        assert get_response.status_code == 200
        retrieved_user = get_response.json()
        assert retrieved_user["userId"] == user_id
        assert retrieved_user["firstName"] == user_data["firstName"]

        # 3. Actualizar usuario
        updated_data = created_user.copy()
        updated_data["firstName"] = f"Jane_{unique_id}"
        updated_data["phone"] = "+57987654321"

        update_response = make_request("PUT", "/api/users", data=updated_data)
        assert update_response.status_code == 200
        updated_user = update_response.json()
        assert updated_user["firstName"] == f"Jane_{unique_id}"
        assert updated_user["phone"] == "+57987654321"

        # 4. Eliminar usuario
        delete_response = make_request("DELETE", f"/api/users/{user_id}")
        assert delete_response.status_code == 200
        assert delete_response.json() is True
        cleanup_resources["users"].remove(user_id)

    def test_e2e_user_with_address_management(self, cleanup_resources):
        """
        E2E Test 2: Gestión completa de usuario con direcciones.
        Crea usuario -> Agrega dirección -> Actualiza dirección -> Lista direcciones.
        """
        unique_id = generate_unique_id()

        # 1. Crear usuario
        user_data = {
            "firstName": f"Alice_{unique_id}",
            "lastName": "Smith",
            "email": f"alice.smith.{unique_id}@example.com",
            "phone": "+57555123456",
        }

        user_response = make_request("POST", "/api/users", data=user_data)
        assert user_response.status_code == 200
        user = user_response.json()
        user_id = user["userId"]
        cleanup_resources["users"].append(user_id)

        # 2. Crear dirección para el usuario
        address_data = {
            "fullAddress": f"Calle 123 #{unique_id}",
            "postalCode": "110111",
            "city": "Bogotá",
            "userDto": {"userId": user_id},
        }

        address_response = make_request("POST", "/api/address", data=address_data)
        assert address_response.status_code == 200
        address = address_response.json()
        address_id = address["addressId"]
        cleanup_resources["addresses"].append(address_id)

        # Verificar que la dirección está asociada al usuario
        assert address["fullAddress"] == address_data["fullAddress"]
        assert address["city"] == "Bogotá"

        # 3. Actualizar dirección
        updated_address = address.copy()
        updated_address["city"] = "Medellín"
        updated_address["postalCode"] = "050001"

        update_address_response = make_request(
            "PUT", "/api/address", data=updated_address
        )
        assert update_address_response.status_code == 200
        final_address = update_address_response.json()
        assert final_address["city"] == "Medellín"
        assert final_address["postalCode"] == "050001"

        # 4. Listar todas las direcciones
        all_addresses_response = make_request("GET", "/api/address")
        assert all_addresses_response.status_code == 200
        addresses_collection = all_addresses_response.json()
        assert "collection" in addresses_collection
        assert isinstance(addresses_collection["collection"], list)

    def test_e2e_user_credentials_workflow(self, cleanup_resources):
        """
        E2E Test 3: Flujo completo de credenciales de usuario.
        Crea usuario -> Crea credencial -> Busca por username -> Actualiza credencial.
        """
        unique_id = generate_unique_id()

        # 1. Crear usuario
        user_data = {
            "firstName": f"Bob_{unique_id}",
            "lastName": "Johnson",
            "email": f"bob.johnson.{unique_id}@example.com",
            "phone": "+57777888999",
        }

        user_response = make_request("POST", "/api/users", data=user_data)
        assert user_response.status_code == 200
        user = user_response.json()
        user_id = user["userId"]
        cleanup_resources["users"].append(user_id)

        # 2. Crear credencial para el usuario
        credential_data = {
            "username": f"bob_{unique_id}",
            "password": "$2a$10$LK9Oiyv1vw3fIAHDrRGdXuIfizqoov6xGfq7QQFG1xzGyXwEy0z8u",
            "roleBasedAuthority": "ROLE_USER",
            "isEnabled": True,
            "isAccountNonExpired": True,
            "isAccountNonLocked": True,
            "isCredentialsNonExpired": True,
            "userDto": {"userId": user_id},
        }

        credential_response = make_request(
            "POST", "/api/credentials", data=credential_data
        )
        assert credential_response.status_code == 200
        credential = credential_response.json()
        credential_id = credential["credentialId"]
        cleanup_resources["credentials"].append(credential_id)

        # Verificar credencial creada
        assert credential["username"] == f"bob_{unique_id}"
        assert credential["roleBasedAuthority"] == "ROLE_USER"
        assert credential["isEnabled"] is True

        # 3. Buscar credencial por username
        username_response = make_request(
            "GET", f"/api/credentials/username/{credential['username']}"
        )
        assert username_response.status_code == 200
        found_credential = username_response.json()
        assert found_credential["credentialId"] == credential_id
        assert found_credential["username"] == f"bob_{unique_id}"

        # 4. Actualizar credencial
        updated_credential = credential.copy()
        updated_credential["roleBasedAuthority"] = "ROLE_ADMIN"
        updated_credential["isEnabled"] = True

        update_credential_response = make_request(
            "PUT", "/api/credentials", data=updated_credential
        )
        assert update_credential_response.status_code == 200
        final_credential = update_credential_response.json()
        assert final_credential["roleBasedAuthority"] == "ROLE_ADMIN"

    def test_e2e_verification_token_workflow(self, cleanup_resources):
        """
        E2E Test 4: Flujo completo de tokens de verificación.
        Crea usuario -> Crea credencial -> Crea token -> Obtiene token -> Actualiza token.
        """
        unique_id = generate_unique_id()

        # 1. Crear usuario
        user_data = {
            "firstName": f"Charlie_{unique_id}",
            "lastName": "Brown",
            "email": f"charlie.brown.{unique_id}@example.com",
            "phone": "+57111222333",
        }

        user_response = make_request("POST", "/api/users", data=user_data)
        assert user_response.status_code == 200
        user = user_response.json()
        user_id = user["userId"]
        cleanup_resources["users"].append(user_id)

        # 2. Crear credencial
        credential_data = {
            "username": f"charlie_{unique_id}",
            "password": "$2a$10$LK9Oiyv1vw3fIAHDrRGdXuIfizqoov6xGfq7QQFG1xzGyXwEy0z8u",
            "roleBasedAuthority": "ROLE_USER",
            "isEnabled": True,
            "isAccountNonExpired": True,
            "isAccountNonLocked": True,
            "isCredentialsNonExpired": True,
            "userDto": {"userId": user_id},
        }

        credential_response = make_request(
            "POST", "/api/credentials", data=credential_data
        )
        assert credential_response.status_code == 200
        credential = credential_response.json()
        credential_id = credential["credentialId"]
        cleanup_resources["credentials"].append(credential_id)

        # 3. Crear token de verificación
        token_data = {
            "token": f"verification_token_{unique_id}",
            "expireDate": "31-12-2025",
            "credentialDto": {"credentialId": credential_id},
        }

        token_response = make_request(
            "POST", "/api/verificationTokens", data=token_data
        )
        assert token_response.status_code == 200
        verification_token = token_response.json()
        token_id = verification_token["verificationTokenId"]
        cleanup_resources["verification_tokens"].append(token_id)

        # Verificar token creado
        assert verification_token["token"] == f"verification_token_{unique_id}"
        assert verification_token["expireDate"] == "31-12-2025"

        # 4. Obtener token por ID
        get_token_response = make_request("GET", f"/api/verificationTokens/{token_id}")
        assert get_token_response.status_code == 200
        retrieved_token = get_token_response.json()
        assert retrieved_token["verificationTokenId"] == token_id

        # 5. Actualizar token
        updated_token = verification_token.copy()
        updated_token["expireDate"] = "30-06-2026"

        update_token_response = make_request(
            "PUT", "/api/verificationTokens", data=updated_token
        )
        assert update_token_response.status_code == 200
        final_token = update_token_response.json()
        assert final_token["expireDate"] == "30-06-2026"

    def test_e2e_multiple_users_listing(self, cleanup_resources):
        """
        E2E Test 5: Gestión de múltiples usuarios y listado.
        Crea múltiples usuarios -> Lista todos -> Verifica existencia -> Busca específico.
        """
        unique_id = generate_unique_id()
        created_users = []

        # 1. Crear múltiples usuarios
        users_data = [
            {
                "firstName": f"User1_{unique_id}",
                "lastName": "Test",
                "email": f"user1.{unique_id}@example.com",
                "phone": "+57111111111",
            },
            {
                "firstName": f"User2_{unique_id}",
                "lastName": "Test",
                "email": f"user2.{unique_id}@example.com",
                "phone": "+57222222222",
            },
            {
                "firstName": f"User3_{unique_id}",
                "lastName": "Test",
                "email": f"user3.{unique_id}@example.com",
                "phone": "+57333333333",
            },
        ]

        for user_data in users_data:
            response = make_request("POST", "/api/users", data=user_data)
            assert response.status_code == 200
            user = response.json()
            created_users.append(user)
            cleanup_resources["users"].append(user["userId"])

        # 2. Obtener lista de todos los usuarios
        all_users_response = make_request("GET", "/api/users")
        assert all_users_response.status_code == 200
        users_collection = all_users_response.json()
        assert "collection" in users_collection
        assert isinstance(users_collection["collection"], list)

        # 3. Verificar que todos los usuarios creados están en la lista
        all_user_ids = [user["userId"] for user in users_collection["collection"]]
        for created_user in created_users:
            assert created_user["userId"] in all_user_ids

        # 4. Buscar usuarios específicos por ID
        for created_user in created_users:
            specific_user_response = make_request(
                "GET", f"/api/users/{created_user['userId']}"
            )
            assert specific_user_response.status_code == 200
            retrieved_user = specific_user_response.json()
            assert retrieved_user["userId"] == created_user["userId"]
            assert retrieved_user["firstName"] == created_user["firstName"]

        # 5. Verificar usuario conocido por username
        known_user_response = make_request("GET", "/api/users/username/selimhorri")
        assert known_user_response.status_code == 200
        known_user = known_user_response.json()
        assert "userId" in known_user
        assert "firstName" in known_user
