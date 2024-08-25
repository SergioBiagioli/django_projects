from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey

class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now, editable=False)
    created_by = models.ForeignKey(User, related_name='created_%(class)s_set', on_delete=models.CASCADE, default=1)
    updated_by = models.ForeignKey(User, related_name='updated_%(class)s_set', on_delete=models.CASCADE, default=1)


    class Meta:
        abstract = True

class Make(BaseModel):
    make = models.CharField(
        max_length=200,
        help_text='Enter a make (e.g. Yamaha)',
        validators=[MinLengthValidator(2, "Make must be greater than 1 character")],
        unique=True
    )

    def __str__(self):
        return self.make

class Year(BaseModel):
    year = models.PositiveIntegerField(
        help_text='Enter a year (e.g. 1995)',
        unique=True
    )

    def __str__(self):
        return str(self.year)

class Model(BaseModel):
    model = models.CharField(
        max_length=200,
        help_text='Enter a model (e.g. YZ 250FX)',
        validators=[MinLengthValidator(2, "Model must be greater than 1 character")],
        unique=True
    )

    def __str__(self):
        return self.model

class Segment(BaseModel):
    segment = models.CharField(
        max_length=30,
        help_text='Enter a segment (e.g. Off-Road, Trail)',
        validators=[MinLengthValidator(2, "Segment must be greater than 1 character")],
        unique=True,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.segment

class Aplication(BaseModel):
    market_choices = [
        ('US', 'United States'),
        ('EU', 'Europe'),
        ('ARG', 'Argentina'),
        ('AU', 'Australia'),
    ]
    
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE)
    make = models.ForeignKey(Make, on_delete=models.CASCADE)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    market = models.CharField(max_length=3, choices=market_choices)
    
    def __str__(self):
        return f"{self.segment} > {self.make} > {self.year} > {self.model}"

class AplicationPhoto(BaseModel):
    aplication = models.ForeignKey(Aplication, related_name='photos', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='aplication_photos/')

class Category(MPTTModel, BaseModel):
    category = models.CharField(
        max_length=200,
        help_text="Enter a category (e.g. Engine, Frame, Suspension)",
        validators=[MinLengthValidator(2, 'Categories must be greater than 1 character')]
    )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['category']

    def __str__(self):
        return self.category
    
    
#-----------------------------------------------Modelo obsoleto----------------------------------------------------------
# class SubCategory(MPTTModel, BaseModel):
#     subcategory = models.CharField(
#         max_length=200,
#         help_text="Enter a subcategory name",
#         validators=[MinLengthValidator(2, 'Subcategories must be greater than 1 character')]
#     )
#     category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
#     parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

#     def __str__(self):
#         return self.subcategory
#-----------------------------------------------Modelo obsoleto----------------------------------------------------------
# class Property(BaseModel):
#     name = models.CharField(
#         max_length=100,
#         help_text="Enter the property name (e.g. Internal Diameter, External Diameter, Material)"
#     )

#     def __str__(self):
#         return self.name


class Part(BaseModel):
    sku = models.CharField(max_length=50, help_text="Enter de SKU", validators=[MinLengthValidator(2, "SKU must be greater than 1 character")])
    name = models.CharField(
        max_length=100,
        help_text="Enter the general part name (e.g. Spark Plug)",
        validators=[MinLengthValidator(2, "Part name must be greater than 1 character")]
    )
    categories = models.ManyToManyField(Category, related_name='parts')
    applications = models.ManyToManyField(Aplication, related_name='parts')
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        categories_str = ' > '.join([cat.name for cat in self.categories.all()])
        # subcategories_str = ' > '.join([subcat.name for subcat in self.subcategories.all()])
        properties_str = ', '.join([f"{prop.property.name}: {prop.value}" for prop in self.properties.all()])
        
        # return f"{self.name}, {properties_str}, in {subcategories_str}-{categories_str}"
        return f"{self.name}, {properties_str}, in -{categories_str}"


class PartProperty(BaseModel):
    part = models.ForeignKey('Part', related_name='part', on_delete=models.CASCADE)
    property = models.CharField(max_length=100,help_text="Enter the property name (e.g. Internal Diameter, External Diameter, Material)")
    value = models.CharField(max_length=200,help_text="Enter the value of the property (e.g. 50mm, Steel)")

    def __str__(self):
        return f"{self.part} - {self.property}: {self.value}"
    


@receiver(pre_save, sender=BaseModel)
def set_default_user(sender, instance, **kwargs):
    if not instance.pk:  # Only for new objects
        default_user = User.objects.get(pk=1)
        if not instance.created_by:
            instance.created_by = default_user
        instance.updated_by = default_user