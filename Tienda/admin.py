from django.contrib import admin

# Register your models here.

# Tienda/admin.py
from django.contrib import admin
from .models import Credenciales, Movimiento, Historial

@admin.register(Credenciales)
class CredencialesAdmin(admin.ModelAdmin):
    list_display = ("idcredenciales", "user")
    search_fields = ("user",)

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ("idmovimiento", "tipo", "fecha", "producto_idproducto", "descripcion")
    list_filter  = ("tipo",)
    search_fields = ("descripcion",)
    date_hierarchy = "fecha"

@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ("idhistorial", "fecha", "alertas_idalertas", "producto_idproducto")
    date_hierarchy = "fecha"
    search_fields = ("idhistorial",)
