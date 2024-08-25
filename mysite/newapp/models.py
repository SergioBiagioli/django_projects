from django.db import models
from django.conf import settings
# Create your models here.

class Texto(models.Model):
    texto_1 = models.CharField(max_length=200)
    texto_2 = models.CharField(max_length=200)  
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='texto_owner',)

    def __str__(self):
        return f'{self.texto_1} {self.texto_2}'
        