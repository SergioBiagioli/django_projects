from django.db import models

class User(models.Model):
    name = models.Charfield(max_lenght=128)
    email= models.Charfield(max_lenght=128)