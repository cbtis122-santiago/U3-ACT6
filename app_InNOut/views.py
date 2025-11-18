from django.shortcuts import render, redirect, get_object_or_404
from .models import Sucursal, Trabajador, Pedido, Proveedor, Producto, Inventario
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



# ==========================================
# VISTAS PARA PROVEEDOR
# ==========================================
def agregar_proveedor(request):
    if request.method == 'POST':
        nombre_empresa = request.POST.get('nombre_empresa')
        contacto = request.POST.get('contacto')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        tipo_proveedor = request.POST.get('tipo_proveedor')
        activo = True if request.POST.get('activo') == 'on' else False

        Proveedor.objects.create(
            nombre_empresa=nombre_empresa,
            contacto=contacto,
            telefono=telefono,
            email=email,
            direccion=direccion,
            tipo_proveedor=tipo_proveedor,
            activo=activo
        )
        return redirect('ver_proveedores')
    return render(request, 'proveedor/agregar_proveedor.html')

def ver_proveedores(request):
    proveedores = Proveedor.objects.all().order_by('nombre_empresa')
    return render(request, 'proveedor/ver_proveedores.html', {'proveedores': proveedores})

def actualizar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    return render(request, 'proveedor/actualizar_proveedor.html', {'proveedor': proveedor})

def realizar_actualizacion_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        proveedor.nombre_empresa = request.POST.get('nombre_empresa')
        proveedor.contacto = request.POST.get('contacto')
        proveedor.telefono = request.POST.get('telefono')
        proveedor.email = request.POST.get('email')
        proveedor.direccion = request.POST.get('direccion')
        proveedor.tipo_proveedor = request.POST.get('tipo_proveedor')
        proveedor.activo = True if request.POST.get('activo') == 'on' else False
        proveedor.save()
        return redirect('ver_proveedores')
    return redirect('ver_proveedores')

def borrar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('ver_proveedores')
    return render(request, 'proveedor/borrar_proveedor.html', {'proveedor': proveedor})

# ==========================================
# VISTAS PARA PRODUCTO
# ==========================================
def agregar_producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        categoria = request.POST.get('categoria')
        precio = request.POST.get('precio')
        costo = request.POST.get('costo')
        disponible = True if request.POST.get('disponible') == 'on' else False
        imagen = request.POST.get('imagen')

        Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            categoria=categoria,
            precio=precio,
            costo=costo,
            disponible=disponible,
            imagen=imagen
        )
        return redirect('ver_productos')
    return render(request, 'producto/agregar_producto.html')

def ver_productos(request):
    productos = Producto.objects.all().order_by('categoria', 'nombre')
    return render(request, 'producto/ver_productos.html', {'productos': productos})

def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'producto/actualizar_producto.html', {'producto': producto})

def realizar_actualizacion_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.categoria = request.POST.get('categoria')
        producto.precio = request.POST.get('precio')
        producto.costo = request.POST.get('costo')
        producto.disponible = True if request.POST.get('disponible') == 'on' else False
        producto.imagen = request.POST.get('imagen')
        producto.save()
        return redirect('ver_productos')
    return redirect('ver_productos')

def borrar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        producto.delete()
        return redirect('ver_productos')
    return render(request, 'producto/borrar_producto.html', {'producto': producto})

# ==========================================
# VISTAS PARA INVENTARIO
# ==========================================
def agregar_inventario(request):
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()
    
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        proveedor_id = request.POST.get('proveedor')
        cantidad = request.POST.get('cantidad')
        unidad_medida = request.POST.get('unidad_medida')
        stock_minimo = request.POST.get('stock_minimo')
        ubicacion = request.POST.get('ubicacion')
        lote = request.POST.get('lote')

        producto = get_object_or_404(Producto, id=producto_id)
        proveedor = get_object_or_404(Proveedor, id=proveedor_id)

        Inventario.objects.create(
            producto=producto,
            proveedor=proveedor,
            cantidad=cantidad,
            unidad_medida=unidad_medida,
            stock_minimo=stock_minimo,
            ubicacion=ubicacion,
            lote=lote
        )
        return redirect('ver_inventarios')
    
    return render(request, 'inventario/agregar_inventario.html', {
        'productos': productos,
        'proveedores': proveedores
    })

def ver_inventarios(request):
    inventarios = Inventario.objects.all().order_by('producto__nombre')
    return render(request, 'inventario/ver_inventarios.html', {'inventarios': inventarios})

def actualizar_inventario(request, inventario_id):
    inventario = get_object_or_404(Inventario, id=inventario_id)
    productos = Producto.objects.all()
    proveedores = Proveedor.objects.all()
    
    return render(request, 'inventario/actualizar_inventario.html', {
        'inventario': inventario,
        'productos': productos,
        'proveedores': proveedores
    })

def realizar_actualizacion_inventario(request, inventario_id):
    inventario = get_object_or_404(Inventario, id=inventario_id)
    if request.method == 'POST':
        producto_id = request.POST.get('producto')
        proveedor_id = request.POST.get('proveedor')
        inventario.cantidad = request.POST.get('cantidad')
        inventario.unidad_medida = request.POST.get('unidad_medida')
        inventario.stock_minimo = request.POST.get('stock_minimo')
        inventario.ubicacion = request.POST.get('ubicacion')
        inventario.lote = request.POST.get('lote')
        
        inventario.producto = get_object_or_404(Producto, id=producto_id)
        inventario.proveedor = get_object_or_404(Proveedor, id=proveedor_id)
        inventario.save()
        
        return redirect('ver_inventarios')
    return redirect('ver_inventarios')

def borrar_inventario(request, inventario_id):
    inventario = get_object_or_404(Inventario, id=inventario_id)
    if request.method == 'POST':
        inventario.delete()
        return redirect('ver_inventarios')
    return render(request, 'inventario/borrar_inventario.html', {'inventario': inventario})