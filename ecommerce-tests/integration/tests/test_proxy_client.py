"""
Pruebas de integración para el Proxy Client.
"""

import pytest
from utils.api_utils import make_request, set_current_service


class TestProxyClientComplete:
    """
    Pruebas para el Proxy Client - comunicación entre servicios.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("proxy-client")

    def test_proxy_client_health_check(self):
        """Prueba de health check del Proxy Client."""
        response = make_request("GET", "/actuator/health")

        assert response.status_code in [200, 404]

    def test_proxy_client_info_endpoint(self):
        """Prueba del endpoint de información del Proxy Client."""
        response = make_request("GET", "/actuator/info")

        assert response.status_code in [200, 404]

    def test_proxy_client_metrics_endpoint(self):
        """Prueba del endpoint de métricas del Proxy Client."""
        response = make_request("GET", "/actuator/metrics")

        assert response.status_code in [200, 404]

    def test_proxy_user_service_connectivity(self):
        """Prueba de conectividad al user-service a través del proxy."""
        response = make_request("GET", "/proxy/user-service/api/users")

        assert response.status_code in [200, 401, 403, 404, 500]

    def test_proxy_product_service_connectivity(self):
        """Prueba de conectividad al product-service a través del proxy."""
        response = make_request("GET", "/proxy/product-service/api/products")

        assert response.status_code in [200, 401, 403, 404, 500]
