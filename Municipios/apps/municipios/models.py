from django.db import models

# Create your models here.
class Municipio(models.Model):
    nombre = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    habitantes = models.IntegerField()
    superficie = models.FloatField()
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre