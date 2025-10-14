from django.contrib import admin
from .models import Credenciales, Movimiento, Historial, Venta

# Register your models here.

# Tienda/admin.py hola chicos

@admin.register(Credenciales)
class CredencialesAdmin(admin.ModelAdmin):
    list_display = ("idcredenciales", "user")
    search_fields = ("user",)
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
    fields = ("fecha", "total")  #se oculto empleado_idempleado
    list_display = ("idventa", "fecha", "total", "empleado_idempleado")
    date_hierarchy = "fecha"