from django.contrib import admin
from .models import Credenciales, Movimiento, Historial, Venta, Empleado, TipoEmpleado, Alertas, DetalleVenta, Producto

# Register your models here.

@admin.register(Alertas)
class AlertasAdmin(admin.ModelAdmin):
    list_display = ("idalertas", "fecha", "estado")
    list_display_links = ("idalertas", "fecha")
    list_filter = ("estado",)
    search_fields = ("estado",)
    date_hierarchy = "fecha"

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("idproducto", "nombre", "precio", "stock_actual", "cantidad_minima")
    list_display_links = ("idproducto", "nombre")
    list_filter = ("stock_actual",)
    search_fields = ("nombre", "descripcion")

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ("iddetalleVenta", "cantidad_producto", "precio_unitario", "subtotal","producto", "venta")
    list_display_links = ("iddetalleVenta",)
    search_fields = ("producto__nombre", "venta__idventa")


# Tienda/admin.py hola chicos

@admin.register(Credenciales)
class CredencialesAdmin(admin.ModelAdmin):
    list_display = ("idcredenciales", "user")
    search_fields = ("user",)

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    # Form del admin: solo estos campos (no pide producto_idproducto)
    fields = ("descripcion", "fecha", "tipo")
    list_display = ("idmovimiento", "tipo", "fecha", "descripcion")
    list_display_links = ("idmovimiento", "tipo")
    list_filter  = ("tipo",)
    search_fields = ("descripcion",)
    date_hierarchy = "fecha"
    actions_on_top = True
    actions_on_bottom = True

@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    # Form del admin: solo fecha (no pide alertas_idalertas ni producto_idproducto)
    fields = ("fecha",)
    list_display = ("idhistorial", "fecha")
    list_display_links = ("idhistorial", "fecha") 
    date_hierarchy = "fecha"
    search_fields = ("idhistorial",)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    fields = ("fecha", "total", "empleado")  #se oculto empleado_idempleado
    list_display = ("idventa", "fecha", "total", "empleado")
    date_hierarchy = "fecha"

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    fields = ("nombre", "apellido", "email") #sin ids
    list_display = ("idempleado", "nombre", "apellido", "email",
                    "credenciales", "tipoEmpleado")
    search_fields = ("nombre", "apellido", "email", "credenciales__user", "tipoEmpleado__rol")

@admin.register(TipoEmpleado)
class TipoEmpleadoAdmin(admin.ModelAdmin):
    fields = ("rol",)  #Solo muestra el rol
    list_display = ("idtipoEmpleado", "rol")
    search_fields = ("rol",)

