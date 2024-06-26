from webcomics.models import Manga

def manga_filters(request):
    high_rated_mangas = Manga.objects.filter(calificacion_promedio__gte=8.0)
    action_mangas = Manga.objects.filter(type_of_manga='Accion')
    adventure_mangas = Manga.objects.filter(type_of_manga='Aventura')
    
    return {
        'high_rated_mangas': high_rated_mangas,
        'action_mangas': action_mangas,
        'adventure_mangas': adventure_mangas
    }

