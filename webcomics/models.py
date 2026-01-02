from typing import Any
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

# Esto va estar cargado desde una vista. En admin se puede modificar.
class Manga(models.Model):
    class Meta:
        app_label = 'webcomics'
        db_table = 'Mangas'
        ordering = ['-id']
        db_table_comment = """
Tabla para la gestión de mangas en la base de datos.
        """

    Types_of_mangas = [
        ('Denim Tears', 'Denim Tears'),
        ('Essentials', 'Essentials'),
        ('Dandy Hats', 'Dandy Hats'),
        ('Barbas Hats', 'Barbas Hats')
    ]

    #Se aplicaron mejores practicas para el modelo 
    
    nombre_del_manga = models.CharField(verbose_name="Nombre del manga", unique=True, max_length=100, db_column="nombre")
    descripcion = models.TextField(verbose_name="Descripción", blank=True, null=True, db_column="descripcion")
    fecha_de_carga = models.DateField(verbose_name="Fecha de carga", max_length=100, db_column="fecha")
    publicado_por = models.CharField(verbose_name="publicado_por", max_length=100, blank=True, db_column="autor")
    talla = models.CharField(verbose_name="Talla", max_length=50, blank=True, null=True, help_text="Ej: S, M, L, XL o Talla de calzado")
    front_page = models.ImageField(verbose_name="portada", upload_to='front_pages/', blank=True, db_column='portadas')
    depth_map = models.ImageField(verbose_name="Mapa de Profundidad", upload_to='depth_maps/', blank=True, null=True, db_column='depth_map')
    mesh_3d = models.FileField(upload_to='meshes_3d/', null=True, blank=True)
    is_3d_converted = models.BooleanField(default=False, verbose_name="Convertido a 3D")

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
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Precio")
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Costo de Adquisición")
    vendido = models.BooleanField(default=False, verbose_name="Vendido")
    fecha_venta = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Venta")

    # Atributos adicionales (si es necesario)

    def __str__(self): #Método de modelo
        return self.nombre_del_manga

class MangaImage(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='manga_gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.manga.nombre_del_manga}"

class Comment(models.Model):
    manga = models.ForeignKey(Manga, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
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

class WarehouseItem(models.Model):
    category = models.CharField(max_length=100, unique=True, verbose_name="Categoría")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Cantidad en Almacén")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category}: {self.quantity}"

class WarehouseEntry(models.Model):
    warehouse_item = models.ForeignKey(WarehouseItem, on_delete=models.CASCADE, related_name='entries')
    manga = models.ForeignKey(Manga, on_delete=models.SET_NULL, null=True, blank=True, related_name='warehouse_entries')
    quantity = models.PositiveIntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"+{self.quantity} {self.warehouse_item.category} ({self.created_at.date()})"
