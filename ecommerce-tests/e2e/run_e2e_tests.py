"""
Script para ejecutar todas las pruebas E2E del ecosistema de microservicios.
"""

import pytest
import os
import sys
import datetime
import argparse
from pathlib import Path


def main():
    """
    Ejecuta las pruebas E2E para todos los servicios.
    """
    parser = argparse.ArgumentParser(
        description="Ejecutar pruebas E2E para todo el ecosistema de microservicios"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Muestra más información durante la ejecución",
    )
    parser.add_argument("--html", action="store_true", help="Genera un reporte HTML")
    parser.add_argument(
        "--parallel", "-p", action="store_true", help="Ejecuta las pruebas en paralelo"
    )
    parser.add_argument(
        "--service",
        "-s",
        type=str,
        choices=[
            "all",
            "user-service",
            "product-service",
            "order-service",
            "payment-service",
            "favourite-service",
            "shipping-service",
            "proxy-client",
        ],
        default="all",
        help="Ejecuta pruebas solo para un servicio específico",
    )
    parser.add_argument(
        "--fail-fast",
        "-x",
        action="store_true",
        help="Detiene la ejecución en el primer fallo",
    )
    parser.add_argument(
        "--connectivity-only",
        action="store_true",
        help="Solo ejecuta pruebas de conectividad básica",
    )
    parser.add_argument(
        "--gateway-url",
        type=str,
        help="URL del API Gateway (ej: http://localhost:8222)",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Ejecuta limpieza de datos de prueba antes de comenzar",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Timeout en segundos para cada prueba (default: 300)",
    )

    args = parser.parse_args()

    # Configurar URL del Gateway si se proporciona
    if args.gateway_url:
        os.environ["API_GATEWAY_URL"] = args.gateway_url
        print(f"🌐 Usando API Gateway: {args.gateway_url}")

    # Directorio de pruebas
    test_dir = Path(__file__).parent

    # Configuración de servicios y sus archivos de prueba
    service_test_files = {
        "user-service": "tests/test_user_service.py",
        "product-service": "tests/test_product_service.py",
        "order-service": "tests/test_order_service.py",
        "payment-service": "tests/test_payment_service.py",
        "favourite-service": "tests/test_favourite_service.py",
        "shipping-service": "tests/test_shipping_service.py",
        "proxy-client": "tests/test_proxy_client.py",
    }

    # Determinar archivos de prueba a ejecutar
    test_files = []
    if args.service == "all":
        test_files = list(service_test_files.values())
    else:
        if args.service in service_test_files:
            test_files = [service_test_files[args.service]]
        else:
            print(f"❌ Servicio '{args.service}' no encontrado")
            sys.exit(1)

    # Verificar que los archivos existen
    existing_files = []
    for test_file in test_files:
        full_path = test_dir / test_file
        if full_path.exists():
            existing_files.append(str(full_path))
        else:
            print(f"⚠️ Archivo no encontrado: {test_file}")

    if not existing_files:
        print("❌ No se encontraron archivos de prueba válidos")
        sys.exit(1)

    # Argumentos para pytest
    pytest_args = []

    # Verbosidad
    if args.verbose:
        pytest_args.extend(["-v", "-s"])
    else:
        pytest_args.extend(["-v"])

    # Fail fast
    if args.fail_fast:
        pytest_args.append("-x")

    # Timeout
    pytest_args.extend(["--timeout", str(args.timeout)])

    # Solo conectividad
    if args.connectivity_only:
        pytest_args.extend(["-k", "connectivity or health"])

    # Archivos de prueba
    pytest_args.extend(existing_files)

    # Reporte HTML
    if args.html:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"e2e_report_{timestamp}.html"
        if args.service != "all":
            report_name = f"e2e_{args.service}_report_{timestamp}.html"
        report_path = test_dir / report_name
        pytest_args.extend(["--html", str(report_path), "--self-contained-html"])
        print(f"📊 Reporte HTML se generará en: {report_path}")

    # Ejecución en paralelo
    if args.parallel:
        pytest_args.extend(["-n", "auto"])

    # Mostrar configuración
    print("=== Configuración de Pruebas E2E ===")
    if args.service != "all":
        print(f"🎯 Servicio: {args.service}")
    else:
        print("🌐 Ejecutando: Todos los servicios")
    print(f"📁 Archivos de prueba: {len(existing_files)}")
    for f in existing_files:
        print(f"  - {Path(f).name}")
    print(f"⚙️ Timeout por prueba: {args.timeout}s")
    if args.clean:
        print("🧹 Limpieza de datos habilitada")
    print("=" * 50)

    # Verificación previa del entorno
    print("🔍 Verificando entorno de pruebas...")

    try:
        import requests

        gateway_url = os.getenv("API_GATEWAY_URL", "http://localhost:8222")

        # Verificación básica de conectividad
        response = requests.get(f"{gateway_url}/actuator/health", timeout=10)
        if response.status_code in [200, 404]:
            print("✅ API Gateway accesible")
        else:
            print(f"⚠️ API Gateway responde con código: {response.status_code}")
    except Exception as e:
        print(f"⚠️ No se pudo verificar API Gateway: {e}")
        print("   Continuando con las pruebas...")

    # Ejecutar pytest
    print("🚀 Iniciando ejecución de pruebas E2E...")
    exit_code = pytest.main(pytest_args)

    # Resumen
    if exit_code == 0:
        print("\n✅ Todas las pruebas E2E pasaron exitosamente")
        if args.service != "all":
            print(f"📊 Servicio probado: {args.service}")
        else:
            print("📊 Todo el ecosistema de microservicios verificado")
    else:
        print(f"\n❌ Algunas pruebas E2E fallaron (código de salida: {exit_code})")

    sys.exit(exit_code)


def run_quick_smoke_test():
    """
    Ejecuta una verificación rápida de humo de todos los servicios.
    """
    print("🔥 Ejecutando pruebas de humo E2E...")

    # Pruebas básicas de conectividad
    smoke_args = [
        "-v",
        "-k",
        "connectivity or health",
        "--timeout",
        "60",
        "tests/",
    ]

    exit_code = pytest.main(smoke_args)

    if exit_code == 0:
        print("✅ Pruebas de humo E2E pasaron")
    else:
        print("❌ Pruebas de humo E2E fallaron")

    return exit_code == 0


def run_service_specific_test(service_name):
    """
    Ejecuta pruebas E2E para un servicio específico.

    Args:
        service_name (str): Nombre del servicio a probar
    """
    print(f"🎯 Ejecutando pruebas E2E para {service_name}...")

    service_args = [
        "-v",
        "-s",
        f"tests/test_{service_name.replace('-', '_')}.py",
        "--timeout",
        "300",
    ]

    exit_code = pytest.main(service_args)
    return exit_code == 0


def generate_coverage_report():
    """
    Genera un reporte de cobertura de las pruebas E2E.
    """
    print("📊 Generando reporte de cobertura E2E...")

    coverage_args = ["--cov=tests", "--cov-report=html", "--cov-report=term", "tests/"]

    exit_code = pytest.main(coverage_args)
    return exit_code == 0


if __name__ == "__main__":
    # Verificar argumentos especiales
    if len(sys.argv) > 1:
        if sys.argv[1] == "--smoke":
            success = run_quick_smoke_test()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--coverage":
            success = generate_coverage_report()
            sys.exit(0 if success else 1)
        elif sys.argv[1].startswith("--service="):
            service = sys.argv[1].split("=")[1]
            success = run_service_specific_test(service)
            sys.exit(0 if success else 1)

    # Ejecución normal
    main()
