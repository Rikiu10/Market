# -*- coding: utf-8 -*-
"""
Archivo de datos locales para el sistema de gestión de productos
Simula una base de datos usando estructuras de datos en memoria
"""

from datetime import datetime

# Datos de productos (simulando una tabla de productos)
# Estructura: {'id': int, 'nombre': str, 'precio': float, 'stock': int, 'cantidad_minima': int}
productos = [
    {
        'id': 1,
        'nombre': 'Arroz',
        'precio': 1500,
        'stock': 20,
        'cantidad_minima': 15
    },
    {
        'id': 2,
        'nombre': 'Aceite',
        'precio': 5000,
        'stock': 8,
        'cantidad_minima': 10
    }
]

# Datos de alertas (simulando una tabla de alertas)
# Estructura: {'id': int, 'producto_id': int, 'mensaje': str, 'fecha_creacion': datetime, 'activa': bool}
alertas = [
    {
        'id': 1,
        'producto_id': 2,
        'mensaje': 'Stock bajo: Aceite (8 unidades, mínimo 10)',
        'fecha_creacion': datetime(2024, 1, 15, 10, 30),
        'activa': True
    }
]

# Historial de alertas (simulando una tabla de historial)
# Estructura: {'id': int, 'producto_id': int, 'mensaje': str, 'fecha_creacion': datetime}
historial_alertas = [
    {
        'id': 1,
        'producto_id': 2,
        'mensaje': 'Stock bajo: Aceite (8 unidades, mínimo 10)',
        'fecha_creacion': datetime(2024, 1, 15, 10, 30)
    },
    {
        'id': 2,
        'producto_id': 2,
        'mensaje': 'Stock bajo: Aceite (5 unidades, mínimo 10)',
        'fecha_creacion': datetime(2024, 1, 10, 16, 20)
    }
]

# Contadores para generar IDs únicos
next_producto_id = 3
next_alerta_id = 2
next_historial_id = 3

def get_next_producto_id():
    """Obtiene el siguiente ID disponible para productos"""
    global next_producto_id
    current_id = next_producto_id
    next_producto_id += 1
    return current_id

def get_next_alerta_id():
    """Obtiene el siguiente ID disponible para alertas"""
    global next_alerta_id
    current_id = next_alerta_id
    next_alerta_id += 1
    return current_id

def get_next_historial_id():
    """Obtiene el siguiente ID disponible para historial"""
    global next_historial_id
    current_id = next_historial_id
    next_historial_id += 1
    return current_id

