# forms.py
from django import forms
from mptt.forms import TreeNodeChoiceField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from vehicles.models import Make, Year, Model, Segment, Category, Part, Property, CatProperty, Aplication, AplicationPhoto

class MakeForm(forms.ModelForm):
    class Meta:
        model = Make
        fields = '__all__'
        exclude = ['created_by', 'updated_by']

class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = '__all__'
        exclude = ['created_by', 'updated_by']

class ModelForm(forms.ModelForm):
    class Meta:
        model = Model
        fields = '__all__'
        exclude = ['created_by', 'updated_by']

class SegmentForm(forms.ModelForm):
    class Meta:
        model = Segment
        fields = '__all__'
        exclude = ['created_by', 'updated_by']


class AplicationForm(forms.ModelForm):
    class Meta:
        model = Aplication
        fields = ['segment', 'make', 'year', 'model', 'market']

class AplicationPhotoForm(forms.ModelForm):
    class Meta:
        model = AplicationPhoto
        fields = ['photo'] 




class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category', 'parent']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Add Category'))





class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = '__all__'
        exclude = ['created_by', 'updated_by']

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        exclude = ['created_by', 'updated_by']

class CatPropertyForm(forms.ModelForm):
    class Meta:
        model = CatProperty
        fields = '__all__'
        exclude = ['created_by', 'updated_by']
