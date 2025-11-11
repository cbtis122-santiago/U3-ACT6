from django.shortcuts import render, redirect, get_object_or_404
from .models import Sucursal, Trabajador, Pedido

# ==========================================
# INICIO
# ==========================================
def inicio_in_n_out(request):
    total_sucursales = Sucursal.objects.count()
    total_trabajadores = Trabajador.objects.count()
    sucursales = Sucursal.objects.all().order_by('-fecha_apertura')[:5]
    trabajadores = Trabajador.objects.all().order_by('-fecha_contratacion')[:5]
    return render(request, 'inicio.html', {
        'total_sucursales': total_sucursales,
        'total_trabajadores': total_trabajadores,
        'sucursales': sucursales,
        'trabajadores': trabajadores
    })


# ==========================================
# CRUD SUCURSAL
# ==========================================
def agregar_sucursal(request):
    if request.method == 'POST':
        nombre_tienda = request.POST.get('nombre_tienda')
        ciudad = request.POST.get('ciudad')
        codigo_postal = request.POST.get('codigo_postal')
        telefono_tienda = request.POST.get('telefono_tienda')
        direccion = request.POST.get('direccion')
        es_drive_thru = True if request.POST.get('es_drive_thru') == 'on' else False
        fecha_apertura = request.POST.get('fecha_apertura')

        Sucursal.objects.create(
            nombre_tienda=nombre_tienda,
            ciudad=ciudad,
            codigo_postal=codigo_postal,
            telefono_tienda=telefono_tienda,
            es_drive_thru=es_drive_thru,
            fecha_apertura=fecha_apertura
        )
        return redirect('ver_sucursales')

    return render(request, 'sucursal/agregar_sucursal.html')


def ver_sucursales(request):
    sucursales = Sucursal.objects.all().order_by('nombre_tienda')
    return render(request, 'sucursal/ver_sucursales.html', {'sucursales': sucursales})


def actualizar_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    return render(request, 'sucursal/actualizar_sucursal.html', {'sucursal': sucursal})


def realizar_actualizacion_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    if request.method == 'POST':
        sucursal.nombre_tienda = request.POST.get('nombre_tienda')
        sucursal.ciudad = request.POST.get('ciudad')
        sucursal.telefono_tienda = request.POST.get('telefono_tienda')
        sucursal.es_drive_thru = True if request.POST.get('es_drive_thru') == 'on' else False
        sucursal.fecha_apertura = request.POST.get('fecha_apertura')
        sucursal.save()
        return redirect('ver_sucursales')
    return redirect('ver_sucursales')


def borrar_sucursal(request, sucursal_id):
    sucursal = get_object_or_404(Sucursal, id=sucursal_id)
    if request.method == 'POST':
        sucursal.delete()
        return redirect('ver_sucursales')
    return render(request, 'sucursal/borrar_sucursal.html', {'sucursal': sucursal})


# ==========================================
# CRUD TRABAJADOR
# ==========================================
def agregar_trabajador(request):
    sucursales = Sucursal.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        puesto = request.POST.get('puesto')
        fecha_contratacion = request.POST.get('fecha_contratacion')
        email = request.POST.get('email')
        telefono_personal = request.POST.get('telefono_personal')
        sucursal_id = request.POST.get('sucursal')

        if sucursal_id:
            sucursal = get_object_or_404(Sucursal, id=sucursal_id)
        else:
            sucursal = None

        Trabajador.objects.create(
            nombre=nombre,
            apellido=apellido,
            puesto=puesto,
            fecha_contratacion=fecha_contratacion,
            email=email,
            telefono_personal=telefono_personal,
            sucursal=sucursal
        )
        return redirect('ver_trabajadores')

    return render(request, 'trabajador/agregar_trabajador.html', {'sucursales': sucursales})


def ver_trabajadores(request):
    trabajadores = Trabajador.objects.select_related('sucursal').all().order_by('nombre')
    return render(request, 'trabajador/ver_trabajadores.html', {'trabajadores': trabajadores})


def actualizar_trabajador(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, id=trabajador_id)
    sucursales = Sucursal.objects.all()
    return render(request, 'trabajador/actualizar_trabajador.html', {
        'trabajador': trabajador,
        'sucursales': sucursales
    })


def realizar_actualizacion_trabajador(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, id=trabajador_id)
    if request.method == 'POST':
        trabajador.nombre = request.POST.get('nombre')
        trabajador.apellido = request.POST.get('apellido')
        trabajador.puesto = request.POST.get('puesto')
        trabajador.fecha_contratacion = request.POST.get('fecha_contratacion')
        trabajador.email = request.POST.get('email')
        trabajador.telefono_personal = request.POST.get('telefono_personal')

        sucursal_id = request.POST.get('sucursal')
        if sucursal_id:
            trabajador.sucursal = get_object_or_404(Sucursal, id=sucursal_id)

        trabajador.save()
        return redirect('ver_trabajadores')

    return redirect('ver_trabajadores')


def borrar_trabajador(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, id=trabajador_id)
    if request.method == 'POST':
        trabajador.delete()
        return redirect('ver_trabajadores')
    return render(request, 'trabajador/borrar_trabajador.html', {'trabajador': trabajador})

# ==========================================
# CRUD PEDIDOS
# ==========================================
def agregar_pedido(request):
    trabajadores = Trabajador.objects.all().order_by('nombre')
    if request.method == 'POST':
        numero_orden = request.POST.get('numero_orden')
        total_pedido = request.POST.get('total_pedido') or 0
        tipo_orden = request.POST.get('tipo_orden')
        nombre_cliente_temporal = request.POST.get('nombre_cliente_temporal')
        pagado = True if request.POST.get('pagado') == 'on' else False
        trabajador_id = request.POST.get('trabajador')

        trabajador = get_object_or_404(Trabajador, id=trabajador_id) if trabajador_id else None

        Pedido.objects.create(
            numero_orden=numero_orden,
            total_pedido=total_pedido,
            tipo_orden=tipo_orden,
            nombre_cliente_temporal=nombre_cliente_temporal,
            pagado=pagado,
            trabajador=trabajador
        )
        return redirect('ver_pedidos')

    return render(request, 'pedido/agregar_pedido.html', {'trabajadores': trabajadores})


def ver_pedidos(request):
    pedidos = Pedido.objects.select_related('trabajador').all().order_by('-fecha_pedido')
    return render(request, 'pedido/ver_pedidos.html', {'pedidos': pedidos})


def actualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    trabajadores = Trabajador.objects.all()
    return render(request, 'pedido/actualizar_pedido.html', {
        'pedido': pedido,
        'trabajadores': trabajadores
    })


def realizar_actualizacion_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.numero_orden = request.POST.get('numero_orden')
        pedido.total_pedido = request.POST.get('total_pedido') or 0
        pedido.tipo_orden = request.POST.get('tipo_orden')
        pedido.nombre_cliente_temporal = request.POST.get('nombre_cliente_temporal')
        pedido.pagado = True if request.POST.get('pagado') == 'on' else False

        trabajador_id = request.POST.get('trabajador')
        if trabajador_id:
            pedido.trabajador = get_object_or_404(Trabajador, id=trabajador_id)

        pedido.save()
        return redirect('ver_pedidos')
    return redirect('ver_pedidos')


def borrar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        return redirect('ver_pedidos')
    return render(request, 'pedido/borrar_pedido.html', {'pedido': pedido})
