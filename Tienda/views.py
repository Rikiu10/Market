from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, Http404
from functools import wraps
from django.contrib import messages
from django.db import transaction
from django.forms import formset_factory

# Services (productos/alertas históricos simulados)
from .models import ProductoService
from .data import AlertaService, HistorialService

# Modelos y formularios (CRUDs “sin FK”)
from .models import Credenciales, Movimiento, Historial, Venta, Empleado, TipoEmpleado, DetalleVenta
from .forms import (
    CredencialesForm, MovimientoForm, HistorialForm,
    VentaForm, EmpleadoForm, TipoEmpleadoForm, DetalleVentaForm, VentaPOSForm
)

# ------------------- AUTENTICACIÓN “TEMPORAL” -------------------
USERS = {
    'gerente1': ('1234', 'GERENTE'),
    'jefe1':    ('1234', 'JEFE'),
    'emple1':   ('1234', 'EMPLEADO'),
    'duena1':   ('1234', 'DUEÑA'),
}

def get_account(username):
    """
    Devuelve (password, rol) para el login.

    1) Primero busca en el diccionario USERS (usuarios de prueba).
    2) Si no está, busca en Credenciales + Empleado + TipoEmpleado.
       - Credenciales.user = username
       - Empleado.credenciales = esa credencial
       - Empleado.tipoEmpleado.rol = GERENTE/JEFE/EMPLEADO
    """
    # 1) Usuarios hardcodeados
    if username in USERS:
        return USERS[username]   # (password, rol)

    # 2) Usuarios en la base de datos
    cred = Credenciales.objects.filter(user=username).first()
    if not cred:
        return None

    # buscamos el empleado que use esas credenciales
    empleado = (
        Empleado.objects
        .select_related('tipoEmpleado')
        .filter(credenciales=cred)
        .first()
    )

    if not empleado or not empleado.tipoEmpleado:
        # No tiene empleado asociado o no tiene tipo, no dejamos entrar
        return None

    rol = empleado.tipoEmpleado.rol.upper()   # GERENTE/JEFE/EMPLEADO
    return (cred.password, rol)

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

def index(request):
    # Si ya está logueado, manda al dashboard
    if request.session.get('role'):
        return redirect_by_role(request)

    ctx = {'error': None}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        account = get_account(username)  # <-- ahora usamos la BD también
        if account and account[0] == password:
            request.session['username'] = username
            request.session['role'] = account[1]
            return redirect_by_role(request)

        ctx['error'] = 'Usuario o contraseña incorrectos.'
    return render(request, "Tienda/index.html", ctx)


def login_view(request):
    if request.session.get('role'):
        return redirect_by_role(request)

    ctx = {'error': None}
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        account = get_account(username)
        if account and account[0] == password:
            request.session['username'] = username
            request.session['role'] = account[1]
            return redirect_by_role(request)

        ctx['error'] = 'Usuario o contraseña incorrectos.'
    return render(request, 'Tienda/index.html', ctx)


def logout_view(request):
    request.session.flush()
    return redirect('Tienda:login')

# ------------------------- DASHBOARDS ---------------------------
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

def _to_int(value, allow_zero=True):
    """Convierte strings como '1.200', '1,200', '1200', '12,0' a int."""
    if value is None:
        raise ValueError("valor vacío")
    s = str(value).strip()
    if s == "":
        raise ValueError("valor vacío")
    s = s.replace(".", "").replace(",", ".")
    n = float(s)
    if not allow_zero and n == 0:
        raise ValueError("cero no permitido")
    return int(n)

# -------------------- VENTAS/REPORTES ----------------------
# (estas vistas son las que tenías para GERENTE/JEFE basadas en memoria)
ventas_demo = [
    {"id": 1, "fecha": "2025-09-01", "total": 15000},
    {"id": 2, "fecha": "2025-09-02", "total": 25000},
]
carrito_demo = [
    {"nombre": "Arroz", "cantidad": 2, "precio": 1500, "subtotal": 3000},
    {"nombre": "Aceite", "cantidad": 1, "precio": 5000, "subtotal": 5000},
]

@require_role('GERENTE', 'JEFE', 'EMPLEADO')
def ventas_list(request):
    # Tomamos las ventas reales desde la BD
    objetos = Venta.objects.select_related('empleado').order_by('-fecha', '-idventa')
    return render(request, "Tienda/ventas/ventas_list.html", {"objetos": objetos})

@require_role('GERENTE','JEFE','EMPLEADO')
def venta_form(request):
    if request.method == "POST":
        nueva_venta = {
            "id": len(ventas_demo) + 1,
            "fecha": request.POST.get("fecha"),
            "total": request.POST.get("total"),
        }
        ventas_demo.append(nueva_venta)
        return redirect("Tienda:ventas_list")
    return render(request, "Tienda/ventas/venta_form.html")

@require_role('GERENTE','JEFE','EMPLEADO')
def venta_edit(request, id):
    venta = next((v for v in ventas_demo if v["id"] == id), None)
    if not venta:
        return redirect("Tienda:ventas_list")
    if request.method == "POST":
        venta["fecha"] = request.POST.get("fecha")
        venta["total"] = request.POST.get("total")
        return redirect("Tienda:ventas_list")
    return render(request, "Tienda/ventas/venta_form.html", {"venta": venta})

@require_role('GERENTE','JEFE','EMPLEADO')
def venta_delete(request, id):
    global ventas_demo
    ventas_demo = [v for v in ventas_demo if v["id"] != id]
    return redirect("Tienda:ventas_list")

@require_role('EMPLEADO','JEFE','GERENTE')
def carrito_view(request):
    total = sum(i['subtotal'] for i in carrito_demo)
    return render(request, "Tienda/ventas/carrito.html", {"carrito": carrito_demo})

@require_role('GERENTE', 'JEFE')
def reportes_view(request):
    reportes = {"diarias": 5, "semanales": 20, "mensuales": 80, "top_producto": "Arroz"}
    return render(request, "Tienda/ventas/reportes.html", {"reportes": reportes})

# --------------------- PRODUCTOS (services) ---------------------
@require_role('JEFE','GERENTE')
def producto_list(request):
    productos = ProductoService.obtener_todos()
    return render(request, "Tienda/productos/productos_list.html", {"productos": productos})

@require_role('JEFE','GERENTE')
def producto_create(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()  
        precio = request.POST.get('precio', '')
        stock = request.POST.get('stock', '')
        cantidad_minima = request.POST.get('cantidad_minima', '')

        try:
            if not nombre:
                messages.error(request, 'El nombre del producto es obligatorio')
                raise ValueError("nombre vacío")

            precio_i = _to_int(precio, allow_zero=False)
            stock_i = _to_int(stock, allow_zero=True)
            min_i = _to_int(cantidad_minima, allow_zero=True)

            if precio_i <= 0:
                messages.error(request, 'El precio debe ser mayor a 0')
                raise ValueError("precio <= 0")
            if stock_i < 0:
                messages.error(request, 'El stock no puede ser negativo')
                raise ValueError("stock < 0")
            if min_i < 0:
                messages.error(request, 'La cantidad mínima no puede ser negativa')
                raise ValueError("min < 0")

            ProductoService.crear(nombre, precio_i, stock_i, min_i, descripcion=descripcion)
            messages.success(request, f'Producto "{nombre}" creado correctamente')
            return redirect("Tienda:producto_list")

        except ValueError:
            if not any('obligatorio' in m.message or 'debe' in m.message for m in messages.get_messages(request)):
                messages.error(request, 'Error en los datos ingresados. Verifique los valores numéricos.')

    return render(request, "Tienda/productos/producto_form.html")

@require_role('JEFE','GERENTE')
def producto_edit(request, id):
    producto = ProductoService.obtener_por_id(id)
    if not producto:
        raise Http404("Producto no encontrado")

    if request.method == "POST":
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        precio = request.POST.get('precio', '')
        stock = request.POST.get('stock', '')
        cantidad_minima = request.POST.get('cantidad_minima', '')

        try:
            if not nombre:
                messages.error(request, 'El nombre del producto es obligatorio')
                raise ValueError("nombre vacío")

            precio_i = _to_int(precio, allow_zero=False)
            stock_i = _to_int(stock, allow_zero=True)
            min_i = _to_int(cantidad_minima, allow_zero=True)

            if precio_i <= 0:
                messages.error(request, 'El precio debe ser mayor a 0')
                raise ValueError("precio <= 0")
            if stock_i < 0:
                messages.error(request, 'El stock no puede ser negativo')
                raise ValueError("stock < 0")
            if min_i < 0:
                messages.error(request, 'La cantidad mínima no puede ser negativa')
                raise ValueError("min < 0")

            ProductoService.actualizar(id, nombre, precio_i, stock_i, min_i, descripcion=descripcion)
            messages.success(request, f'Producto "{nombre}" actualizado correctamente')
            return redirect("Tienda:producto_list")

        except ValueError:
            messages.error(request, 'Error en los datos ingresados. Verifique los valores numéricos.')

    return render(request, "Tienda/productos/producto_form.html", {"producto": producto})

@require_role('JEFE','GERENTE')
def producto_delete(request, id):
    producto = ProductoService.obtener_por_id(id)
    if not producto:
        raise Http404("Producto no encontrado")
    if request.method == "POST":
        nombre_producto = producto['nombre']
        ProductoService.eliminar(id)
        messages.success(request, f'Producto "{nombre_producto}" eliminado correctamente')
        return redirect("Tienda:producto_list")
    return render(request, "Tienda/productos/producto_confirmar_eliminar.html", {"producto": producto})

# ------------------- ALERTAS (services) -------------------------
@require_role('GERENTE', 'JEFE')
def alertas_view(request):
    alertas = AlertaService.obtener_todas()
    enriquecidas = []
    for alerta in alertas:
        producto = ProductoService.obtener_por_id(alerta['producto_id'])
        a = alerta.copy()
        a['producto'] = producto
        enriquecidas.append(a)
    return render(request, "Tienda/alertas/alertas_list.html", {"alertas": enriquecidas})

@require_role('GERENTE', 'JEFE')
def alerta_desactivar(request, alerta_id):
    alerta = AlertaService.obtener_por_id(alerta_id)
    if not alerta:
        raise Http404("Alerta no encontrada")
    if request.method == 'POST':
        AlertaService.desactivar_alerta(alerta_id)
        messages.success(request, 'Alerta desactivada correctamente')
        return redirect('Tienda:alertas')
    return render(request, 'Tienda/alertas/alerta_confirmar_desactivar.html', {'alerta': alerta})

@require_role('GERENTE', 'JEFE')
def alertas_historial_list(request):
    """Historial de alertas (vía services)"""
    historial = HistorialService.obtener_todo()
    historial_enriquecido = []
    for entrada in historial:
        producto = ProductoService.obtener_por_id(entrada['producto_id'])
        e = entrada.copy()
        e['producto'] = producto
        historial_enriquecido.append(e)
    return render(request, 'Tienda/alertas/historial_list.html', {'historial': historial_enriquecido})

# ---------------------- CRUDS (DUEÑA) ---------------------------
# CREDENCIALES
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

# MOVIMIENTOS
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

# HISTORIAL (tabla)
@require_role('GERENTE', 'JEFE')
def historial_list(request):
    objetos = Historial.objects.all().order_by('-fecha')
    return render(request, "Tienda/historial/historial_list.html", {"objetos": objetos})

@require_role('GERENTE', 'JEFE')
def historial_create(request):
    form = HistorialForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Entrada de historial creada correctamente.")
        return redirect("Tienda:historial_list")
    return render(request, "Tienda/historial/historial_form.html", {"form": form})

@require_role('GERENTE', 'JEFE')
def historial_edit(request, pk):
    obj = get_object_or_404(Historial, pk=pk)
    form = HistorialForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Entrada de historial actualizada correctamente.")
        return redirect("Tienda:historial_list")
    return render(request, "Tienda/historial/historial_form.html", {"form": form, "obj": obj})

@require_role('GERENTE', 'JEFE')
def historial_delete(request, pk):
    obj = get_object_or_404(Historial, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Entrada de historial eliminada correctamente.")
        return redirect("Tienda:historial_list")
    return render(request, "Tienda/historial/historial_confirmar_eliminar.html", {"obj": obj})

# VENTAS (CRUD Dueña)
@require_role('GERENTE', 'EMPLEADO')
def ventas_crud_list(request):
    objetos = Venta.objects.all().order_by('-fecha', '-idventa')
    return render(request, "Tienda/ventas/ventas_crud_list.html", {"objetos": objetos})

@require_role('GERENTE', 'EMPLEADO')
def venta_crud_create(request):
    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Venta creada correctamente.")
            return redirect("Tienda:ventas_crud_list")
    else:
        form = VentaForm()

    return render(request, "Tienda/ventas/venta_crud_form.html", {"form": form})

@require_role('GERENTE', 'JEFE', 'EMPLEADO')
def venta_crud_edit(request, pk):
    venta = get_object_or_404(Venta, pk=pk)

    if request.method == "POST":
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            messages.success(request, "Venta actualizada correctamente.")
            return redirect("Tienda:ventas_list")
    else:
        form = VentaForm(instance=venta)

    return render(
        request,
        "Tienda/ventas/venta_crud_form.html",
        {"form": form, "obj": venta}
    )


@require_role('GERENTE', 'JEFE', 'EMPLEADO')
def venta_crud_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)

    if request.method == "POST":
        venta.delete()
        messages.success(request, "Venta eliminada correctamente.")
        return redirect("Tienda:ventas_list")

    return render(
        request,
        "Tienda/ventas/venta_crud_confirmar_eliminar.html",
        {"obj": venta}
    )


# EMPLEADOS (CRUD Dueña)
@require_role('DUEÑA')
def empleados_list(request):
    objetos = Empleado.objects.all().order_by('idempleado')
    return render(request, "Tienda/empleados/empleados_list.html", {"objetos": objetos})

@require_role('DUEÑA')
def empleado_create(request):
    form = EmpleadoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Empleado creado correctamente.")
        return redirect("Tienda:empleados_list")
    return render(request, "Tienda/empleados/empleado_form.html", {"form": form})

@require_role('DUEÑA')
def empleado_edit(request, pk):
    obj = get_object_or_404(Empleado, pk=pk)
    form = EmpleadoForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Empleado actualizado correctamente.")
        return redirect("Tienda:empleados_list")
    return render(request, "Tienda/empleados/empleado_form.html", {"form": form, "obj": obj})

@require_role('DUEÑA')
def empleado_delete(request, pk):
    obj = get_object_or_404(Empleado, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Empleado eliminado correctamente.")
        return redirect("Tienda:empleados_list")
    return render(request, "Tienda/empleados/empleado_confirmar_eliminar.html", {"obj": obj})

# TIPOEMPLEADO (CRUD Dueña)
@require_role('DUEÑA')
def tipoempleado_list(request):
    objetos = TipoEmpleado.objects.all().order_by('idtipoEmpleado')
    return render(request, "Tienda/tipoempleado/tipoempleado_list.html", {"objetos": objetos})

@require_role('DUEÑA')
def tipoempleado_create(request):
    form = TipoEmpleadoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tipo de empleado creado correctamente.")
        return redirect("Tienda:tipoempleado_list")
    return render(request, "Tienda/tipoempleado/tipoempleado_form.html", {"form": form})

@require_role('DUEÑA')
def tipoempleado_edit(request, pk):
    obj = get_object_or_404(TipoEmpleado, pk=pk)
    form = TipoEmpleadoForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tipo de empleado actualizado correctamente.")
        return redirect("Tienda:tipoempleado_list")
    return render(request, "Tienda/tipoempleado/tipoempleado_form.html", {"form": form, "obj": obj})

@require_role('DUEÑA')
def tipoempleado_delete(request, pk):
    obj = get_object_or_404(TipoEmpleado, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Tipo de empleado eliminado correctamente.")
        return redirect("Tienda:tipoempleado_list")
    return render(request, "Tienda/tipoempleado/tipoempleado_confirmar_eliminar.html", {"obj": obj})


@require_role('EMPLEADO', 'JEFE', 'GERENTE')
def venta_pos_create(request):
    DetalleFormSet = formset_factory(DetalleVentaForm, extra=3)  # 3 filas de detalle vacías

    if request.method == 'POST':
        venta_form = VentaPOSForm(request.POST)
        detalle_formset = DetalleFormSet(request.POST)

        if venta_form.is_valid() and detalle_formset.is_valid():
            with transaction.atomic():
                venta = venta_form.save(commit=False)

                total = 0
                detalles_validos = []

                for f in detalle_formset:
                    if not f.cleaned_data:
                        # fila completamente vacía
                        continue

                    producto = f.cleaned_data['producto']
                    cantidad = f.cleaned_data['cantidad_producto']

                    if not producto or not cantidad:
                        continue

                    precio_unitario = producto.precio
                    subtotal = precio_unitario * cantidad
                    total += subtotal

                    detalles_validos.append((producto, cantidad, precio_unitario, subtotal))

                if not detalles_validos:
                    messages.error(request, "Debes ingresar al menos un producto.")
                else:
                    # guardar venta con total calculado
                    venta.total = total
                    venta.save()

                    # guardar detalles
                    for producto, cantidad, precio_unitario, subtotal in detalles_validos:
                        DetalleVenta.objects.create(
                            venta=venta,
                            producto=producto,
                            cantidad_producto=cantidad,
                            precio_unitario=precio_unitario,
                            subtotal=subtotal,
                        )

                    messages.success(request, f"Venta #{venta.idventa} creada por ${total}.")
                    return redirect('Tienda:ventas_crud_list')  # o la lista que estés usando

    else:
        venta_form = VentaPOSForm()
        detalle_formset = DetalleFormSet()

    return render(
        request,
        'Tienda/ventas/venta_pos_form.html',
        {
            'venta_form': venta_form,
            'detalle_formset': detalle_formset,
        }
    )