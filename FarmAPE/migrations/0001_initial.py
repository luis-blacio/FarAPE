# Generated by Django 5.1.6 on 2025-02-17 19:41

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cedula', models.CharField(max_length=20, unique=True)),
                ('telefono', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Farmacia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.TextField()),
                ('telefono', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Medicamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroFactura', models.IntegerField()),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('total', models.FloatField()),
                ('metodoPago', models.CharField(choices=[('EFECTIVO', 'Efectivo'), ('TARJETA', 'Tarjeta')], max_length=20)),
                ('opcion_entrega', models.CharField(choices=[('RETIRO', 'Retiro'), ('ENVIO', 'Envío')], default='RETIRO', max_length=20)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facturas', to='FarmAPE.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='ItemFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroitemfactura', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_factura', to='FarmAPE.factura')),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_factura', to='FarmAPE.medicamento')),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeroSucursal', models.CharField(max_length=50)),
                ('direccion', models.TextField()),
                ('telefono', models.CharField(max_length=20)),
                ('farmacia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sucursales', to='FarmAPE.farmacia')),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventarios', to='FarmAPE.medicamento')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventarios', to='FarmAPE.sucursal')),
            ],
        ),
        migrations.AddField(
            model_name='factura',
            name='sucursal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facturas', to='FarmAPE.sucursal'),
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('cedula', models.CharField(max_length=20, unique=True)),
                ('rol', models.CharField(choices=[('ADMINISTRADOR', 'Administrador'), ('EMPLEADO', 'Empleado')], max_length=20)),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empleados', to='FarmAPE.sucursal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_transferencia', models.IntegerField()),
                ('cantidad', models.IntegerField()),
                ('fecha', models.DateField()),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('COMPLETADA', 'Completada'), ('CANCELADA', 'Cancelada')], max_length=20)),
                ('medicamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias', to='FarmAPE.medicamento')),
                ('sucursal_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_destino', to='FarmAPE.sucursal')),
                ('sucursal_origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_origen', to='FarmAPE.sucursal')),
            ],
        ),
    ]
