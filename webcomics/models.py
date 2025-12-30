from typing import Any
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Esto va estar cargado desde una vista. En admin se puede modificar.
class Manga(models.Model):
    class Meta:
        app_label = 'webcomics'
        db_table = 'Mangas'
        db_table_comment = """
Tabla para la gestión de mangas en la base de datos.
        """

    Types_of_mangas = [
        ('Denim Tears', 'Denim Tears'),
        ('Essentials', 'Essentials'),
        ('Porsche 911', 'Porsche 911')
    ]

    #Se aplicaron mejores practicas para el modelo 
    
    nombre_del_manga = models.CharField(verbose_name="Nombre del manga", unique=True, max_length=100, db_column="nombre")
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True, db_column="descripcion")
    fecha_de_carga = models.DateField(verbose_name="Fecha de carga", max_length=100, db_column="fecha")
    publicado_por = models.CharField(verbose_name="publicado_por", max_length=100, blank=True, db_column="autor")
    front_page = models.ImageField(verbose_name="portada", upload_to='front_pages/', blank=True, db_column='portadas')

    manga_file = models.FileField(verbose_name="Archivo del manga", blank=True, null=True, db_column="archivo")

    type_of_manga = models.CharField(verbose_name="Género del manga", choices=Types_of_mangas,
                                    help_text="Agregar el género del manga", blank=True, default=Types_of_mangas[0], max_length=100,
                                    db_column="genero del manga"
                                    )
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

class Comment(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.manga}'

class Like(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('manga', 'user')

    def __str__(self):
        return f'{self.user.username} likes {self.manga}'

class Favorite(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='favorited_by')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('manga', 'user')

    def __str__(self):
        return f'{self.user.username} favorited {self.manga}'
