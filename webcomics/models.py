from typing import Any
from django.db import models

# Create your models here.

# Esto va estar cargado desde una vista. En admin se puede modificar.
class Manga(models.Model):
    nombre_del_manga = models.CharField(verbose_name="Nombre_del_manga", unique=True, max_length=100)
    fecha_de_carga = models.DateField(verbose_name="Fecha de carga", max_length=100)
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    # Atributos adicionales (si es necesario)

    def __str__(self):
        return self.nombre_del_manga