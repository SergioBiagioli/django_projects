from django.contrib import admin

# Register your models here.
from .models import Auto
from .models import Make

admin.site.register(Auto)
admin.site.register(Make)
