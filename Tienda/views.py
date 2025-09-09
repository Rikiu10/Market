from django.shortcuts import render, redirect
from datetime import date
from django.http import HttpResponseForbidden, Http404
from functools import wraps
from django.contrib import messages
from .services import ProductoService, AlertaService, HistorialService

# Create your views here.
# ====== AUTENTICACIÓN "TEMPORAL" SIN BD ======
USERS = {
    'gerente1': ('1234', 'GERENTE'),
    'jefe1':    ('1234', 'JEFE'),
    'emple1':   ('1234', 'EMPLEADO'),
}

# ====== DATOS EN MEMORIA ======
ventas = [
    {"id": 1, "fecha": "2025-09-01", "total": 15000},
    {"id": 2, "fecha": "2025-09-02", "total": 25000},
]

carrito = [
    {"nombre": "Arroz", "cantidad": 2, "precio": 1500, "subtotal": 3000},
    {"nombre": "Aceite", "cantidad": 1, "precio": 5000, "subtotal": 5000},
]

# ====== HELPERS ======
def redirect_by_role(request):
    role = request.session.get('role')
    if role == 'GERENTE':
        return redirect('Tienda:dashboard_gerente')
    if role == 'JEFE':
        return redirect('Tienda:dashboard_jefe')
    if role == 'EMPLEADO':
        return redirect('Tienda:dashboard_empleado')
    return redirect('Tienda:login')

def require_role(*roles):
    """Protege vistas según rol almacenado en sesión."""
    def decorator(view_func):
        @wraps(view_func)
        def _wrap(request, *args, **kwargs):
            role = request.session.get('role')
            if not role:
                return redirect('Tienda:login')
            if roles and role not in roles:
                return HttpResponseForbidden("No tienes permisos para esta vista.")
            return view_func(request, *args, **kwargs)
        return _wrap
    return decorator

# ====== INDEX = LOGIN ======
def index(request):
    # Si ya está logueado, manda al dashboard
    if request.session.get('role'):
        return redirect_by_role(request)

    context = {'error': None}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = USERS.get(username)
        if user and user[0] == password:
            request.session['username'] = username
            request.session['role'] = user[1]
            return redirect_by_role(request)
        context['error'] = 'Usuario o contraseña incorrectos.'

    # ⬇️ RUTA EXACTA DE TU TEMPLATE
    return render(request, "Tienda/index.html", context)

# (opcional) login_view si quieres /login además de /
def login_view(request):
    if request.session.get('role'):
        return redirect_by_role(request)
    context = {'error': None}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = USERS.get(username)
        if user and user[0] == password:
            request.session['username'] = username
            request.session['role'] = user[1]
            return redirect_by_role(request)
        context['error'] = 'Usuario o contraseña incorrectos.'
    # OJO: si tu login.html vive en subcarpeta, ajusta la ruta
    return render(request, 'Tienda/index.html', context)

def logout_view(request):
    request.session.flush()
    return redirect('Tienda:login')

# ====== DASHBOARDS ======
@require_role('GERENTE')
def dashboard_gerente(request):
    return render(request, 'Tienda/dashboard.html', {'titulo': 'Panel Gerente'})

@require_role('JEFE')
def dashboard_jefe(request):
    return render(request, 'Tienda/dashboard.html', {'titulo': 'Panel Jefe'})

@require_role('EMPLEADO')
def dashboard_empleado(request):
    return render(request, 'Tienda/dashboard.html', {'titulo': 'Panel Empleado'})

# ====== VISTAS DE NEGOCIO (CON PERMISOS) ======
@require_role('GERENTE','JEFE')
def ventas_list(request):
    return render(request, "Tienda/ventas/ventas_list.html", {"ventas": ventas})

@require_role('GERENTE','JEFE')
def venta_form(request):
    if request.method == "POST":
        nueva_venta = {
            "id": len(ventas) + 1,
            "fecha": request.POST.get("fecha"),
            "total": request.POST.get("total"),
        }
        ventas.append(nueva_venta)
        return redirect("Tienda:ventas_list")
    return render(request, "Tienda/ventas/venta_form.html")

@require_role('EMPLEADO','JEFE','GERENTE')
def carrito_view(request):
    total = sum(i['subtotal'] for i in carrito)
    return render(request, "Tienda/ventas/carrito.html", {"carrito": carrito})

@require_role('GERENTE', 'JEFE')
def reportes_view(request):
    reportes = {
        "diarias": 5,
        "semanales": 20,
        "mensuales": 80,
        "top_producto": "Arroz",
    }
    return render(request, "Tienda/ventas/reportes.html", {"reportes": reportes})

# ====== VISTAS DE PRODUCTOS INTEGRADAS ======
@require_role('JEFE','GERENTE')
def producto_list(request):
    """Vista para listar todos los productos usando el servicio"""
    productos = ProductoService.obtener_todos()
    return render(request, "Tienda/productos/productos_list.html", {"productos": productos})

@require_role('JEFE','GERENTE')
def producto_create(request):
    """Vista para crear un nuevo producto"""
    if request.method == "POST":
        nombre = request.POST.get('nombre', '').strip()
        precio = request.POST.get('precio', '')
        stock = request.POST.get('stock', '')
        cantidad_minima = request.POST.get('cantidad_minima', '')
        
        # Validaciones básicas
        if not nombre:
            messages.error(request, 'El nombre del producto es obligatorio')
        elif not precio or float(precio) <= 0:
            messages.error(request, 'El precio debe ser mayor a 0')
        elif not stock or int(stock) < 0:
            messages.error(request, 'El stock no puede ser negativo')
        elif not cantidad_minima or int(cantidad_minima) < 0:
            messages.error(request, 'La cantidad mínima no puede ser negativa')
        else:
            try:
                ProductoService.crear(nombre, precio, stock, cantidad_minima)
                messages.success(request, f'Producto "{nombre}" creado correctamente')
                return redirect("Tienda:producto_list")
            except ValueError as e:
                messages.error(request, 'Error en los datos ingresados. Verifique los valores numéricos.')
            except Exception as e:
                messages.error(request, f'Error al guardar el producto: {str(e)}')
    
    return render(request, "Tienda/productos/producto_form.html")

@require_role('JEFE','GERENTE')
def producto_edit(request, id):
    """Vista para editar un producto existente"""
    producto = ProductoService.obtener_por_id(id)
    if not producto:
        raise Http404("Producto no encontrado")
    
    if request.method == "POST":
        nombre = request.POST.get('nombre', '').strip()
        precio = request.POST.get('precio', '')
        stock = request.POST.get('stock', '')
        cantidad_minima = request.POST.get('cantidad_minima', '')
        
        # Validaciones básicas
        if not nombre:
            messages.error(request, 'El nombre del producto es obligatorio')
        elif not precio or float(precio) <= 0:
            messages.error(request, 'El precio debe ser mayor a 0')
        elif not stock or int(stock) < 0:
            messages.error(request, 'El stock no puede ser negativo')
        elif not cantidad_minima or int(cantidad_minima) < 0:
            messages.error(request, 'La cantidad mínima no puede ser negativa')
        else:
            try:
                ProductoService.actualizar(id, nombre, precio, stock, cantidad_minima)
                messages.success(request, f'Producto "{nombre}" actualizado correctamente')
                return redirect("Tienda:producto_list")
            except ValueError as e:
                messages.error(request, 'Error en los datos ingresados. Verifique los valores numéricos.')
            except Exception as e:
                messages.error(request, f'Error al guardar el producto: {str(e)}')
    
    return render(request, "Tienda/productos/producto_form.html", {"producto": producto})

@require_role('JEFE','GERENTE')
def producto_delete(request, id):
    """Vista para eliminar un producto"""
    producto = ProductoService.obtener_por_id(id)
    if not producto:
        raise Http404("Producto no encontrado")
    
    if request.method == "POST":
        nombre_producto = producto['nombre']
        ProductoService.eliminar(id)
        messages.success(request, f'Producto "{nombre_producto}" eliminado correctamente')
        return redirect("Tienda:producto_list")
    
    return render(request, "Tienda/productos/producto_confirmar_eliminar.html", {"producto": producto})

@require_role('GERENTE','JEFE')
def venta_edit(request, id):
    venta = next((v for v in ventas if v["id"] == id), None)
    if not venta:
        return redirect("Tienda:ventas_list")
    if request.method == "POST":
        venta["fecha"] = request.POST.get("fecha")
        venta["total"] = request.POST.get("total")
        return redirect("Tienda:ventas_list")
    return render(request, "Tienda/ventas/venta_form.html", {"venta": venta})

@require_role('GERENTE','JEFE')
def venta_delete(request, id):
    global ventas
    ventas = [v for v in ventas if v["id"] != id]
    return redirect("Tienda:ventas_list")

# ====== VISTAS DE ALERTAS INTEGRADAS ======
@require_role('GERENTE', 'JEFE')
def alertas_view(request):
    """Vista para listar todas las alertas activas"""
    alertas = AlertaService.obtener_todas()
    
    # Enriquecer alertas con información del producto
    alertas_enriquecidas = []
    for alerta in alertas:
        producto = ProductoService.obtener_por_id(alerta['producto_id'])
        alerta_enriquecida = alerta.copy()
        alerta_enriquecida['producto'] = producto
        alertas_enriquecidas.append(alerta_enriquecida)
    
    return render(request, "Tienda/alertas/alertas_list.html", {"alertas": alertas_enriquecidas})

@require_role('GERENTE', 'JEFE')
def alerta_desactivar(request, alerta_id):
    """Vista para desactivar una alerta"""
    alerta = AlertaService.obtener_por_id(alerta_id)
    if not alerta:
        raise Http404("Alerta no encontrada")
    
    if request.method == 'POST':
        AlertaService.desactivar_alerta(alerta_id)
        messages.success(request, 'Alerta desactivada correctamente')
        return redirect('Tienda:alertas')
    
    return render(request, 'Tienda/alertas/alerta_confirmar_desactivar.html', {'alerta': alerta})

@require_role('GERENTE', 'JEFE')
def historial_list(request):
    """Vista para mostrar el historial de alertas"""
    historial = HistorialService.obtener_todo()
    
    # Enriquecer historial con información del producto
    historial_enriquecido = []
    for entrada in historial:
        producto = ProductoService.obtener_por_id(entrada['producto_id'])
        entrada_enriquecida = entrada.copy()
        entrada_enriquecida['producto'] = producto
        historial_enriquecido.append(entrada_enriquecida)
    
    return render(request, 'Tienda/alertas/historial_list.html', {'historial': historial_enriquecido})