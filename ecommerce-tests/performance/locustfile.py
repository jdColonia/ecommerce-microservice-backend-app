"""
Archivo principal para pruebas de rendimiento con Locust.

Ejecutar con:
    locust -f locustfile.py --host=https://api-gateway.your-cluster.com
    
O con interfaz web:
    locust -f locustfile.py
"""

import os
import sys
import logging
from locust import events
from dotenv import load_dotenv

# Asegurarse de que los módulos puedan ser importados
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Cargar variables de entorno
load_dotenv()

# Importar tipos de usuarios
from locustfiles.browse_user import BrowseUser
from locustfiles.buyer_user import BuyerUser
from locustfiles.admin_user import AdminUser

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("locust.log"),
        logging.StreamHandler()
    ]
)

# Eventos de Locust
@events.init.add_listener
def on_locust_init(environment, **kwargs):
    """
    Evento llamado cuando Locust se inicializa.
    """
    logging.info("Iniciando pruebas de rendimiento con Locust")

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    """
    Evento llamado cuando se completa una petición.
    """
    if exception:
        logging.error(f"Request {name} falló: {exception}")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """
    Evento llamado cuando comienza la prueba de carga.
    """
    logging.info(f"Prueba iniciada: {environment.host}")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """
    Evento llamado cuando finaliza la prueba de carga.
    """
    logging.info("Prueba finalizada")
    
    # Estadísticas
    stats = environment.stats
    total_requests = stats.total.num_requests
    total_failures = stats.total.num_failures
    total_response_time = stats.total.avg_response_time
    
    logging.info(f"Total peticiones: {total_requests}")
    logging.info(f"Total fallos: {total_failures}")
    logging.info(f"Tiempo medio de respuesta: {total_response_time:.2f} ms")
    
    # Guardar estadísticas en CSV
    stats.write_csv_files("locust_stats")
