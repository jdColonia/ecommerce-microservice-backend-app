"""
Archivo de inicio para las pruebas de integración.
"""

import pytest
from utils.api_utils import (
    wait_for_services,
    reset_auth_token,
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """
    Configura el entorno de pruebas antes de ejecutar las pruebas.
    Verifica que el API Gateway y todos los servicios estén disponibles.
    """
    print("\n=== Configurando entorno de pruebas vía API Gateway ===")

    # Verificar que todos los servicios estén disponibles
    if not wait_for_services():
        pytest.fail(
            "Los servicios no están disponibles para las pruebas vía API Gateway"
        )

    print("✅ Entorno de pruebas configurado correctamente")
    print("🌐 Todas las pruebas se ejecutarán vía API Gateway")

    yield

    print("\n=== Limpieza del entorno de pruebas ===")
    reset_auth_token()


@pytest.fixture(scope="function")
def clean_test_data():
    """
    Fixture para limpiar datos de prueba después de cada test.
    """
    # Setup: Lista para tracking de recursos creados
    created_resources = {
        "users": [],
        "addresses": [],
        "credentials": [],
        "verification_tokens": [],
    }

    yield created_resources

    # Teardown: Limpiar recursos creados durante la prueba
    from utils.api_utils import make_request

    # Limpiar en orden inverso de dependencias
    for token_id in created_resources.get("verification_tokens", []):
        try:
            make_request("DELETE", f"/api/verificationTokens/{token_id}")
        except:
            pass  # Ignorar errores de limpieza

    for credential_id in created_resources.get("credentials", []):
        try:
            make_request("DELETE", f"/api/credentials/{credential_id}")
        except:
            pass

    for address_id in created_resources.get("addresses", []):
        try:
            make_request("DELETE", f"/api/address/{address_id}")
        except:
            pass

    for user_id in created_resources.get("users", []):
        try:
            make_request("DELETE", f"/api/users/{user_id}")
        except:
            pass


@pytest.fixture
def test_markers():
    """
    Fixture para marcar diferentes tipos de pruebas.
    """
    return {
        "integration": "Prueba de integración",
        "user_service": "Prueba específica del user-service",
        "happy_path": "Prueba de caso feliz",
    }
