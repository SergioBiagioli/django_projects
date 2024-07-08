from django import forms
from .models import Empresa, Sucursal, EgresoCierto, EgresoPresupuestado, PresupuestoMensualFijo, IngresoCierto, IngresoPrevisionado

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'

class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = '__all__'

class EgresoCiertoForm(forms.ModelForm):
    class Meta:
        model = EgresoCierto
        fields = '__all__'

class EgresoPresupuestadoForm(forms.ModelForm):
    class Meta:
        model = EgresoPresupuestado
        fields = '__all__'

class PresupuestoMensualFijoForm(forms.ModelForm):
    class Meta:
        model = PresupuestoMensualFijo
        fields = '__all__'

class IngresoCiertoForm(forms.ModelForm):
    class Meta:
        model = IngresoCierto
        fields = '__all__'

class IngresoPrevisionadoForm(forms.ModelForm):
    class Meta:
        model = IngresoPrevisionado
        fields = '__all__'
