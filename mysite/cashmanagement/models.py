from django.db import models

class BaseEntity(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.nombre

class Empresa(BaseEntity):
    pass

class Sucursal(BaseEntity):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.empresa.nombre}"

class BaseMovimiento(models.Model):
    FISCAL_CHOICES = (
        ('Fiscal', 'Fiscal'),
        ('No Fiscal', 'No Fiscal'),
    )
    fecha = models.DateField()
    fecha_vencimiento = models.DateField()
    proveedor_cliente = models.CharField(max_length=255)
    modalidad = models.CharField(max_length=10, choices=FISCAL_CHOICES)
    importe_total = models.DecimalField(max_digits=10, decimal_places=2)
    importe_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    importe_adeudado = models.DecimalField(max_digits=10, decimal_places=2)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class EgresoCierto(BaseMovimiento):
    pass

class EgresoPresupuestado(BaseMovimiento):
    pass

class PresupuestoMensualFijo(models.Model):
    CATEGORIA_CHOICES = (
        ('Bancarios', 'Bancarios'),
        ('Tarjetas de credito', 'Tarjetas de credito'),
        ('Sueldos y remuneraciones', 'Sueldos y remuneraciones'),
        ('Proveedores', 'Proveedores'),
    )
    fecha = models.DateField()
    fecha_vencimiento = models.DateField()
    proveedor = models.CharField(max_length=255)
    modalidad = models.CharField(max_length=10, choices=BaseMovimiento.FISCAL_CHOICES)
    importe_total = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_CHOICES)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)

class IngresoCierto(BaseMovimiento):
    pass

class IngresoPrevisionado(BaseMovimiento):
    pass
