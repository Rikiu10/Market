# Tienda/forms.py
from django import forms
from .models import Credenciales, Movimiento, Historial, Venta, Empleado, TipoEmpleado

# --- CREDENCIALES -------------------------------------------------
class CredencialesForm(forms.ModelForm):
    class Meta:
        model = Credenciales
        fields = ['user', 'password']
        widgets = {
            'user':     forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean_user(self):
        u = self.cleaned_data['user'].strip().lower()
        if Credenciales.objects.filter(user=u).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Ese nombre de usuario ya existe.')
        return u

    def clean_password(self):
        p = self.cleaned_data['password']
        if not self.instance.pk and not p:
            raise forms.ValidationError('La contraseña es obligatoria al crear.')
        if p and len(p) < 4:
            raise forms.ValidationError('Mínimo 4 caracteres.')
        return p


class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['descripcion', 'fecha', 'tipo', 'producto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'fecha':       forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'tipo':        forms.TextInput(attrs={'class': 'form-control'}),
            'producto':    forms.Select(attrs={'class': 'form-control'}),
        }


# --- HISTORIAL (sin FK: guardamos solo IDs) ----------------------
class HistorialForm(forms.ModelForm):
    class Meta:
        model = Historial
        # ahora incluimos las FKs:
        fields = ['fecha', 'alerta', 'producto']
        widgets = {
            'fecha': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
            'alerta': forms.Select(attrs={'class': 'form-select'}),
            'producto': forms.Select(attrs={'class': 'form-select'}),
        }

#Venta
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        # AHORA incluimos el empleado
        fields = ['fecha', 'total', 'empleado']
        widgets = {
            'fecha': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'total': forms.NumberInput(
                attrs={'class': 'form-control'}
            ),
            'empleado': forms.Select(
                attrs={'class': 'form-select'}  # o 'form-control' si prefieres
            ),
        }

#Empleado
class EmpleadoForm(forms.ModelForm):
    #Form sin empleado/credenciales
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'email','credenciales', 'tipoEmpleado'] #sin ids
        widgets = {
            'nombre':   forms.TextInput(attrs={'class':'form-control'}),
            'apellido': forms.TextInput(attrs={'class':'form-control'}),
            'email':    forms.EmailInput(attrs={'class':'form-control'}),
            'credenciales': forms.Select(attrs={'class': 'form-control'}),
            'tipoEmpleado': forms.Select(attrs={'class': 'form-control'}),
        }

#TipoEmpleado
class TipoEmpleadoForm(forms.ModelForm):
    class Meta:
        model = TipoEmpleado
        fields = ['rol']
        widgets = {
            'rol': forms.TextInput(attrs={'class': 'form-control'}),
        }
