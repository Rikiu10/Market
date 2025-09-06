from django.shortcuts import render, redirect
from datetime import date
from django.http import HttpResponseForbidden
from functools import wraps

# ====== AUTENTICACIÓN “TEMPORAL” SIN BD ======
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

productos = [   # <-- FALTABA
    {"id": 1, "nombre": "Arroz",  "precio": 1500, "stock": 20},
    {"id": 2, "nombre": "Aceite", "precio": 5000, "stock": 8},
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
    return render(request, "Tienda/empleados/login.html", context)

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
    return render(request, 'Tienda/empleados/login.html', context)

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

@require_role('GERENTE')
def reportes_view(request):
    reportes = {
        "diarias": 5,
        "semanales": 20,
        "mensuales": 80,
        "top_producto": "Arroz",
    }
    return render(request, "Tienda/ventas/reportes.html", {"reportes": reportes})

@require_role('JEFE','GERENTE')
def producto_list(request):
    return render(request, "Tienda/productos/producto_list.html", {"productos": productos})

@require_role('JEFE','GERENTE')
def producto_create(request):
    if request.method == "POST":
        nuevo = {
            "id": len(productos) + 1,
            "nombre": request.POST.get("nombre"),
            "precio": int(request.POST.get("precio")),
            "stock": int(request.POST.get("stock")),
        }
        productos.append(nuevo)
        return redirect("Tienda:producto_list")
    return render(request, "Tienda/productos/producto_form.html")

@require_role('JEFE','GERENTE')
def producto_edit(request, id):
    producto = next((p for p in productos if p["id"] == id), None)
    if not producto:
        return redirect("Tienda:producto_list")
    if request.method == "POST":
        producto["nombre"] = request.POST.get("nombre")
        producto["precio"] = int(request.POST.get("precio"))
        producto["stock"] = int(request.POST.get("stock"))
        return redirect("Tienda:producto_list")
    return render(request, "Tienda/productos/producto_form.html", {"producto": producto})

@require_role('JEFE','GERENTE')
def producto_delete(request, id):
    global productos
    productos = [p for p in productos if p["id"] != id]
    return redirect("Tienda:producto_list")

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
