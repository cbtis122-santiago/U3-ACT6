from django.db import models

# ==========================================
# MODELO: SUCURSAL
# ==========================================
class Sucursal(models.Model):
    nombre_tienda = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    telefono_tienda = models.CharField(max_length=20)
    es_drive_thru = models.BooleanField(default=False)
    fecha_apertura = models.DateField()

    def __str__(self):
        return f"{self.nombre_tienda} - {self.ciudad}"

# ==========================================
# MODELO: TRABAJADOR
# ==========================================
class Trabajador(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    puesto = models.CharField(max_length=50)
    fecha_contratacion = models.DateField()
    email = models.EmailField(unique=True)
    telefono_personal = models.CharField(max_length=20, blank=True)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, related_name="trabajadores")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# ==========================================
# MODELO: PEDIDO
# ==========================================
class Pedido(models.Model):
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    numero_orden = models.PositiveIntegerField()
    total_pedido = models.DecimalField(max_digits=7, decimal_places=2)
    tipo_orden = models.CharField(max_length=50, help_text="Comer ahí o Para llevar")
    nombre_cliente_temporal = models.CharField(max_length=100, blank=True)
    pagado = models.BooleanField(default=False)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.SET_NULL, null=True, blank=True, related_name="pedidos")

    def __str__(self):
        return f"Pedido #{self.numero_orden}"

# ==========================================
# MODELO: PROVEEDOR (7 CAMPOS)
# ==========================================
class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=100)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion = models.TextField()
    tipo_proveedor = models.CharField(max_length=50, choices=[
        ('ALIMENTOS', 'Alimentos'),
        ('BEBIDAS', 'Bebidas'),
        ('LIMPIEZA', 'Limpieza'),
        ('EQUIPOS', 'Equipos')
    ])
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre_empresa

# ==========================================
# MODELO: PRODUCTO (7 CAMPOS)
# ==========================================
class Producto(models.Model):
    CATEGORIAS = [
        ('HAMBURGUESAS', 'Hamburguesas'),
        ('BEBIDAS', 'Bebidas'),
        ('PAPAS', 'Papas'),
        ('POSTRES', 'Postres'),
        ('COMBOS', 'Combos'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    costo = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    disponible = models.BooleanField(default=True)
    imagen = models.CharField(max_length=200, blank=True, help_text="URL de la imagen")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

# ==========================================
# MODELO: INVENTARIO (7 CAMPOS)
# ==========================================
class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="inventarios")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="inventarios")
    cantidad = models.PositiveIntegerField()
    unidad_medida = models.CharField(max_length=20, default="unidades")
    stock_minimo = models.PositiveIntegerField(default=10)
    ubicacion = models.CharField(max_length=50, default="Almacén principal")
    fecha_ultima_actualizacion = models.DateTimeField(auto_now=True)
    lote = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad} {self.unidad_medida}"