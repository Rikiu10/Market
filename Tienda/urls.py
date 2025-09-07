from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('empleados/', views.empleados_list, name='empleados_list'),
    path('empleados/nuevo/', views.empleado_create, name='empleado_create'),
    path('empleados/<int:id>/editar/', views.empleado_update, name='empleado_update'),
    path('empleados/<int:id>/eliminar/', views.empleado_delete, name='empleado_delete'),
    path('login/', views.login_view, name='login'),
    path('movimientos/', views.movimientos_list, name='movimientos_list'),
    path('movimientos/nuevo/', views.movimiento_create, name='movimiento_create'),
    path('movimientos/<int:id>/editar/', views.movimiento_update, name='movimiento_update'),
    path('movimientos/<int:id>/eliminar/', views.movimiento_delete, name='movimiento_delete'),
    path('productos/', views.productos_list, name='productos_list'),
    path('alertas/', views.alertas_list, name='alertas_list'),
    path('ventas/', views.ventas_list, name='ventas_list'),
]
