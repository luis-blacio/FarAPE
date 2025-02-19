from django.contrib import admin
from FarmAPE.models import (
    Farmacia, Sucursal, Medicamento, Inventario, Cliente,
    Empleado, Factura, ItemFactura, Transferencia
)

@admin.register(Farmacia)
class FarmaciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono')
    search_fields = ('nombre', 'direccion', 'telefono')
    list_filter = ('nombre',)

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('numeroSucursal', 'direccion', 'telefono', 'farmacia')
    search_fields = ('numeroSucursal', 'direccion', 'telefono', 'farmacia__nombre')
    list_filter = ('farmacia',)
    raw_id_fields = ('farmacia',)

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)
    list_filter = ('precio',)

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('sucursal', 'medicamento', 'cantidad')
    search_fields = ('sucursal__numeroSucursal', 'medicamento__nombre')
    list_filter = ('sucursal', 'medicamento')
    raw_id_fields = ('sucursal', 'medicamento')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'telefono', 'email')
    search_fields = ('nombre', 'cedula', 'telefono', 'email')

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cedula', 'sucursal', 'rol')
    search_fields = ('nombre', 'cedula', 'sucursal__numeroSucursal')
    list_filter = ('sucursal', 'rol')
    raw_id_fields = ('sucursal',)

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numeroFactura', 'fecha', 'cliente', 'sucursal', 'total', 'metodoPago')
    search_fields = ('numeroFactura', 'fecha', 'cliente__nombre', 'sucursal__numeroSucursal')
    list_filter = ('fecha', 'sucursal', 'metodoPago')
    raw_id_fields = ('cliente', 'sucursal')

@admin.register(ItemFactura)
class ItemFacturaAdmin(admin.ModelAdmin):
    list_display = ('numeroitemfactura', 'factura', 'medicamento', 'cantidad')
    search_fields = ('factura__numeroFactura', 'medicamento__nombre')
    list_filter = ('medicamento',)
    raw_id_fields = ('factura', 'medicamento')

@admin.register(Transferencia)
class TransferenciaAdmin(admin.ModelAdmin):
    list_display = ('numero_transferencia', 'medicamento', 'sucursal_origen', 'sucursal_destino', 'cantidad', 'fecha', 'estado')
    search_fields = ('numero_transferencia', 'medicamento__nombre', 'sucursal_origen__numeroSucursal', 'sucursal_destino__numeroSucursal')
    list_filter = ('fecha', 'estado', 'sucursal_origen', 'sucursal_destino')
    raw_id_fields = ('medicamento', 'sucursal_origen', 'sucursal_destino')
