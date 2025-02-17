from django.contrib.auth import login
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView

from .forms import RegistroClienteForm, InventarioForm, TransferenciaForm, MedicamentoForm, FacturaForm
from .models import Cliente, Farmacia, Sucursal, Medicamento, Factura, ItemFactura, Transferencia


def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            # Crear el usuario
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Crear el cliente asociado
            Cliente.objects.create(
                nombre=Cliente.nombre,
                cedula=Cliente.cedula,  # Puedes reemplazar esto con otro dato si lo necesitas
                telefono=Cliente.telefono,
                email=Cliente.email
            )

            # Iniciar sesión automáticamente
            login(request, user)
            return redirect('/')  # Redirige a la página principal o deseada
    else:
        form = RegistroClienteForm()

    return render(request, 'registro.html', {'form': form})


def home(request):
    # Obtener las farmacias, sucursales y medicamentos para mostrar
    farmacias = Farmacia.objects.all()
    sucursales = Sucursal.objects.all()
    medicamentos = Medicamento.objects.all()

    return render(request, 'home.html', {
        'farmacias': farmacias,
        'sucursales': sucursales,
        'medicamentos': medicamentos
    })


class NoClienteMixin:
    def dispatch(self, request, *args, **kwargs):
        # Verificar si el usuario tiene un objeto Cliente asociado
        if hasattr(request.user, 'Cliente'):
            # Si el usuario es cliente, lo redirigimos o mostramos un error
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return super().dispatch(request, *args, **kwargs)

from django.shortcuts import render
from .models import Inventario

class GestionInventarioListView(ListView):
    model = Inventario
    template_name = 'gestion_inventario.html'
    context_object_name = 'inventarios'
    paginate_by = 10  # Paginación de 10 resultados por página

    # Filtrar inventarios de una sucursal (si se necesita)
    def get_queryset(self):
        return Inventario.objects.all()

class GestionInventarioUpdateView(UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'editar_inventario.html'
    success_url = reverse_lazy('gestion_inventario')  # Redirige a la lista de inventarios

    def form_valid(self, form):
        # Aquí se pueden agregar más validaciones, por ejemplo, si el stock no puede ser negativo
        return super().form_valid(form)

class GestionInventarioCreateView(CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'nuevo_inventario.html'
    success_url = reverse_lazy('gestion_inventario')



class CrearTransferenciaView(View):
    def get(self, request):
        form = TransferenciaForm()
        return render(request, 'crear_transferencia.html', {'form': form})

    def post(self, request):
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            transferencia = form.save(commit=False)
            # Obtenemos datos de la transferencia
            origen = transferencia.sucursal_origen
            destino = transferencia.sucursal_destino
            medicamento = transferencia.medicamento
            cantidad = transferencia.cantidad

            # Verificamos el inventario en la sucursal de origen
            inventario_origen = origen.inventario_list.filter(medicamento=medicamento).first()
            inventario_destino = destino.inventario_list.filter(medicamento=medicamento).first()

            if inventario_origen and inventario_origen.cantidad >= cantidad:
                # Reducimos inventario en origen
                inventario_origen.cantidad -= cantidad
                inventario_origen.save()

                # Aumentamos inventario en destino o creamos uno nuevo
                if inventario_destino:
                    inventario_destino.cantidad += cantidad
                    inventario_destino.save()
                else:
                    destino.inventario_list.create(medicamento=medicamento, cantidad=cantidad)

                transferencia.estado = 'COMPLETADA'
            else:
                transferencia.estado = 'CANCELADA'

            transferencia.save()  # Guardamos finalmente la transferencia
            return redirect('transferencias_list')
        return render(request, 'crear_transferencia.html', {'form': form})


class ListaTransferenciasView(View):
    def get(self, request):
        transferencias = Transferencia.objects.all()
        return render(request, 'lista_transferencias.html', {'transferencias': transferencias})

class MedicamentoListView(View):
    def get(self, request):
        medicamentos = Medicamento.objects.all()
        form = MedicamentoForm()
        return render(request, 'medicamento_list.html', {'medicamentos': medicamentos, 'form': form})

    def post(self, request):
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/medicamentos')
        medicamentos = Medicamento.objects.all()
        return render(request, 'medicamento_list.html', {'medicamentos': medicamentos, 'form': form})

def crear_factura(request):
        if request.method == 'POST':
            form = FacturaForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('ver_facturas')  # Redirige a la vista que mostrará todas las facturas creadas
        else:
            form = FacturaForm()
        return render(request, 'crear_factura.html', {'form': form})

def ver_facturas(request):
        facturas = Factura.objects.all()
        return render(request, 'ver_facturas.html', {'facturas': facturas})
