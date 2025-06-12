"""
Script para ejecutar pruebas de integración.
"""

import pytest
import os
import sys
import datetime
import argparse

def main():
    """
    Ejecuta las pruebas de integración.
    """
    parser = argparse.ArgumentParser(description='Ejecutar pruebas de integración para microservicios de e-commerce')
    parser.add_argument('--verbose', '-v', action='store_true', help='Muestra más información durante la ejecución')
    parser.add_argument('--html', action='store_true', help='Genera un reporte HTML')
    parser.add_argument('--parallel', '-p', action='store_true', help='Ejecuta las pruebas en paralelo')
    parser.add_argument('--service', '-s', type=str, help='Ejecuta pruebas solo para un servicio específico (user, product, order, etc.)')
    
    args = parser.parse_args()
    
    # Directorio de pruebas
    test_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Argumentos para pytest
    pytest_args = ['-v'] if args.verbose else []
    
    # Si se especificó un servicio
    if args.service:
        pytest_args.append(f"tests/test_{args.service}_service.py")
    else:
        pytest_args.append('tests/')
    
    # Reporte HTML
    if args.html:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(test_dir, f"report_{timestamp}.html")
        pytest_args.extend(['--html', report_path, '--self-contained-html'])
    
    # Ejecución en paralelo
    if args.parallel:
        pytest_args.append('-xvs')
        pytest_args.append('-n')
        pytest_args.append('auto')
    
    # Ejecutamos pytest
    sys.exit(pytest.main(pytest_args))

if __name__ == "__main__":
    main()
