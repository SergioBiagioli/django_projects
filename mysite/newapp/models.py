from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings


# Create your models here.
class Texto(models.Model):
    texto_1 = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    texto_2 = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    
    def __str__(self):
        return f'{self.texto_1} {self.texto_2}