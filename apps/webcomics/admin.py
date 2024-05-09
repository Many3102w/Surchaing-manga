from django.contrib import admin
from .models import Manga
# Register your models here.


class Mangas_admin(admin.ModelAdmin):
    list_display = ('id', 'nombre_del_manga', 'fecha_de_carga', 'publicado_por', 'calificacion_promedio')
    search_fields = ("nombre_del_manga", "fecha_de_carga")
    list_editable = ('nombre_del_manga', 'calificacion_promedio', 'publicado_por', 'fecha_de_carga')

    date_hierarchy = "fecha_de_carga"
    empty_value_display = 'vacio'

admin.site.register(Manga, Mangas_admin)