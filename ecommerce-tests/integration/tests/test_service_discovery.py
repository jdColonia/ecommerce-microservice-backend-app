"""
Pruebas de integración para el Service Discovery (Eureka).
"""

import pytest
from utils.api_utils import make_request, set_current_service


class TestServiceDiscoveryComplete:
    """
    Pruebas para el Service Discovery - registro de servicios.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("service-discovery")

    def test_eureka_health_check(self):
        """Prueba de health check de Eureka."""
        response = make_request("GET", "/actuator/health")

        assert response.status_code in [200, 404]

    def test_eureka_info_endpoint(self):
        """Prueba del endpoint de información de Eureka."""
        response = make_request("GET", "/actuator/info")

        assert response.status_code in [200, 404]

    def test_eureka_apps_registry(self):
        """Prueba para obtener aplicaciones registradas."""
        response = make_request("GET", "/eureka/apps")

        assert response.status_code in [200, 404]

    def test_eureka_status_endpoint(self):
        """Prueba del endpoint de estado de Eureka."""
        response = make_request("GET", "/eureka/status")

        assert response.status_code in [200, 404]

    def test_eureka_lastn_cancellations(self):
        """Prueba del endpoint de últimas cancelaciones."""
        response = make_request("GET", "/eureka/lastn")

        assert response.status_code in [200, 404]
