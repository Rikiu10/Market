from django.shortcuts import render, redirect


# Create your views here.
empleados = []
movimientos = []

def index(request):
    return render(request, 'Tienda/index.html')

def empleados_list(request):
    return render(request, 'Tienda/empleados/empleados_list.html', {'empleados': empleados})

def empleado_create(request):
    if request.method == 'POST':
        nuevo = {
            'id': len(empleados) + 1,
            'nombre': request.POST.get('nombre'),
            'apellido': request.POST.get('apellido'),
            'email': request.POST.get('email'),
            'rol': request.POST.get('rol'),
        }
        empleados.append(nuevo)
        return redirect('empleados_list')
    return render(request, 'Tienda/empleados/empleado_form.html')

def empleado_update(request, id):
    empleado = next((e for e in empleados if e['id'] == id), None)
    if request.method == 'POST' and empleado:
        empleado['nombre'] = request.POST.get('nombre')
        empleado['apellido'] = request.POST.get('apellido')
        empleado['email'] = request.POST.get('email')
        empleado['rol'] = request.POST.get('rol')
        return redirect('empleados_list')
    return render(request, 'Tienda/empleados/empleado_form.html', {'empleado': empleado})

def empleado_delete(request, id):
    global empleados
    empleados = [e for e in empleados if e['id'] != id]
    return redirect('empleados_list')

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == 'admin' and password == '1234': 
            return redirect('index')
        else:
            error = "Usuario o contraseña incorrectos"
    return render(request, 'Tienda/empleados/login.html', {'error': error})

def movimientos_list(request):
    return render(request, 'Tienda/movimientos/movimientos_list.html', {'movimientos': movimientos})

def movimiento_create(request):
    if request.method == 'POST':
        nuevo = {
            'id': len(movimientos) + 1,
            'producto': request.POST.get('producto'),
            'tipo': request.POST.get('tipo'),
            'cantidad': request.POST.get('cantidad'),
            'empleado': request.POST.get('empleado'),
            'fecha': '2025-09-04',
        }
        movimientos.append(nuevo)
        return redirect('movimientos_list')
    return render(request, 'Tienda/movimientos/movimientos_form.html')

def movimiento_update(request, id):
    movimiento = next((m for m in movimientos if m['id'] == id), None)
    if request.method == 'POST' and movimiento:
        movimiento['producto'] = request.POST.get('producto')
        movimiento['tipo'] = request.POST.get('tipo')
        movimiento['cantidad'] = request.POST.get('cantidad')
        movimiento['empleado'] = request.POST.get('empleado')
        return redirect('movimientos_list')
    return render(request, 'Tienda/movimientos/movimientos_form.html', {'movimiento': movimiento})

def movimiento_delete(request, id):
    global movimientos
    movimientos = [m for m in movimientos if m['id'] != id]
    return redirect('movimientos_list')

def productos_list(request):
    return render(request, 'Tienda/productos/productos_list.html')

def alertas_list(request):
    return render(request, 'Tienda/alertas/alertas_list.html')

def ventas_list(request):
    return render(request, 'Tienda/ventas/ventas_list.html')

