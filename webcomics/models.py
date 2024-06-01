from typing import Any
from django.db import models

# Create your models here.

# Esto va estar cargado desde una vista. En admin se puede modificar.
class Manga(models.Model):
    class Meta:
        pass 
    Types_of_mangas = [
        ('Accion', 'Acción'),
        ('Aventura', 'Aventura')
    ]

    #Se aplicaron mejores practicas para el modelo 
    
    nombre_del_manga = models.CharField(verbose_name="Nombre del manga", unique=True, max_length=100, db_column="nombre")
    fecha_de_carga = models.DateField(verbose_name="Fecha de carga", max_length=100, db_column="Fecha")
    publicado_por = models.CharField(verbose_name="Autor del manga", max_length=100, blank=True, null=True, db_column="autor")
    front_page = models.ImageField(verbose_name="Portada", blank=True, null=True, upload_to='front_pages', db_column="portada")
    manga_file = models.FileField(verbose_name="Archivo del manga", blank=True, null=True, db_column="Archivo")
    calificacion_promedio = models.DecimalField("Calificación", max_digits=3, decimal_places=2, default=0.0,db_column="calificacion")
    type_of_manga = models.CharField(verbose_name="Género del manga", choices=Types_of_mangas,
                                    help_text="Agregar el género del manga", blank=True, null=True, default=Types_of_mangas[0], max_length=10, db_column="Genero")
    # Atributos adicionales (si es necesario)

    def __str__(self): #Método de modelo
        return self.nombre_del_manga