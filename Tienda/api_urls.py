from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    CredencialesViewSet, TipoEmpleadoViewSet, EmpleadoViewSet, 
    AlertasViewSet, ProductoViewSet, VentaViewSet, 
    MovimientoViewSet, HistorialViewSet, DetalleVentaViewSet
)

# Crear un router y registrar nuestros viewsets
router = DefaultRouter()
router.register(r'credenciales', CredencialesViewSet)
router.register(r'tipo-empleado', TipoEmpleadoViewSet)
router.register(r'empleados', EmpleadoViewSet)
router.register(r'alertas', AlertasViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'detalle-ventas', DetalleVentaViewSet)
router.register(r'movimientos', MovimientoViewSet)
router.register(r'historial', HistorialViewSet)

# Las URLs de la API se determinan automáticamente por el router.
urlpatterns = [
    path('', include(router.urls)),
]
