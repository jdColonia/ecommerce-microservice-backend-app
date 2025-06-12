"""
Script para ejecutar pruebas E2E.
"""

import pytest
import os
import sys
import datetime
import argparse
import logging
from config.config import LOG_LEVEL

def setup_logging(log_level):
    """Configura el logging para las pruebas."""
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("e2e_tests.log"),
            logging.StreamHandler()
        ]
    )

def main():
    """
    Ejecuta las pruebas E2E.
    """
    parser = argparse.ArgumentParser(description='Ejecutar pruebas E2E para microservicios de e-commerce')
    parser.add_argument('--verbose', '-v', action='store_true', help='Muestra más información durante la ejecución')
    parser.add_argument('--html', action='store_true', help='Genera un reporte HTML')
    parser.add_argument('--scenario', '-s', type=str, help='Ejecuta un escenario específico (purchase, user, inventory)')
    parser.add_argument('--log-level', type=str, default=LOG_LEVEL, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                        help='Nivel de logging')
    parser.add_argument('--record', '-r', action='store_true', help='Graba las peticiones y respuestas para depuración')
    parser.add_argument('--failfast', '-f', action='store_true', help='Detiene las pruebas en el primer fallo')
    
    args = parser.parse_args()
    
    # Configurar logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Iniciando pruebas E2E")
    
    # Directorio de pruebas
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Argumentos para pytest
    pytest_args = ['-v'] if args.verbose else []
    
    # Si se especificó un escenario
    if args.scenario:
        pytest_args.append(f"scenarios/test_{args.scenario}.py")
    else:
        pytest_args.append('scenarios/')
    
    # Reporte HTML
    if args.html:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(test_dir, f"e2e_report_{timestamp}.html")
        pytest_args.extend(['--html', report_path, '--self-contained-html'])
    
    # Grabar peticiones para depuración
    if args.record:
        pytest_args.append('--vcr-record=new_episodes')
    
    # Detener en el primer fallo
    if args.failfast:
        pytest_args.append('--exitfirst')
    
    logger.info(f"Ejecutando pytest con argumentos: {pytest_args}")
    
    # Ejecutamos pytest
    result = pytest.main(pytest_args)
    
    logger.info(f"Pruebas E2E completadas con código de salida: {result}")
    sys.exit(result)

if __name__ == "__main__":
    main()
