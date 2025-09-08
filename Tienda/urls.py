from django.urls import path
from . import views

app_name = 'Tienda'

urlpatterns = [
    path("", views.index, name="index"),
    path("ventas/", views.ventas_list, name="ventas_list"),
    path("ventas/nueva/", views.venta_form, name="venta_form"),
    path("carrito/", views.carrito_view, name="carrito"),
    path("reportes/", views.reportes_view, name="reportes"),
    path("productos/", views.producto_list, name="producto_list"),
    path("productos/nuevo/", views.producto_create, name="producto_create"),
    path("productos/editar/<int:id>/", views.producto_edit, name="producto_edit"),
    path("productos/eliminar/<int:id>/", views.producto_delete, name="producto_delete"),
    path("ventas/editar/<int:id>/", views.venta_edit, name="venta_edit"),
    path("ventas/eliminar/<int:id>/", views.venta_delete, name="venta_delete"),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('gerente/', views.dashboard_gerente, name='dashboard_gerente'),
    path('jefe/', views.dashboard_jefe, name='dashboard_jefe'),
    path('empleado/', views.dashboard_empleado, name='dashboard_empleado'),
    
    # URLs para alertas
    path("alertas/", views.alertas_view, name="alertas"),
    path("alertas/desactivar/<int:alerta_id>/", views.alerta_desactivar, name="alerta_desactivar"),
    path("historial/", views.historial_list, name="historial_list"),
]