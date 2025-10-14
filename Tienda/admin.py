from django.contrib import admin
from .models import Credenciales, Movimiento, Historial

# Register your models here.

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
    list_filter  = ("tipo",)
    search_fields = ("descripcion",)
    date_hierarchy = "fecha"

@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    # Form del admin: solo fecha (no pide alertas_idalertas ni producto_idproducto)
    fields = ("fecha",)
    list_display = ("idhistorial", "fecha")
    date_hierarchy = "fecha"
    search_fields = ("idhistorial",)