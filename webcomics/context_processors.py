from webcomics.models import Manga

def manga_filters(request):
    denim_mangas = Manga.objects.filter(type_of_manga='Denim Tears').order_by('-fecha_de_carga')[:6]
    essentials_mangas = Manga.objects.filter(type_of_manga='Essentials').order_by('-fecha_de_carga')[:6]
    dandy_mangas = Manga.objects.filter(type_of_manga='Dandy Hats').order_by('-fecha_de_carga')[:6]
    barbas_mangas = Manga.objects.filter(type_of_manga='Barbas Hats').order_by('-fecha_de_carga')[:6]
    
    recent_mangas = Manga.objects.order_by('-fecha_de_carga')
    
    return {
        'recent_mangas': recent_mangas,
        'denim_mangas': denim_mangas,
        'essentials_mangas': essentials_mangas,
        'dandy_mangas': dandy_mangas,
        'barbas_mangas': barbas_mangas,
    }
