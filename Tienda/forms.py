# Tienda/forms.py
from django import forms
from .models import Credenciales, Movimiento, Historial

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


# --- MOVIMIENTO (sin FK: guardamos solo IDs) ----------------------
class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['descripcion', 'fecha', 'tipo']
        widgets = {
            'descripcion':         forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'fecha':               forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'tipo':                forms.TextInput(attrs={'class': 'form-control'})
        }


# --- HISTORIAL (sin FK: guardamos solo IDs) ----------------------
class HistorialForm(forms.ModelForm):
    class Meta:
        model = Historial
        fields = ['fecha']
        widgets = {
            'fecha':             forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
        }