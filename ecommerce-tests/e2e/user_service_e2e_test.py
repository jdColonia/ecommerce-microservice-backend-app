import pytest
import requests
import time
from typing import Dict, Any

class TestE2EBackendFlows:
    """
    Pruebas E2E a nivel backend que simulan flujos completos de usuario.
    Estas pruebas verifican la integración entre múltiples servicios.
    """
    
    # URLs de servicios (ajustar según tu configuración)
    API_GATEWAY = "http://localhost:8080"
    USER_SERVICE = "http://localhost:8700/user-service/api"
    
    HEADERS = {"Content-Type": "application/json"}
    
    @pytest.fixture(autouse=True)
    def setup_test_data(self):
        """Setup para cada test."""
        self.timestamp = str(int(time.time() * 1000))
        self.cleanup_ids = []
        
        yield
        
        # Limpieza
        self.cleanup_test_data()
    
    def cleanup_test_data(self):
        """Limpia los datos de prueba creados."""
        for user_id in self.cleanup_ids:
            try:
                requests.delete(f"{self.USER_SERVICE}/users/{user_id}")
            except:
                pass
    
    def create_test_user(self, suffix="") -> Dict[str, Any]:
        """Helper para crear un usuario de prueba."""
        user_data = {
            "firstName": f"E2E_User{suffix}",
            "lastName": f"Test{suffix}",
            "email": f"e2e.user{suffix}.{self.timestamp}@test.com",
            "phone": f"+57 300 {self.timestamp[-6:]}",
            "imageUrl": "https://example.com/avatar.jpg",
            "credentialDto": {
                "username": f"e2euser{suffix}_{self.timestamp}",
                "password": "$2a$10$N.zmdr9k7uOCQb07YxkiNOhsqlQ5166rWa8rN5.4aDh7d6c8QWsma",
                "roleBasedAuthority": "ROLE_USER",
                "isEnabled": True,
                "isAccountNonExpired": True,
                "isAccountNonLocked": True,
                "isCredentialsNonExpired": True
            }
        }
        
        response = requests.post(f"{self.USER_SERVICE}/users", headers=self.HEADERS, json=user_data)
        assert response.status_code == 200
        
        user = response.json()
        self.cleanup_ids.append(user["userId"])
        return user
    
    def test_complete_user_registration_flow(self):
        """
        E2E: Flujo completo de registro de usuario
        1. Crear usuario
        2. Verificar que se puede buscar por email
        3. Verificar que se puede autenticar (buscar por username)
        4. Actualizar perfil
        5. Verificar cambios
        """
        print("🎭 Ejecutando flujo completo de registro de usuario")
        
        # 1. Crear usuario (simula registro)
        user_data = {
            "firstName": "María",
            "lastName": "González",
            "email": f"maria.gonzalez.{self.timestamp}@empresa.com",
            "phone": "+57 315 123 4567",
            "credentialDto": {
                "username": f"mariagonzalez_{self.timestamp}",
                "password": "$2a$10$encodedPassword",
                "roleBasedAuthority": "ROLE_USER",
                "isEnabled": True,
                "isAccountNonExpired": True,
                "isAccountNonLocked": True,
                "isCredentialsNonExpired": True
            }
        }
        
        create_response = requests.post(f"{self.USER_SERVICE}/users", headers=self.HEADERS, json=user_data)
        assert create_response.status_code == 200
        user = create_response.json()
        self.cleanup_ids.append(user["userId"])
        
        print(f"✅ Usuario creado con ID: {user['userId']}")
        
        # 2. Verificar que el usuario existe (simula verificación de email)
        get_response = requests.get(f"{self.USER_SERVICE}/users/{user['userId']}")
        assert get_response.status_code == 200
        assert get_response.json()["email"] == user_data["email"]
        
        print("✅ Usuario verificado por ID")
        
        # 3. Buscar por username (simula login)
        username = user_data["credentialDto"]["username"]
        login_response = requests.get(f"{self.USER_SERVICE}/credentials/username/{username}")
        assert login_response.status_code == 200
        logged_user = login_response.json()
        
        print("✅ Usuario autenticado por username")
        
        # 4. Actualizar perfil (simula edición de perfil)
        update_data = {
            "userId": user["userId"],
            "firstName": "María Actualizada",
            "lastName": user["lastName"],
            "email": user["email"],
            "phone": "+57 316 999 8888",
            "credentialDto": user["credentialDto"]
        }
        
        update_response = requests.put(
            f"{self.USER_SERVICE}/users/{user['userId']}",
            headers=self.HEADERS,
            json=update_data
        )
        assert update_response.status_code == 200
        
        print("✅ Perfil actualizado")
        
        # 5. Verificar cambios persistieron
        final_response = requests.get(f"{self.USER_SERVICE}/users/{user['userId']}")
        final_user = final_response.json()
        assert final_user["firstName"] == "María Actualizada"
        assert final_user["phone"] == "+57 316 999 8888"
        
        print("✅ Cambios verificados - Flujo completo exitoso!")
    
    def test_user_lifecycle_with_role_change(self):
        """
        E2E: Flujo de cambio de rol de usuario
        1. Crear usuario normal
        2. Promover a admin
        3. Verificar permisos
        4. Degradar a usuario normal
        """
        print("👤 Ejecutando flujo de cambio de roles")
        
        # 1. Crear usuario normal
        user = self.create_test_user("_role")
        assert user["credentialDto"]["roleBasedAuthority"] == "ROLE_USER"
        
        print(f"✅ Usuario normal creado: {user['credentialDto']['username']}")
        
        # 2. Promover a admin (simula acción de admin)
        update_data = user.copy()
        update_data["credentialDto"]["roleBasedAuthority"] = "ROLE_ADMIN"
        
        promote_response = requests.put(
            f"{self.USER_SERVICE}/users/{user['userId']}",
            headers=self.HEADERS,
            json=update_data
        )
        assert promote_response.status_code == 200
        admin_user = promote_response.json()
        assert admin_user["credentialDto"]["roleBasedAuthority"] == "ROLE_ADMIN"
        
        print("✅ Usuario promovido a ADMIN")
        
        # 3. Verificar que el cambio persistió
        verify_response = requests.get(f"{self.USER_SERVICE}/users/{user['userId']}")
        verified_user = verify_response.json()
        assert verified_user["credentialDto"]["roleBasedAuthority"] == "ROLE_ADMIN"
        
        print("✅ Rol de admin verificado")
        
        # 4. Degradar a usuario normal
        update_data["credentialDto"]["roleBasedAuthority"] = "ROLE_USER"
        
        demote_response = requests.put(
            f"{self.USER_SERVICE}/users/{user['userId']}",
            headers=self.HEADERS,
            json=update_data
        )
        assert demote_response.status_code == 200
        
        # Verificar degradación
        final_response = requests.get(f"{self.USER_SERVICE}/users/{user['userId']}")
        final_user = final_response.json()
        assert final_user["credentialDto"]["roleBasedAuthority"] == "ROLE_USER"
        
        print("✅ Usuario degradado a ROLE_USER - Flujo de roles completo!")
    
    def test_multiple_users_interaction_flow(self):
        """
        E2E: Flujo de interacción entre múltiples usuarios
        1. Crear varios usuarios
        2. Verificar que aparecen en lista
        3. Simular actividad concurrente
        4. Cleanup selectivo
        """
        print("👥 Ejecutando flujo de múltiples usuarios")
        
        # 1. Crear múltiples usuarios (simula registros múltiples)
        users = []
        for i in range(3):
            user = self.create_test_user(f"_multi{i}")
            users.append(user)
            print(f"✅ Usuario {i+1} creado: {user['credentialDto']['username']}")
        
        # 2. Verificar que todos aparecen en lista
        all_users_response = requests.get(f"{self.USER_SERVICE}/users")
        assert all_users_response.status_code == 200
        
        all_users = all_users_response.json()["collection"]
        created_usernames = [u["credentialDto"]["username"] for u in users]
        existing_usernames = [u.get("credentialDto", {}).get("username") for u in all_users]
        
        for username in created_usernames:
            assert username in existing_usernames
        
        print("✅ Todos los usuarios aparecen en la lista")
        
        # 3. Simular actividad concurrente (actualizaciones)
        for i, user in enumerate(users):
            update_data = user.copy()
            update_data["firstName"] = f"Updated_User_{i}"
            
            update_response = requests.put(
                f"{self.USER_SERVICE}/users/{user['userId']}",
                headers=self.HEADERS,
                json=update_data
            )
            assert update_response.status_code == 200
        
        print("✅ Actualizaciones concurrentes exitosas")
        
        # 4. Verificar que las actualizaciones no se interfirieron
        for i, user in enumerate(users):
            verify_response = requests.get(f"{self.USER_SERVICE}/users/{user['userId']}")
            verified_user = verify_response.json()
            assert verified_user["firstName"] == f"Updated_User_{i}"
        
        print("✅ Flujo de múltiples usuarios completo!")
    
    def test_user_data_consistency_flow(self):
        """
        E2E: Flujo de verificación de consistencia de datos
        1. Crear usuario con datos específicos
        2. Verificar datos por diferentes endpoints
        3. Actualizar parcialmente
        4. Verificar consistencia en todos los endpoints
        """
        print("🔍 Ejecutando flujo de consistencia de datos")
        
        # 1. Crear usuario con datos específicos
        specific_username = f"consistency_user_{self.timestamp}"
        specific_email = f"consistency.{self.timestamp}@test.com"
        
        user_data = {
            "firstName": "Consistency",
            "lastName": "Test",
            "email": specific_email,
            "phone": "+57 320 111 2222",
            "credentialDto": {
                "username": specific_username,
                "password": "$2a$10$encoded",
                "roleBasedAuthority": "ROLE_USER",
                "isEnabled": True,
                "isAccountNonExpired": True,
                "isAccountNonLocked": True,
                "isCredentialsNonExpired": True
            }
        }
        
        create_response = requests.post(f"{self.USER_SERVICE}/users", headers=self.HEADERS, json=user_data)
        assert create_response.status_code == 200
        user = create_response.json()
        self.cleanup_ids.append(user["userId"])
        
        print(f"✅ Usuario de consistencia creado: {specific_username}")
        
        # 2. Verificar datos por diferentes endpoints
        # Por ID
        by_id_response = requests.get(f"{self.USER_SERVICE}/users/{user['userId']}")
        by_id_user = by_id_response.json()
        
        # Por username
        by_username_response = requests.get(f"{self.USER_SERVICE}/credentials/username/{specific_username}")
        by_username_user = by_username_response.json()
        
        # En lista general
        all_users_response = requests.get(f"{self.USER_SERVICE}/users")
        all_users = all_users_response.json()["collection"]
        user_in_list = next((u for u in all_users if u["userId"] == user["userId"]), None)
        
        # Verificar consistencia
        assert by_id_user["email"] == specific_email
        assert by_username_user["username"] == specific_username
        assert user_in_list["email"] == specific_email
        
        print("✅ Datos consistentes en todos los endpoints")
        
        # 3. Actualizar parcialmente
        update_data = by_id_user.copy()
        update_data["firstName"] = "Updated_Consistency"
        update_data["phone"] = "+57 321 999 8888"
        
        update_response = requests.put(
            f"{self.USER_SERVICE}/users/{user['userId']}",
            headers=self.HEADERS,
            json=update_data
        )
        assert update_response.status_code == 200
        
        print("✅ Actualización parcial realizada")
        
        # 4. Verificar consistencia post-actualización en todos los endpoints
        # Por ID (actualizado)
        updated_by_id = requests.get(f"{self.USER_SERVICE}/users/{user['userId']}").json()
        
        # Por username (actualizado)
        updated_by_username = requests.get(f"{self.USER_SERVICE}/credentials/username/{specific_username}").json()
        
        # Verificaciones finales
        assert updated_by_id["firstName"] == "Updated_Consistency"
        assert updated_by_id["phone"] == "+57 321 999 8888"
        assert updated_by_id["email"] == specific_email
        assert updated_by_username["username"] == specific_username
        
        print("✅ Consistencia de datos verificada post-actualización!")
    
    def test_error_handling_and_recovery_flow(self):
        """
        E2E: Flujo de manejo de errores y recuperación
        1. Intentar operaciones inválidas
        2. Verificar que el sistema mantiene estado consistente
        3. Realizar operaciones válidas después de errores
        """
        print("⚠️ Ejecutando flujo de manejo de errores")
        
        # 1. Crear usuario válido primero
        user = self.create_test_user("_error")
        original_username = user["credentialDto"]["username"]
        
        print(f"✅ Usuario base creado: {original_username}")
        
        # 2. Intentar buscar usuario inexistente
        invalid_id_response = requests.get(f"{self.USER_SERVICE}/users/999999")
        assert invalid_id_response.status_code == 400
        
        invalid_username_response = requests.get(f"{self.USER_SERVICE}/credentials/username/nonexistent")
        assert invalid_username_response.status_code == 400
        
        print("✅ Errores de búsqueda manejados correctamente")
        
        # 3. Verificar que el usuario original sigue intacto después de errores
        verify_response = requests.get(f"{self.USER_SERVICE}/users/{user['userId']}")
        assert verify_response.status_code == 200
        verified_user = verify_response.json()
        assert verified_user["credentialDto"]["username"] == original_username
        
        print("✅ Usuario original intacto después de errores")
        
        # 4. Realizar operación válida después de errores
        update_data = verified_user.copy()
        update_data["firstName"] = "Recovery_Test"
        
        recovery_response = requests.put(
            f"{self.USER_SERVICE}/users/{user['userId']}",
            headers=self.HEADERS,
            json=update_data
        )
        assert recovery_response.status_code == 200
        assert recovery_response.json()["firstName"] == "Recovery_Test"
        
        print("✅ Sistema recuperado - operaciones válidas funcionan post-error!")
    
    @pytest.mark.slow
    def test_service_availability_check(self):
        """
        E2E: Verificación básica de disponibilidad de servicios
        """
        print("🏥 Verificando disponibilidad de servicios")
        
        # Verificar User Service
        user_health = requests.get(f"{self.USER_SERVICE}/users")
        assert user_health.status_code in [200, 400]  # 400 puede ser válido si no hay datos
        
        print("✅ User Service disponible")
        
        # Si tienes API Gateway configurado, verificar
        try:
            gateway_health = requests.get(f"{self.API_GATEWAY}/user-service/api/users", timeout=5)
            if gateway_health.status_code in [200, 400]:
                print("✅ API Gateway disponible")
            else:
                print("⚠️ API Gateway responde pero con código no esperado")
        except requests.RequestException:
            print("⚠️ API Gateway no disponible o no configurado")
        
        print("✅ Verificación de servicios completada!")


# Para ejecutar solo pruebas E2E
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short", "-m", "not slow"]) 