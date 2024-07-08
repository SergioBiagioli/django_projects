from django.forms import ModelForm
from autos.models import Make
from autos.models import Auto

class MakeForm(ModelForm):
    class meta:
        model = Make
        fields = '__all__'

class AutoForm(ModelForm):
    class meta:
        model = Auto
        fields = '__all__'