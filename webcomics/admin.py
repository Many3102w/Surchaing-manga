from django.contrib import admin
from .models import Manga
# Register your models here.


class Mangas_admin(admin.ModelAdmin):
    list_display = ('id', 'nombre_del_manga', 'fecha_de_carga', 'publicado_por', 'front_page', 'manga_file', 'calificacion_promedio')
    search_fields = ("nombre_del_manga", "fecha_de_carga")
    list_editable = ('nombre_del_manga', 'fecha_de_carga', 'publicado_por', 'front_page', 'manga_file', 'calificacion_promedio')

    date_hierarchy = "fecha_de_carga"
    empty_value_display = 'vacio'

    fieldsets = [
    ("", {
        "fields": ["nombre_del_manga", "fecha_de_carga", "publicado_por", "calificacion_promedio"],
    }),
    # ...
]

admin.site.register(Manga, Mangas_admin)