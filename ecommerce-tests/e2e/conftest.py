"""
Configuración global para las pruebas e2e.
"""

import pytest
import uuid
import time
from typing import Dict, List
import requests
from config.config import (
    API_GATEWAY_URL,
    AUTH_ENDPOINT,
    TEST_USER,
    REQUEST_TIMEOUT,
    SERVICES_CONFIG,
    E2E_CONFIG,
)

_jwt_token = None
_current_service = ""


def set_current_service(service_name):
    """Establece el servicio actual para las pruebas."""
    global _current_service
    if service_name in SERVICES_CONFIG:
        _current_service = service_name
    else:
        raise ValueError(f"Servicio '{service_name}' no está configurado")


def get_auth_token():
    """Obtiene un token JWT de autenticación."""
    global _jwt_token

    if _jwt_token:
        return _jwt_token

    try:
        response = requests.post(
            AUTH_ENDPOINT,
            json={"username": TEST_USER["username"], "password": TEST_USER["password"]},
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=REQUEST_TIMEOUT,
        )

        if response.status_code == 200:
            auth_data = response.json()
            _jwt_token = auth_data.get("jwtToken")
            if _jwt_token:
                return _jwt_token
            else:
                raise Exception(f"Token no encontrado en la respuesta: {auth_data}")
        else:
            raise Exception(
                f"Error {response.status_code} al obtener token: {response.text}"
            )

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error de conexión al obtener token: {e}")


def make_request(
    method, endpoint, data=None, params=None, headers=None, service_name=None
):
    """Realiza una solicitud HTTP al servicio especificado."""
    if service_name is None:
        service_name = _current_service

    service_config = SERVICES_CONFIG.get(service_name)
    if not service_config:
        raise ValueError(f"Servicio '{service_name}' no está configurado")

    # Construir URL completa
    if endpoint.startswith("/"):
        endpoint = endpoint[1:]

    base_url = service_config["url"]
    path_prefix = service_config["path_prefix"]

    if path_prefix:
        url = f"{base_url}/{path_prefix}/{endpoint}"
    else:
        url = f"{base_url}/{endpoint}"

    # Headers según el servicio
    request_headers = {"Content-Type": "application/json", "Accept": "application/json"}

    if service_config.get("requires_auth", True):
        token = get_auth_token()
        request_headers["Authorization"] = f"Bearer {token}"

    if headers:
        request_headers.update(headers)

    # Realizar solicitud con reintentos
    for attempt in range(E2E_CONFIG["max_retries"]):
        try:
            if method.upper() == "GET":
                return requests.get(
                    url, headers=request_headers, params=params, timeout=REQUEST_TIMEOUT
                )
            elif method.upper() == "POST":
                return requests.post(
                    url, headers=request_headers, json=data, timeout=REQUEST_TIMEOUT
                )
            elif method.upper() == "PUT":
                return requests.put(
                    url, headers=request_headers, json=data, timeout=REQUEST_TIMEOUT
                )
            elif method.upper() == "DELETE":
                return requests.delete(
                    url, headers=request_headers, timeout=REQUEST_TIMEOUT
                )
            else:
                raise ValueError(f"Método HTTP no soportado: {method}")

        except requests.exceptions.RequestException as e:
            if attempt < E2E_CONFIG["max_retries"] - 1:
                time.sleep(E2E_CONFIG["retry_delay"])
                continue
            else:
                raise


@pytest.fixture(scope="session", autouse=True)
def setup_e2e_environment():
    """Configura el entorno de pruebas E2E antes de ejecutar las pruebas."""
    print("\n=== Configurando entorno de pruebas E2E ===")

    # Verificar conectividad básica con el API Gateway
    try:
        response = requests.get(
            f"{API_GATEWAY_URL}/actuator/health", timeout=REQUEST_TIMEOUT
        )
        if response.status_code not in [200, 404]:
            pytest.fail("API Gateway no está disponible para las pruebas E2E")
    except:
        pytest.fail("No se puede conectar al API Gateway")

    print("✅ Entorno de pruebas E2E configurado correctamente")
    yield
    print("\n=== Limpieza del entorno de pruebas E2E ===")


@pytest.fixture
def cleanup_resources():
    """Fixture para limpiar recursos creados durante las pruebas E2E."""
    created_resources = {
        "users": [],
        "products": [],
        "categories": [],
        "orders": [],
        "carts": [],
        "payments": [],
        "favourites": [],
        "shippings": [],
        "addresses": [],
        "credentials": [],
        "verification_tokens": [],
    }

    yield created_resources

    # Cleanup en orden de dependencias
    if E2E_CONFIG["cleanup_after_test"]:
        cleanup_test_data(created_resources)


def cleanup_test_data(resources: Dict[str, List]):
    """Limpia los recursos de prueba creados."""
    cleanup_order = [
        ("verification_tokens", "api/verificationTokens"),
        ("credentials", "api/credentials"),
        ("addresses", "api/address"),
        ("favourites", "api/favourites"),
        ("shippings", "api/shippings"),
        ("payments", "api/payments"),
        ("orders", "api/orders"),
        ("carts", "api/carts"),
        ("products", "api/products"),
        ("categories", "api/categories"),
        ("users", "api/users"),
    ]

    for resource_type, endpoint in cleanup_order:
        resource_ids = resources.get(resource_type, [])
        for resource_id in resource_ids:
            try:
                # Determinar el servicio correcto para cada tipo de recurso
                if resource_type in [
                    "users",
                    "addresses",
                    "credentials",
                    "verification_tokens",
                ]:
                    set_current_service("user-service")
                elif resource_type in ["products", "categories"]:
                    set_current_service("product-service")
                elif resource_type in ["orders", "carts"]:
                    set_current_service("order-service")
                elif resource_type == "payments":
                    set_current_service("payment-service")
                elif resource_type == "favourites":
                    set_current_service("favourite-service")
                elif resource_type == "shippings":
                    set_current_service("shipping-service")

                # Realizar eliminación
                if isinstance(resource_id, tuple):
                    # Para recursos con múltiples IDs (como favourites)
                    delete_url = f"{endpoint}/" + "/".join(map(str, resource_id))
                else:
                    delete_url = f"{endpoint}/{resource_id}"

                make_request("DELETE", delete_url)
            except Exception:
                pass  # Ignorar errores de limpieza


def generate_unique_id():
    """Genera un ID único para las pruebas."""
    return f"{E2E_CONFIG['test_data_prefix']}{uuid.uuid4().hex[:8]}"
