from django import forms
from django.contrib.auth.models import User

from FarmAPE.models import Inventario, Transferencia, Medicamento, Factura


class RegistroClienteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirmar_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar_password = cleaned_data.get("confirmar_password")

        if password != confirmar_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['sucursal', 'medicamento', 'cantidad']

    # Validación personalizada (ejemplo: evitar cantidades negativas)
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")
        return cantidad


class TransferenciaForm(forms.ModelForm):
    class Meta:
        model = Transferencia
        fields = ['numero_transferencia', 'medicamento', 'sucursal_origen', 'sucursal_destino', 'cantidad', 'fecha']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }


class MedicamentoForm(forms.ModelForm):
    class Meta:
        model = Medicamento
        fields = ['nombre', 'precio']

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['numeroFactura', 'sucursal', 'fecha', 'cliente', 'total', 'metodoPago', 'opcion_entrega']
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'opcion_entrega': forms.Select(attrs={'class': 'custom-select'}),  # Añadir una clase personalizada al campo
        }