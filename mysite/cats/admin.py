from django.contrib import admin

# Register your models here.
from .models import Cat
from .models import Breed

admin.site.register(Cat)
admin.site.register(Breed)