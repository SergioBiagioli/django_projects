from django.contrib import admin
from .models import Aplication, Make, Year, Model, Segment, Category, Part, PartProperty

admin.site.register(Aplication)
admin.site.register(Make)
admin.site.register(Year)
admin.site.register(Model)
admin.site.register(Segment)
admin.site.register(Category)
# admin.site.register(SubCategory)
admin.site.register(Part)
# admin.site.register(Property)
admin.site.register(PartProperty)