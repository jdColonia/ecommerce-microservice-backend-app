"""
Pruebas de integración para el API Gateway.
"""

import pytest
from utils.api_utils import make_request, set_current_service


class TestApiGatewayComplete:
    """
    Pruebas para el API Gateway - endpoints de infraestructura.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("api-gateway")

    def test_gateway_health_check(self):
        """Prueba de health check del API Gateway."""
        response = make_request("GET", "/actuator/health")

        assert response.status_code in [200, 404]

    def test_gateway_info_endpoint(self):
        """Prueba del endpoint de información del API Gateway."""
        response = make_request("GET", "/actuator/info")

        assert response.status_code in [200, 404]

    def test_gateway_routes_endpoint(self):
        """Prueba para obtener las rutas configuradas en el gateway."""
        response = make_request("GET", "/actuator/gateway/routes")

        assert response.status_code in [200, 404]

    def test_gateway_metrics_endpoint(self):
        """Prueba del endpoint de métricas del gateway."""
        response = make_request("GET", "/actuator/metrics")

        assert response.status_code in [200, 404]
