from rest_framework import viewsets
from .models import (
    Credenciales, TipoEmpleado, Empleado, Alertas, 
    Producto, Venta, Movimiento, Historial, DetalleVenta
)
from .serializers import (
    CredencialesSerializer, TipoEmpleadoSerializer, EmpleadoSerializer, 
    AlertasSerializer, ProductoSerializer, VentaSerializer, 
    MovimientoSerializer, HistorialSerializer, DetalleVentaSerializer
)

class CredencialesViewSet(viewsets.ModelViewSet):
    """
    API para gestionar Credenciales de usuarios.
    """
    queryset = Credenciales.objects.all()
    serializer_class = CredencialesSerializer

class TipoEmpleadoViewSet(viewsets.ModelViewSet):
    """
    API para gestionar Tipos de Empleado (Roles).
    """
    queryset = TipoEmpleado.objects.all()
    serializer_class = TipoEmpleadoSerializer

class EmpleadoViewSet(viewsets.ModelViewSet):
    """
    API para gestionar Empleados.
    """
    queryset = Empleado.objects.all()
    serializer_class = EmpleadoSerializer

class AlertasViewSet(viewsets.ModelViewSet):
    """
    API para gestionar Alertas de stock.
    """
    queryset = Alertas.objects.all()
    serializer_class = AlertasSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    """
    API para gestionar Productos (Inventario).
    """
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class VentaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar Ventas.
    """
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class DetalleVentaViewSet(viewsets.ModelViewSet):
    """
    API para gestionar los detalles de cada venta.
    """
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

class MovimientoViewSet(viewsets.ModelViewSet):
    """
    API para gestionar Movimientos de stock (entradas/salidas).
    """
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

class HistorialViewSet(viewsets.ModelViewSet):
    """
    API para el Historial de cambios.
    """
    queryset = Historial.objects.all()
    serializer_class = HistorialSerializer
