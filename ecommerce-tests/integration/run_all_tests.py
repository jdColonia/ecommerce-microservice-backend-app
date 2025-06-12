"""
Script para ejecutar todas las pruebas de integración del ecosistema de microservicios.
"""

import pytest
import os
import sys
import datetime
import argparse
from pathlib import Path


def main():
    """
    Ejecuta las pruebas de integración para todos los servicios.
    """
    parser = argparse.ArgumentParser(
        description="Ejecutar pruebas de integración para todo el ecosistema de microservicios"
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
            "infrastructure",
            "business",
            "api-gateway",
            "cloud-config",
            "service-discovery",
            "proxy-client",
            "user-service",
            "product-service",
            "order-service",
            "payment-service",
            "favourite-service",
            "shipping-service",
        ],
        help="Ejecuta pruebas solo para un servicio o categoría específica",
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
        help="Solo ejecuta pruebas de conectividad",
    )
    parser.add_argument(
        "--method",
        "-m",
        type=str,
        choices=["save", "update", "delete", "find", "health"],
        help="Ejecuta solo métodos específicos (save, update, delete, find, health)",
    )
    parser.add_argument(
        "--gateway-url",
        type=str,
        help="URL del API Gateway (ej: http://localhost:8080)",
    )

    args = parser.parse_args()

    # Configurar URL del Gateway si se proporciona
    if args.gateway_url:
        os.environ["API_GATEWAY_URL"] = args.gateway_url
        print(f"🌐 Usando API Gateway: {args.gateway_url}")

    # Directorio de pruebas
    test_dir = Path(__file__).parent

    # Configuración de servicios
    service_groups = {
        "infrastructure": [
            "test_api_gateway.py",
            "test_cloud_config.py",
            "test_service_discovery.py",
            "test_proxy_client.py",
        ],
        "business": [
            "test_user_service.py",
            "test_product_service.py",
            "test_order_service.py",
            "test_payment_service.py",
            "test_favourite_service.py",
            "test_shipping_service.py",
        ],
        "api-gateway": ["test_api_gateway.py"],
        "cloud-config": ["test_cloud_config.py"],
        "service-discovery": ["test_service_discovery.py"],
        "proxy-client": ["test_proxy_client.py"],
        "user-service": ["test_user_service.py"],
        "product-service": ["test_product_service.py"],
        "order-service": ["test_order_service.py"],
        "payment-service": ["test_payment_service.py"],
        "favourite-service": ["test_favourite_service.py"],
        "shipping-service": ["test_shipping_service.py"],
    }

    # Determinar archivos de prueba a ejecutar
    test_files = []
    if args.service:
        if args.service in service_groups:
            test_files = [f"tests/{f}" for f in service_groups[args.service]]
        else:
            print(f"❌ Servicio '{args.service}' no encontrado")
            sys.exit(1)
    else:
        # Ejecutar todos los servicios
        all_files = set()
        for files in service_groups.values():
            all_files.update(files)
        test_files = [f"tests/{f}" for f in all_files]

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

    # Solo conectividad
    if args.connectivity_only:
        pytest_args.extend(["-k", "health"])

    # Filtros por método
    if args.method:
        if args.connectivity_only:
            # Combinar filtros
            current_filter = pytest_args[-1]
            pytest_args[-1] = f"{current_filter} and {args.method}"
        else:
            pytest_args.extend(["-k", args.method])

    # Archivos de prueba
    pytest_args.extend(existing_files)

    # Reporte HTML
    if args.html:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"all_services_report_{timestamp}.html"
        if args.service:
            report_name = f"{args.service}_report_{timestamp}.html"
        report_path = test_dir / report_name
        pytest_args.extend(["--html", str(report_path), "--self-contained-html"])
        print(f"📊 Reporte HTML se generará en: {report_path}")

    # Ejecución en paralelo
    if args.parallel:
        pytest_args.extend(["-n", "auto"])

    # Mostrar configuración
    print("=== Configuración de Pruebas de Integración ===")
    if args.service:
        print(f"🎯 Servicio/Categoría: {args.service}")
    else:
        print("🌐 Ejecutando: Todos los servicios")
    print(f"📁 Archivos de prueba: {len(existing_files)}")
    for f in existing_files:
        print(f"  - {Path(f).name}")
    print(
        f"⚙️ Argumentos pytest: {' '.join(pytest_args[-5:])}"
    )  # Solo últimos argumentos
    print("=" * 50)

    # Ejecutar pytest
    print("🚀 Iniciando ejecución de pruebas...")
    exit_code = pytest.main(pytest_args)

    # Resumen
    if exit_code == 0:
        print("\n✅ Todas las pruebas pasaron exitosamente")
        if args.service:
            print(f"📊 Servicio probado: {args.service}")
        else:
            print("📊 Todo el ecosistema de microservicios verificado")
    else:
        print(f"\n❌ Algunas pruebas fallaron (código de salida: {exit_code})")

    sys.exit(exit_code)


def run_connectivity_check():
    """
    Ejecuta una verificación rápida de conectividad de todos los servicios.
    """
    print("🔍 Ejecutando verificación de conectividad...")

    from utils.api_utils import test_all_services_connectivity

    results = test_all_services_connectivity()

    available_count = sum(1 for status in results.values() if status)
    total_count = len(results)

    print(f"\n📊 Resultado: {available_count}/{total_count} servicios disponibles")

    if available_count == total_count:
        print("🎉 Todos los servicios están disponibles")
        return True
    elif available_count > 0:
        print("⚠️ Algunos servicios están disponibles")
        return True
    else:
        print("❌ Ningún servicio está disponible")
        return False


def run_auth_test():
    """
    Prueba específicamente el flujo de autenticación para servicios que lo requieren.
    """
    print("🔐 Probando autenticación...")

    try:
        from utils.api_utils import get_auth_token, reset_auth_token

        # Resetear token para probar desde cero
        reset_auth_token()

        # Intentar obtener token
        token = get_auth_token()

        if token:
            print(f"✅ Token obtenido exitosamente: {token[:20]}...")
            return True
        else:
            print("❌ No se pudo obtener token de autenticación")
            return False

    except Exception as e:
        print(f"❌ Error en autenticación: {e}")
        return False


def run_smoke_tests():
    """
    Ejecuta pruebas de humo (smoke tests) básicas para todos los servicios.
    """
    print("🔥 Ejecutando pruebas de humo...")

    # Pruebas básicas solo de health/conectividad
    smoke_args = [
        "-v",
        "-k",
        "health",  # Solo pruebas de health
        "tests/",
    ]

    exit_code = pytest.main(smoke_args)

    if exit_code == 0:
        print("✅ Pruebas de humo pasaron")
    else:
        print("❌ Pruebas de humo fallaron")

    return exit_code == 0


def run_infrastructure_tests():
    """
    Ejecuta solo las pruebas de servicios de infraestructura.
    """
    print("🏗️ Ejecutando pruebas de infraestructura...")

    infrastructure_args = [
        "-v",
        "tests/test_api_gateway.py",
        "tests/test_cloud_config.py",
        "tests/test_service_discovery.py",
        "tests/test_proxy_client.py",
    ]

    exit_code = pytest.main(infrastructure_args)
    return exit_code == 0


def run_business_tests():
    """
    Ejecuta solo las pruebas de microservicios de negocio.
    """
    print("💼 Ejecutando pruebas de microservicios de negocio...")

    business_args = [
        "-v",
        "tests/test_user_service.py",
        "tests/test_product_service.py",
        "tests/test_order_service.py",
        "tests/test_payment_service.py",
        "tests/test_favourite_service.py",
        "tests/test_shipping_service.py",
    ]

    exit_code = pytest.main(business_args)
    return exit_code == 0


if __name__ == "__main__":
    # Verificar argumentos especiales
    if len(sys.argv) > 1:
        if sys.argv[1] == "--connectivity":
            success = run_connectivity_check()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--infrastructure":
            success = run_infrastructure_tests()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--business":
            success = run_business_tests()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--smoke":
            success = run_smoke_tests()
            sys.exit(0 if success else 1)
        elif sys.argv[1] == "--auth":
            success = run_auth_test()
            sys.exit(0 if success else 1)

    # Ejecución normal
    main()
