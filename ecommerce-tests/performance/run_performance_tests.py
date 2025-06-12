"""
Script para ejecutar pruebas de rendimiento con Locust en diferentes escenarios.
"""

import os
import sys
import argparse
import subprocess
import datetime
import time
import json
from pathlib import Path

def run_scenario(scenario_name, users, spawn_rate, run_time, host, headless=True):
    """
    Ejecuta un escenario de prueba de carga.
    
    Args:
        scenario_name (str): Nombre del escenario
        users (int): Número de usuarios concurrentes
        spawn_rate (int): Tasa de usuarios nuevos por segundo
        run_time (str): Tiempo de ejecución (ej: "30s", "5m", "1h")
        host (str): URL del host a probar
        headless (bool): Si se ejecuta sin interfaz gráfica
    
    Returns:
        tuple: (Código de salida, Ruta del informe)
    """
    print(f"\n{'='*80}")
    print(f"Ejecutando escenario: {scenario_name}")
    print(f"Usuarios: {users}, Tasa: {spawn_rate}/s, Duración: {run_time}")
    print(f"{'='*80}\n")
    
    # Crear directorio para informes
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_dir = Path(f"reports/{scenario_name}/{timestamp}")
    report_dir.mkdir(parents=True, exist_ok=True)
    
    # Construir comando
    cmd = [
        "locust",
        "-f", "locustfile.py",
        "--host", host,
        "--headless" if headless else "",
        "--users", str(users),
        "--spawn-rate", str(spawn_rate),
        "--run-time", run_time,
        "--html", str(report_dir / "report.html"),
        "--csv", str(report_dir / "stats")
    ]
    
    # Filtrar elementos vacíos
    cmd = [c for c in cmd if c]
    
    # Guardar configuración
    config = {
        "scenario": scenario_name,
        "users": users,
        "spawn_rate": spawn_rate,
        "run_time": run_time,
        "host": host,
        "timestamp": timestamp,
        "command": " ".join(cmd)
    }
    
    with open(report_dir / "config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    # Ejecutar Locust
    start_time = time.time()
    process = subprocess.run(cmd, capture_output=True, text=True)
    end_time = time.time()
    
    # Guardar salida
    with open(report_dir / "stdout.log", "w") as f:
        f.write(process.stdout)
    
    with open(report_dir / "stderr.log", "w") as f:
        f.write(process.stderr)
    
    # Guardar resultados
    results = {
        "exit_code": process.returncode,
        "duration": end_time - start_time,
        "timestamp_end": datetime.datetime.now().isoformat()
    }
    
    with open(report_dir / "results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nEscenario {scenario_name} completado en {end_time - start_time:.2f} segundos")
    print(f"Informe guardado en: {report_dir}")
    
    return process.returncode, report_dir

def main():
    """
    Ejecuta diferentes escenarios de prueba de carga.
    """
    parser = argparse.ArgumentParser(description='Ejecutar pruebas de rendimiento con Locust')
    parser.add_argument('--host', type=str, default=os.getenv('API_BASE_URL', 'https://api-gateway.your-cluster.com'),
                        help='URL del host a probar')
    parser.add_argument('--gui', action='store_true', help='Ejecutar con interfaz gráfica')
    parser.add_argument('--scenario', type=str, choices=['light', 'medium', 'heavy', 'spike', 'endurance', 'all'],
                        default='all', help='Escenario a ejecutar')
    
    args = parser.parse_args()
    
    # Definir escenarios
    scenarios = {
        'light': {
            'users': 10,
            'spawn_rate': 5,
            'run_time': '1m'
        },
        'medium': {
            'users': 50,
            'spawn_rate': 10,
            'run_time': '3m'
        },
        'heavy': {
            'users': 100,
            'spawn_rate': 20,
            'run_time': '5m'
        },
        'spike': {
            'users': 200,
            'spawn_rate': 50,
            'run_time': '2m'
        },
        'endurance': {
            'users': 30,
            'spawn_rate': 5,
            'run_time': '10m'
        }
    }
    
    # Ejecutar escenarios seleccionados
    if args.scenario == 'all':
        for name, config in scenarios.items():
            run_scenario(
                name,
                config['users'],
                config['spawn_rate'],
                config['run_time'],
                args.host,
                not args.gui
            )
    else:
        config = scenarios[args.scenario]
        run_scenario(
            args.scenario,
            config['users'],
            config['spawn_rate'],
            config['run_time'],
            args.host,
            not args.gui
        )

if __name__ == "__main__":
    main()
