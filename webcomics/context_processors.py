from webcomics.models import Manga

def manga_filters(request):
    denim_mangas = Manga.objects.filter(type_of_manga='Denim Tears').order_by('-fecha_de_carga')[:6]
    essentials_mangas = Manga.objects.filter(type_of_manga='Essentials').order_by('-fecha_de_carga')[:6]
    porsche_mangas = Manga.objects.filter(type_of_manga='Porsche 911').order_by('-fecha_de_carga')[:6]
    
    recent_mangas = Manga.objects.order_by('-fecha_de_carga')
    
    return {
        'recent_mangas': recent_mangas,
        'denim_mangas': denim_mangas,
        'essentials_mangas': essentials_mangas,
        'porsche_mangas': porsche_mangas,
    }
