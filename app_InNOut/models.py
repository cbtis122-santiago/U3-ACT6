from django.db import models

# ==========================================
# MODELO: SUCURSAL
# ==========================================
class Sucursal(models.Model):
    nombre_tienda = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    telefono_tienda = models.CharField(max_length=150)
    codigo_postal = models.CharField(max_length=10)
    direccion = models.CharField(max_length=150)
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
    email = models.EmailField()
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