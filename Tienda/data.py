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


# --------------------- ALERTAS EN MEMORIA (MOVIDO DE services.py) --------------------- #
class HistorialService:
    """Servicio para manejar el historial de alertas EN MEMORIA"""

    @staticmethod
    def obtener_todo():
        """Historial ordenado (más reciente primero)"""
        return sorted(historial_alertas, key=lambda x: x['fecha_creacion'], reverse=True)

    @staticmethod
    def agregar_al_historial(alerta):
        entrada = {
            'id': get_next_historial_id(),
            'producto_id': alerta['producto_id'],
            'mensaje': alerta['mensaje'],
            'fecha_creacion': alerta['fecha_creacion']
        }
        historial_alertas.append(entrada)
        return entrada

    @staticmethod
    def obtener_por_producto(producto_id):
        return [h for h in historial_alertas if h['producto_id'] == producto_id]


class AlertaService:
    """Servicio para manejar operaciones de alertas EN MEMORIA"""

    @staticmethod
    def obtener_todas():
        """Obtiene todas las alertas activas"""
        return [a for a in alertas if a['activa']]

    @staticmethod
    def obtener_por_id(alerta_id):
        for a in alertas:
            if a['id'] == alerta_id:
                return a
        return None

    @staticmethod
    def verificar_y_crear_alerta(producto_dict):
        """
        Recibe un dict de producto (id, nombre, stock, cantidad_minima).
        Crea alerta si 'stock' < 'cantidad_minima' y no existe una activa para ese producto.
        """
        if producto_dict['stock'] < producto_dict['cantidad_minima']:
            existe = any(a for a in alertas if a['producto_id'] == producto_dict['id'] and a['activa'])
            if not existe:
                AlertaService.crear_alerta(producto_dict)

    @staticmethod
    def crear_alerta(producto_dict):
        """Crea una nueva alerta y la agrega al historial (ambos en memoria)"""
        mensaje = f"Stock bajo: {producto_dict['nombre']} ({producto_dict['stock']} unidades, mínimo {producto_dict['cantidad_minima']})"
        nueva = {
            'id': get_next_alerta_id(),
            'producto_id': producto_dict['id'],
            'mensaje': mensaje,
            'fecha_creacion': datetime.now(),
            'activa': True
        }
        alertas.append(nueva)
        HistorialService.agregar_al_historial(nueva)
        return nueva

    @staticmethod
    def desactivar_alerta(alerta_id):
        alerta = AlertaService.obtener_por_id(alerta_id)
        if alerta:
            alerta['activa'] = False
            return alerta
        return None

    @staticmethod
    def eliminar_por_producto(producto_id):
        """Elimina TODAS las alertas (en memoria) asociadas a un producto"""
        global alertas
        alertas = [a for a in alertas if a['producto_id'] != producto_id]
