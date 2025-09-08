# -*- coding: utf-8 -*-
"""
Servicios para manejar la lógica de negocio del sistema de gestión de productos
Incluye CRUD de productos, gestión de alertas e historial
"""

from datetime import datetime
from .data import productos, alertas, historial_alertas
from .data import get_next_producto_id, get_next_alerta_id, get_next_historial_id

class ProductoService:
    """Servicio para manejar operaciones CRUD de productos"""
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los productos"""
        return productos
    
    @staticmethod
    def obtener_por_id(producto_id):
        """Obtiene un producto por su ID"""
        for producto in productos:
            if producto['id'] == producto_id:
                return producto
        return None
    
    @staticmethod
    def crear(nombre, precio, stock, cantidad_minima):
        """Crea un nuevo producto"""
        nuevo_producto = {
            'id': get_next_producto_id(),
            'nombre': nombre,
            'precio': float(precio),
            'stock': int(stock),
            'cantidad_minima': int(cantidad_minima)
        }
        productos.append(nuevo_producto)
        
        # Verificar si necesita crear alerta
        AlertaService.verificar_y_crear_alerta(nuevo_producto)
        
        return nuevo_producto
    
    @staticmethod
    def actualizar(producto_id, nombre, precio, stock, cantidad_minima):
        """Actualiza un producto existente"""
        producto = ProductoService.obtener_por_id(producto_id)
        if producto:
            producto['nombre'] = nombre
            producto['precio'] = float(precio)
            producto['stock'] = int(stock)
            producto['cantidad_minima'] = int(cantidad_minima)
            
            # Verificar si necesita crear alerta después de la actualización
            AlertaService.verificar_y_crear_alerta(producto)
            
            return producto
        return None
    
    @staticmethod
    def eliminar(producto_id):
        """Elimina un producto"""
        global productos
        productos = [p for p in productos if p['id'] != producto_id]
        
        # Eliminar alertas relacionadas
        AlertaService.eliminar_por_producto(producto_id)

class AlertaService:
    """Servicio para manejar operaciones de alertas"""
    
    @staticmethod
    def obtener_todas():
        """Obtiene todas las alertas activas"""
        return [alerta for alerta in alertas if alerta['activa']]
    
    @staticmethod
    def obtener_por_id(alerta_id):
        """Obtiene una alerta por su ID"""
        for alerta in alertas:
            if alerta['id'] == alerta_id:
                return alerta
        return None
    
    @staticmethod
    def verificar_y_crear_alerta(producto):
        """Verifica si un producto necesita alerta y la crea si es necesario"""
        if producto['stock'] < producto['cantidad_minima']:
            # Verificar si ya existe una alerta activa para este producto
            alerta_existente = False
            for alerta in alertas:
                if alerta['producto_id'] == producto['id'] and alerta['activa']:
                    alerta_existente = True
                    break
            
            if not alerta_existente:
                AlertaService.crear_alerta(producto)
    
    @staticmethod
    def crear_alerta(producto):
        """Crea una nueva alerta para un producto"""
        mensaje = f"Stock bajo: {producto['nombre']} ({producto['stock']} unidades, mínimo {producto['cantidad_minima']})"
        
        nueva_alerta = {
            'id': get_next_alerta_id(),
            'producto_id': producto['id'],
            'mensaje': mensaje,
            'fecha_creacion': datetime.now(),
            'activa': True
        }
        
        alertas.append(nueva_alerta)
        
        # Agregar automáticamente al historial
        HistorialService.agregar_al_historial(nueva_alerta)
        
        return nueva_alerta
    
    @staticmethod
    def desactivar_alerta(alerta_id):
        """Desactiva una alerta"""
        alerta = AlertaService.obtener_por_id(alerta_id)
        if alerta:
            alerta['activa'] = False
            return alerta
        return None
    
    @staticmethod
    def eliminar_por_producto(producto_id):
        """Elimina todas las alertas de un producto"""
        global alertas
        alertas = [a for a in alertas if a['producto_id'] != producto_id]

class HistorialService:
    """Servicio para manejar el historial de alertas"""
    
    @staticmethod
    def obtener_todo():
        """Obtiene todo el historial de alertas ordenado por fecha (más reciente primero)"""
        return sorted(historial_alertas, key=lambda x: x['fecha_creacion'], reverse=True)
    
    @staticmethod
    def agregar_al_historial(alerta):
        """Agrega una alerta al historial automáticamente"""
        entrada_historial = {
            'id': get_next_historial_id(),
            'producto_id': alerta['producto_id'],
            'mensaje': alerta['mensaje'],
            'fecha_creacion': alerta['fecha_creacion']
        }
        
        historial_alertas.append(entrada_historial)
        return entrada_historial
    
    @staticmethod
    def obtener_por_producto(producto_id):
        """Obtiene el historial de alertas de un producto específico"""
        return [h for h in historial_alertas if h['producto_id'] == producto_id]

