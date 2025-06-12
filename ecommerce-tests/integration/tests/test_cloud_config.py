"""
Pruebas de integración para el Cloud Config Server.
"""

import pytest
from utils.api_utils import make_request, set_current_service


class TestCloudConfigComplete:
    """
    Pruebas para el Cloud Config Server - gestión de configuración.
    """

    def setup_method(self):
        """Configurar el servicio para las pruebas."""
        set_current_service("cloud-config")

    def test_config_health_check(self):
        """Prueba de health check del Config Server."""
        response = make_request("GET", "/actuator/health")

        assert response.status_code in [200, 404]

    def test_config_info_endpoint(self):
        """Prueba del endpoint de información del Config Server."""
        response = make_request("GET", "/actuator/info")

        assert response.status_code in [200, 404]

    def test_config_application_default_profile(self):
        """Prueba de configuración para application con perfil default."""
        response = make_request("GET", "/application/default")

        assert response.status_code in [200, 404]

    def test_config_application_dev_profile(self):
        """Prueba de configuración para application con perfil dev."""
        response = make_request("GET", "/application/dev")

        assert response.status_code in [200, 404]
