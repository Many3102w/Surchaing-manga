from webcomics.models import Manga

def manga_filters(request):
    genres = ['Accion', 'Aventura']
    manga_by_genre = {
        genre: Manga.objects.filter(type_of_manga=genre).order_by('-fecha_de_carga')[:5]
        for genre in genres
    }
    high_rated_mangas = Manga.objects.filter(calificacion_promedio__gte=8.0).order_by('-calificacion_promedio', '-fecha_de_carga')
    recent_mangas = Manga.objects.order_by('-fecha_de_carga')
    
    return {
        'high_rated_mangas': high_rated_mangas,
        'recent_mangas': recent_mangas,
        'manga_by_genre': manga_by_genre,
    }
