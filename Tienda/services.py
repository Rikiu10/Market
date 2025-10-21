# -*- coding: utf-8 -*-
"""
Servicios para manejar la lógica de negocio.
- ProductoService -> usa BD (ORM) con el modelo Producto
- AlertaService / HistorialService -> siguen en memoria (data.py), sin FK
"""
from datetime import datetime
from .models import Producto

from .data import alertas, historial_alertas
from .data import get_next_alerta_id, get_next_historial_id


# --------------------- ALERTAS EN MEMORIA --------------------- #
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


# --------------------- PRODUCTOS CON ORM ---------------------- #
class ProductoService:
    """
    Ahora usa el modelo Producto (BD). Devuelve dicts compatibles con tus
    vistas/templates anteriores (incluye clave 'stock').
    """

    @staticmethod
    def _to_dict(obj: Producto):
        return {
            "id": obj.pk,                     
            "idproducto": obj.idproducto,     
            "nombre": obj.nombre,
            "descripcion": obj.descripcion,
            "precio": obj.precio,
            "stock": obj.stock_actual,       
            "cantidad_minima": obj.cantidad_minima,
        }

    @staticmethod
    def obtener_todos():
        qs = Producto.objects.all().order_by('idproducto')
        return [ProductoService._to_dict(p) for p in qs]

    @staticmethod
    def obtener_por_id(producto_id):
        try:
            p = Producto.objects.get(pk=producto_id)
        except Producto.DoesNotExist:
            return None
        return ProductoService._to_dict(p)

    @staticmethod
    def crear(nombre, precio, stock, cantidad_minima, descripcion=""):
        p = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion or "",
            precio=int(precio),
            stock_actual=int(stock),
            cantidad_minima=int(cantidad_minima),
        )
        prod_dict = ProductoService._to_dict(p)

        try:
            AlertaService.verificar_y_crear_alerta(prod_dict)
        except Exception:
            pass

        return prod_dict

    @staticmethod
    def actualizar(producto_id, nombre, precio, stock, cantidad_minima, descripcion=None):
        p = Producto.objects.get(pk=producto_id)  
        p.nombre = nombre
        if descripcion is not None:
            p.descripcion = descripcion
        p.precio = int(precio)
        p.stock_actual = int(stock)
        p.cantidad_minima = int(cantidad_minima)
        p.save()

        prod_dict = ProductoService._to_dict(p)
        try:
            AlertaService.verificar_y_crear_alerta(prod_dict)
        except Exception:
            pass

        return prod_dict

    @staticmethod
    def eliminar(producto_id):
        try:
            AlertaService.eliminar_por_producto(producto_id)
        except Exception:
            pass
        Producto.objects.filter(pk=producto_id).delete()
