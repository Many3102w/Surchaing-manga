from django.contrib import admin
from .models import Manga
# Register your models here.

@admin.register(Manga)
class Mangas_admin(admin.ModelAdmin):
    pass