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
    path('duena/', views.dashboard_duena, name='dashboard_duena'), 

    # Empleados (solo Dueña)
    path("empleados/", views.empleados_list, name="empleados_list"),
    path("empleados/nuevo/", views.empleado_create, name="empleado_create"),
    path("empleados/editar/<int:id>/", views.empleado_edit, name="empleado_edit"),
    path("empleados/eliminar/<int:id>/", views.empleado_delete, name="empleado_delete"),
    
    # URLs para alertas
    path("alertas/", views.alertas_view, name="alertas"),
    path("alertas/desactivar/<int:alerta_id>/", views.alerta_desactivar, name="alerta_desactivar"),
    path("historial/", views.historial_list, name="historial_list"),


    #URls tablas Ricardo, Movimiento, credenciales, historial
    # CREDENCIALES
    path("credenciales/", views.credenciales_list, name="credenciales_list"),
    path("credenciales/nueva/", views.credencial_create, name="credencial_create"),
    path("credenciales/editar/<int:pk>/", views.credencial_edit, name="credencial_edit"),
    path("credenciales/eliminar/<int:pk>/", views.credencial_delete, name="credencial_delete"),

    # MOVIMIENTOS
    path("movimientos/", views.movimientos_list, name="movimientos_list"),
    path("movimientos/nuevo/", views.movimiento_create, name="movimiento_create"),
    path("movimientos/editar/<int:pk>/", views.movimiento_edit, name="movimiento_edit"),
    path("movimientos/eliminar/<int:pk>/", views.movimiento_delete, name="movimiento_delete"),

    # HISTORIAL
    path("historiales/", views.historial_list, name="historial_list"),
    path("historiales/nuevo/", views.historial_create, name="historial_create"),
    path("historiales/editar/<int:pk>/", views.historial_edit, name="historial_edit"),
    path("historiales/eliminar/<int:pk>/", views.historial_delete, name="historial_delete"),

    #urls tablas Soledad, Venta, Empleado, Tipo Empleado
    #Venta
    path("ventas-crud/", views.ventas_crud_list, name="ventas_crud_list"),
    path("ventas-crud/nueva/", views.venta_crud_create, name="venta_crud_create"),
    path("ventas-crud/editar/<int:pk>/", views.venta_crud_edit, name="venta_crud_edit"),
    path("ventas-crud/eliminar/<int:pk>/", views.venta_crud_delete, name="venta_crud_delete"),
    # path("empleado-crud/"), # Comentado para corregir TypeError

    #Empleado
    path("empleados/", views.empleados_list, name="empleados_list"),
    path("empleados/nuevo/", views.empleado_create, name="empleado_create"),
    path("empleados/editar/<int:pk>/", views.empleado_edit, name="empleado_edit"),
    path("empleados/eliminar/<int:pk>/", views.empleado_delete, name="empleado_delete"),

    #TipoEmpleado
    path("tipoempleados/", views.tipoempleado_list, name="tipoempleado_list"),
    path("tipoempleados/nuevo/", views.tipoempleado_create, name="tipoempleado_create"),
    path("tipoempleados/editar/<int:pk>/", views.tipoempleado_edit, name="tipoempleado_edit"),
    path("tipoempleados/eliminar/<int:pk>/", views.tipoempleado_delete, name="tipoempleado_delete"),

]