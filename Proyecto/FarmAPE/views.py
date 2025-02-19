from django.contrib.auth import login
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView,DeleteView
from .forms import RegistroClienteForm, InventarioForm, TransferenciaForm, MedicamentoForm, FacturaForm, SucursalForm
from .models import Cliente, Farmacia, Sucursal, Medicamento, Factura, ItemFactura, Transferencia, Inventario


def registro_cliente(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            Cliente.objects.create(
                nombre=form.cleaned_data['nombre'],
                cedula=form.cleaned_data['cedula'],
                telefono=form.cleaned_data['telefono'],
                email=form.cleaned_data['email']
            )

            login(request, user)
            return redirect('/')
    else:
        form = RegistroClienteForm()

    return render(request, 'registro.html', {'form': form})


def home(request):
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
        if hasattr(request.user, 'cliente'):
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return super().dispatch(request, *args, **kwargs)


class GestionInventarioListView(ListView):
    model = Inventario
    template_name = 'gestion_inventario.html'
    context_object_name = 'inventarios'
    paginate_by = 10

    def get_queryset(self):
        return Inventario.objects.all()


class GestionInventarioUpdateView(UpdateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'editar_inventario.html'
    success_url = reverse_lazy('gestion_inventario')

    def form_valid(self, form):
        return super().form_valid(form)


class GestionInventarioCreateView(CreateView):
    model = Inventario
    form_class = InventarioForm
    template_name = 'nuevo_inventario.html'
    success_url = reverse_lazy('gestion_inventario')


class CrearTransferenciaView(View):
    def get(self, request):
        form = TransferenciaForm()
        return render(request, 'creaTrans.html', {'form': form})

    def post(self, request):
        form = TransferenciaForm(request.POST)
        if form.is_valid():
            transferencia = form.save(commit=False)
            origen = transferencia.sucursal_origen
            destino = transferencia.sucursal_destino
            medicamento = transferencia.medicamento
            cantidad = transferencia.cantidad

            inventario_origen = origen.inventarios.filter(medicamento=medicamento).first()  #
            inventario_destino = destino.inventarios.filter(medicamento=medicamento).first()  #

            if inventario_origen and inventario_origen.cantidad >= cantidad:
                inventario_origen.cantidad -= cantidad
                inventario_origen.save()

                if inventario_destino:
                    inventario_destino.cantidad += cantidad
                    inventario_destino.save()
                else:
                    Inventario.objects.create(sucursal=destino, medicamento=medicamento, cantidad=cantidad)

                transferencia.estado = 'COMPLETADA'
            else:
                transferencia.estado = 'CANCELADA'

            transferencia.save()
            return redirect('transferencias_list')
        return render(request, 'creaTrans.html', {'form': form})



class ListaTransferenciasView(ListView):
    model = Transferencia
    template_name = 'lista_transferencias.html'
    context_object_name = 'transferencias'


class MedicamentoListView(View):
    def get(self, request):
        medicamentos = Medicamento.objects.all()
        form = MedicamentoForm()
        return render(request, 'medicamento_list.html', {'medicamentos': medicamentos, 'form': form})

    def post(self, request):
        form = MedicamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicamento_list')
        medicamentos = Medicamento.objects.all()
        return render(request, 'medicamento_list.html', {'medicamentos': medicamentos, 'form': form})


def crear_factura(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            # Guardar la factura
            factura = form.save(commit=False)
            factura.total = 0  # Inicializar el total en 0
            factura.save()

            # Procesar los ítems de la factura
            productos = request.POST.getlist('producto')
            cantidades = request.POST.getlist('cantidad')
            precios = request.POST.getlist('precio')

            for producto_id, cantidad, precio in zip(productos, cantidades, precios):
                if producto_id and cantidad and precio:
                    medicamento = Medicamento.objects.get(id=producto_id)
                    item_factura = ItemFactura(
                        factura=factura,
                        medicamento=medicamento,
                        cantidad=int(cantidad),
                        precio_unitario=float(precio)
                    )
                    item_factura.save()

                    # Actualizar el total de la factura
                    factura.total += float(precio) * int(cantidad)
                    factura.save()

            return redirect('ver_facturas')
    else:
        form = FacturaForm()

    # Obtener la lista de medicamentos para el formulario
    medicamentos = Medicamento.objects.all()
    return render(request, 'creaFac.html', {'form': form, 'medicamentos': medicamentos})
def ver_facturas(request):
    facturas = Factura.objects.all()
    return render(request, 'ver_facturas.html', {'facturas': facturas})


class CrearSucursalView(CreateView):
    model = Sucursal
    form_class = SucursalForm
    template_name = 'agregar_surcursal.html'
    success_url = reverse_lazy('lista_sucursales')


class ListaSucursalesView(ListView):
    model = Sucursal
    template_name = 'surcursal_list.html'
    context_object_name = 'sucursales'

class EliminarInventarioView(DeleteView):
    model = Inventario
    template_name = 'confirmar_eliminacion.html'  # Template para confirmar la eliminación
    success_url = reverse_lazy('gestion_inventario')  # Redirige a la gestión de inventario después de eliminar
