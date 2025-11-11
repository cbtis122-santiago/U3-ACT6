from django.contrib import admin
from .models import Sucursal, Trabajador, Pedido

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('nombre_tienda', 'ciudad', 'telefono_tienda', 'es_drive_thru', 'fecha_apertura')
    search_fields = ('nombre_tienda', 'ciudad')
    list_filter = ('es_drive_thru',)

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'puesto', 'sucursal')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero_orden', 'total_pedido', 'tipo_orden', 'pagado', 'fecha_pedido')
    search_fields = ('numero_orden', 'tipo_orden')
    list_filter = ('pagado', 'tipo_orden')
