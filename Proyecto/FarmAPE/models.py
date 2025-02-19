from django.db import models
from django.utils import timezone

class Farmacia(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Sucursal(models.Model):
    numeroSucursal = models.CharField(max_length=50)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    farmacia = models.ForeignKey(Farmacia, related_name='sucursales', on_delete=models.CASCADE)

    def __str__(self):
        return self.numeroSucursal

class Medicamento(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    sucursal = models.ForeignKey(Sucursal, related_name='inventarios', on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, related_name='inventarios', on_delete=models.CASCADE)
    cantidad = models.IntegerField()

class Persona(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)

    class Meta:
        abstract = True

class Cliente(Persona):
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} - {self.cedula}"

class Ocupacion(models.TextChoices):
    ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
    EMPLEADO = 'EMPLEADO', 'Empleado'

class Empleado(Persona):
    sucursal = models.ForeignKey(Sucursal, related_name='empleados', on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=Ocupacion.choices)

class MetodoPago(models.TextChoices):
    EFECTIVO = 'EFECTIVO', 'Efectivo'
    TARJETA = 'TARJETA', 'Tarjeta'

class MetodoEntrega(models.TextChoices):
    RETIRO = 'RETIRO', 'Retiro'
    ENVIO = 'ENVIO', 'Envío'

class Factura(models.Model):
    numeroFactura = models.IntegerField()
    sucursal = models.ForeignKey(Sucursal, related_name='facturas', on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey(Cliente, related_name='facturas', on_delete=models.CASCADE)
    total = models.FloatField()
    metodoPago = models.CharField(max_length=20, choices=MetodoPago.choices)
    opcion_entrega = models.CharField(max_length=20, choices=MetodoEntrega.choices, default=MetodoEntrega.RETIRO)

    def __str__(self):
        return f"Factura #{self.numeroFactura}"

class ItemFactura(models.Model):
    numeroitemfactura = models.IntegerField()
    factura = models.ForeignKey(Factura, related_name='items_factura', on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamento, related_name='items_factura', on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"Item Factura #{self.numeroitemfactura}"

class Estado(models.TextChoices):
    PENDIENTE = 'PENDIENTE', 'Pendiente'
    COMPLETADA = 'COMPLETADA', 'Completada'
    CANCELADA = 'CANCELADA', 'Cancelada'

class Transferencia(models.Model):
    numero_transferencia = models.IntegerField()
    medicamento = models.ForeignKey(Medicamento, related_name='transferencias', on_delete=models.CASCADE)
    sucursal_origen = models.ForeignKey(Sucursal, related_name='transferencias_origen', on_delete=models.CASCADE)
    sucursal_destino = models.ForeignKey(Sucursal, related_name='transferencias_destino', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField()
    estado = models.CharField(max_length=20, choices=Estado.choices)

    def __str__(self):
        return f"Transferencia #{self.numero_transferencia}"
