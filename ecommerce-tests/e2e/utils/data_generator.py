"""
Generador de datos de prueba para E2E tests.
"""

import uuid
import random
import string
import datetime
from typing import Dict, Any, List, Optional

def generate_unique_username() -> str:
    """
    Genera un nombre de usuario único para pruebas.
    
    Returns:
        str: Nombre de usuario único
    """
    return f"e2e_user_{uuid.uuid4().hex[:8]}"

def generate_unique_email(username: Optional[str] = None) -> str:
    """
    Genera un email único para pruebas.
    
    Args:
        username (str, optional): Nombre de usuario para usar en el email
        
    Returns:
        str: Email único
    """
    username = username or generate_unique_username()
    return f"{username}@example.com"

def generate_user_data() -> Dict[str, Any]:
    """
    Genera datos de usuario para pruebas.
    
    Returns:
        dict: Datos de usuario
    """
    username = generate_unique_username()
    return {
        "username": username,
        "email": generate_unique_email(username),
        "password": "Test@1234"
    }

def generate_address_data() -> Dict[str, Any]:
    """
    Genera datos de dirección para pruebas.
    
    Returns:
        dict: Datos de dirección
    """
    return {
        "street": f"Calle Prueba {random.randint(1, 1000)}",
        "number": str(random.randint(1, 999)),
        "city": random.choice(["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao"]),
        "state": random.choice(["Madrid", "Cataluña", "Valencia", "Andalucía", "País Vasco"]),
        "country": "España",
        "zipCode": f"{random.randint(10000, 99999)}"
    }

def generate_product_data() -> Dict[str, Any]:
    """
    Genera datos de producto para pruebas.
    
    Returns:
        dict: Datos de producto
    """
    product_name = f"Producto E2E {uuid.uuid4().hex[:8]}"
    return {
        "name": product_name,
        "description": f"Descripción de {product_name} para pruebas E2E",
        "price": round(random.uniform(10.0, 1000.0), 2),
        "stock": random.randint(1, 100),
        "categoryId": random.randint(1, 5)
    }

def generate_order_data(user_id: int) -> Dict[str, Any]:
    """
    Genera datos de orden para pruebas.
    
    Args:
        user_id (int): ID del usuario
        
    Returns:
        dict: Datos de orden
    """
    return {
        "userId": user_id,
        "totalAmount": round(random.uniform(50.0, 500.0), 2),
        "status": "PENDING"
    }

def generate_payment_data(order_id: int, amount: float) -> Dict[str, Any]:
    """
    Genera datos de pago para pruebas.
    
    Args:
        order_id (int): ID de la orden
        amount (float): Monto del pago
        
    Returns:
        dict: Datos de pago
    """
    payment_methods = ["CREDIT_CARD", "DEBIT_CARD", "PAYPAL", "TRANSFER"]
    
    return {
        "orderId": order_id,
        "method": random.choice(payment_methods),
        "amount": amount,
        "details": {
            "cardNumber": "4111111111111111",
            "expiryMonth": "12",
            "expiryYear": "2030",
            "cvv": "123"
        }
    }

def generate_shipping_data(order_id: int) -> Dict[str, Any]:
    """
    Genera datos de envío para pruebas.
    
    Args:
        order_id (int): ID de la orden
        
    Returns:
        dict: Datos de envío
    """
    shipping_methods = ["STANDARD", "EXPRESS", "PRIORITY"]
    
    return {
        "orderId": order_id,
        "method": random.choice(shipping_methods),
        "trackingNumber": f"TRACK-{uuid.uuid4().hex[:10].upper()}",
        "estimatedDelivery": (datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d")
    }
