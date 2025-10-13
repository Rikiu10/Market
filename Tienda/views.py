from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from django.http import HttpResponseForbidden, Http404
from functools import wraps
from django.contrib import messages
from .services import ProductoService, AlertaService, HistorialService

#tablas ricardo
from django.contrib import messages
from .models import Credenciales, Movimiento, Historial
from .forms import CredencialesForm, MovimientoForm, HistorialForm
#tablas ricardo



# Create your views here.
# ====== AUTENTICACIÓN "TEMPORAL" SIN BD ======
USERS = {
    'gerente1': ('1234', 'GERENTE'),
    'jefe1':    ('1234', 'JEFE'),
    'emple1':   ('1234', 'EMPLEADO'),
    'duena1':   ('1234', 'DUEÑA'), 
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

#empleados en memoria (puedes partir vacío)
empleados = [
    {"id": 1, "nombre": "Ana Torres", "rut": "12.345.678-9", "cargo": "Cajera", "email": "ana@market.cl", "telefono": "+56911111111"},
    {"id": 2, "nombre": "Pedro Soto", "rut": "9.876.543-2", "cargo": "Reponedor", "email": "pedro@market.cl", "telefono": "+56922222222"},
    {"id": 3, "nombre": "Juan Gonzalez", "rut": "9.831.413-2", "cargo": "Reponedor", "email": "juanito@market.cl", "telefono": "+56922324232"}
]

# Roles permitidos para cuentas creadas por la Dueña
ROL_CHOICES = ['GERENTE', 'JEFE', 'EMPLEADO']

def username_in_use(username, exclude_id=None):
    """Valida unicidad de username contra USERS fijos y empleados."""
    if username in USERS:
        return True
    for e in empleados:
        if e.get('username') == username and (exclude_id is None or e['id'] != exclude_id):
            return True
    return False

def get_account(username):
    """
    Devuelve (password, role) para login.
    Primero busca en USERS fijos; si no, en empleados creados por Dueña.
    """
    if username in USERS:
        return USERS[username]
    for e in empleados:
        if e.get('username') == username:
            return (e.get('password'), e.get('rol'))
    return None


# ====== HELPERS ======
def redirect_by_role(request):
    role = request.session.get('role')
    if role == 'GERENTE':
        return redirect('Tienda:dashboard_gerente')
    if role == 'JEFE':
        return redirect('Tienda:dashboard_jefe')
    if role == 'EMPLEADO':
        return redirect('Tienda:dashboard_empleado')
    if role == 'DUEÑA':                                  
        return redirect('Tienda:dashboard_duena')
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
        user = get_account(username) 
        if user and user[0] == password:
            request.session['username'] = username
            request.session['role'] = user[1]
            return redirect_by_role(request)
        context['error'] = 'Usuario o contraseña incorrectos.'

    return render(request, "Tienda/index.html", context)

# (opcional) login_view si quieres /login además de /
def login_view(request):
    if request.session.get('role'):
        return redirect_by_role(request)
    context = {'error': None}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = get_account(username) 
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

@require_role('DUEÑA')                                  
def dashboard_duena(request):
    return render(request, 'Tienda/dashboard.html', {'titulo': 'Panel Dueña'})

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

# ====== CRUD EMPLEADOS (solo DUEÑA) ============================
@require_role('DUEÑA')
def empleados_list(request):
    return render(request, "Tienda/empleados/empleados_list.html", {"empleados": empleados})

@require_role('DUEÑA')
def empleado_create(request):
    if request.method == "POST":
        nombre   = request.POST.get('nombre', '').strip()
        rut      = request.POST.get('rut', '').strip()
        cargo    = request.POST.get('cargo', '').strip()
        email    = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()

        username = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password', '').strip()
        rol      = request.POST.get('rol', '').strip().upper()

        # Validaciones
        if not nombre or not rut:
            messages.error(request, "Nombre y RUT son obligatorios.")
        elif not username:
            messages.error(request, "Debes definir un nombre de usuario.")
        elif username_in_use(username):
            messages.error(request, "Ese nombre de usuario ya está en uso.")
        elif not password or len(password) < 4:
            messages.error(request, "La contraseña debe tener al menos 4 caracteres.")
        elif rol not in ROL_CHOICES:
            messages.error(request, "Rol inválido. Debe ser GERENTE, JEFE o EMPLEADO.")
        else:
            nuevo = {
                "id": (empleados[-1]["id"] + 1) if empleados else 1,
                "nombre": nombre, "rut": rut, "cargo": cargo,
                "email": email, "telefono": telefono,
                "username": username, "password": password, "rol": rol,
            }
            empleados.append(nuevo)
            messages.success(request, f'Empleado "{nombre}" creado correctamente.')
            return redirect("Tienda:empleados_list")

        # Si hay errores, re-render con lo ingresado
        data = {
            "nombre": nombre, "rut": rut, "cargo": cargo,
            "email": email, "telefono": telefono,
            "username": username, "rol": rol
        }
        return render(request, "Tienda/empleados/empleado_form.html", {"empleado": data})

    return render(request, "Tienda/empleados/empleado_form.html")


@require_role('DUEÑA')
def empleado_edit(request, id):
    emp = next((e for e in empleados if e["id"] == id), None)
    if not emp:
        raise Http404("Empleado no encontrado")

    if request.method == "POST":
        nombre   = request.POST.get('nombre', '').strip()
        rut      = request.POST.get('rut', '').strip()
        cargo    = request.POST.get('cargo', '').strip()
        email    = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()

        username = request.POST.get('username', '').strip().lower()
        password = request.POST.get('password', '').strip()  # opcional: permitir vacío para no cambiar
        rol      = request.POST.get('rol', '').strip().upper()

        # Validaciones
        if not nombre or not rut:
            messages.error(request, "Nombre y RUT son obligatorios.")
        elif not username:
            messages.error(request, "Debes definir un nombre de usuario.")
        elif username_in_use(username, exclude_id=id):
            messages.error(request, "Ese nombre de usuario ya está en uso.")
        elif rol not in ROL_CHOICES:
            messages.error(request, "Rol inválido. Debe ser GERENTE, JEFE o EMPLEADO.")
        else:
            emp["nombre"] = nombre
            emp["rut"] = rut
            emp["cargo"] = cargo
            emp["email"] = email
            emp["telefono"] = telefono
            emp["username"] = username
            emp["rol"] = rol
            if password:  # solo cambia si ingresó algo
                if len(password) < 4:
                    messages.error(request, "La contraseña debe tener al menos 4 caracteres.")
                    return render(request, "Tienda/empleados/empleado_form.html", {"empleado": emp})
                emp["password"] = password

            messages.success(request, f'Empleado "{emp["nombre"]}" actualizado correctamente.')
            return redirect("Tienda:empleados_list")

    return render(request, "Tienda/empleados/empleado_form.html", {"empleado": emp})

@require_role('DUEÑA')
def empleado_delete(request, id):
    emp = next((e for e in empleados if e["id"] == id), None)
    if not emp:
        raise Http404("Empleado no encontrado")

    if request.method == "POST":
        nombre = emp["nombre"]
        empleados[:] = [e for e in empleados if e["id"] != id]
        messages.success(request, f'Empleado "{nombre}" eliminado correctamente.')
        return redirect("Tienda:empleados_list")

    return render(request, "Tienda/empleados/empleado_confirmar_eliminar.html", {"empleado": emp})



#movimientos en base de models tablas ricardo


# --------- CREDENCIALES (DUEÑA) ---------
@require_role('DUEÑA')
def credenciales_list(request):
    objetos = Credenciales.objects.all().order_by('idcredenciales')
    return render(request, "Tienda/credenciales/credenciales_list.html", {"objetos": objetos})

@require_role('DUEÑA')
def credencial_create(request):
    form = CredencialesForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Credencial creada correctamente.")
        return redirect("Tienda:credenciales_list")
    return render(request, "Tienda/credenciales/credencial_form.html", {"form": form})

@require_role('DUEÑA')
def credencial_edit(request, pk):
    obj = get_object_or_404(Credenciales, pk=pk)
    form = CredencialesForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Credencial actualizada correctamente.")
        return redirect("Tienda:credenciales_list")
    return render(request, "Tienda/credenciales/credencial_form.html", {"form": form, "obj": obj})

@require_role('DUEÑA')
def credencial_delete(request, pk):
    obj = get_object_or_404(Credenciales, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Credencial eliminada correctamente.")
        return redirect("Tienda:credenciales_list")
    return render(request, "Tienda/credenciales/credencial_confirmar_eliminar.html", {"obj": obj})


# --------- MOVIMIENTOS (DUEÑA) ---------
@require_role('DUEÑA')
def movimientos_list(request):
    objetos = Movimiento.objects.all().order_by('-fecha')
    return render(request, "Tienda/movimientos/movimientos_list.html", {"objetos": objetos})

@require_role('DUEÑA')
def movimiento_create(request):
    form = MovimientoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Movimiento creado correctamente.")
        return redirect("Tienda:movimientos_list")
    return render(request, "Tienda/movimientos/movimiento_form.html", {"form": form})

@require_role('DUEÑA')
def movimiento_edit(request, pk):
    obj = get_object_or_404(Movimiento, pk=pk)
    form = MovimientoForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Movimiento actualizado correctamente.")
        return redirect("Tienda:movimientos_list")
    return render(request, "Tienda/movimientos/movimiento_form.html", {"form": form, "obj": obj})

@require_role('DUEÑA')
def movimiento_delete(request, pk):
    obj = get_object_or_404(Movimiento, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Movimiento eliminado correctamente.")
        return redirect("Tienda:movimientos_list")
    return render(request, "Tienda/movimientos/movimiento_confirmar_eliminar.html", {"obj": obj})


# --------- HISTORIAL (DUEÑA) ---------
@require_role('DUEÑA')
def historial_list(request):
    objetos = Historial.objects.all().order_by('-fecha')
    return render(request, "Tienda/historial/historial_list.html", {"objetos": objetos})

@require_role('DUEÑA')
def historial_create(request):
    form = HistorialForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Entrada de historial creada correctamente.")
        return redirect("Tienda:historial_list")
    return render(request, "Tienda/historial/historial_form.html", {"form": form})

@require_role('DUEÑA')
def historial_edit(request, pk):
    obj = get_object_or_404(Historial, pk=pk)
    form = HistorialForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Entrada de historial actualizada correctamente.")
        return redirect("Tienda:historial_list")
    return render(request, "Tienda/historial/historial_form.html", {"form": form, "obj": obj})

@require_role('DUEÑA')
def historial_delete(request, pk):
    obj = get_object_or_404(Historial, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Entrada de historial eliminada correctamente.")
        return redirect("Tienda:historial_list")
    return render(request, "Tienda/historial/historial_confirmar_eliminar.html", {"obj": obj})