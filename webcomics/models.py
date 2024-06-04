from typing import Any
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Esto va estar cargado desde una vista. En admin se puede modificar.
class Manga(models.Model):
    Types_of_mangas = [
        ('Accion', 'Acción'),
        ('Aventura', 'Aventura')
    ]
    
    nombre_del_manga = models.CharField(verbose_name="Nombre_del_manga", unique=True, max_length=100)
    fecha_de_carga = models.DateField(verbose_name="Fecha de carga", max_length=100)
    publicado_por = models.CharField(verbose_name="publicado_por", max_length=100, blank=True)
    front_page = models.ImageField(verbose_name="portada", upload_to='portadas/', blank=True)
    manga_file = models.FileField(verbose_name="Archivo_de_manga", blank=True)
    type_of_manga = models.CharField(verbose_name="Género del manga", choices=Types_of_mangas,
                                    help_text="Agregar el género del manga", blank=True, default=Types_of_mangas[0], max_length=10)
    calificacion_promedio = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        default=0.0,
        validators=[
            MinValueValidator(0.00), 
            MaxValueValidator(10.00)
        ]
    )

    # Atributos adicionales (si es necesario)

    def __str__(self): #Método de modelo
        return self.nombre_del_manga
