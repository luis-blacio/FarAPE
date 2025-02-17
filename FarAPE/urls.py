"""
URL configuration for FarAPE project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from FarmAPE import views
from FarmAPE.views import registro_cliente, home, GestionInventarioListView, \
    GestionInventarioUpdateView, GestionInventarioCreateView, CrearTransferenciaView, ListaTransferenciasView, \
    MedicamentoListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', registro_cliente, name='registro'),
    path('', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('home/', home, name='home'),
    path('inventario/', GestionInventarioListView.as_view(), name='gestion_inventario'),
    path('inventario/editar/<int:pk>/', GestionInventarioUpdateView.as_view(), name='editar_inventario'),
    path('inventario/nuevo/', GestionInventarioCreateView.as_view(), name='nuevo_inventario'),
    path('transferencias/crear/', CrearTransferenciaView.as_view(), name='crear_transferencia'),
    path('transferencias/', ListaTransferenciasView.as_view(), name='transferencias_list'),
    path('medicamentos/', MedicamentoListView.as_view(), name='medicamento_list'),
    path('factura/crear/', views.crear_factura, name='crear_factura'),
    path('facturas/', views.ver_facturas, name='ver_facturas'),

]

