from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from webcomics.models import Manga
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    #vista en progreso
    manga = Manga.objects.all()
    print(type(manga))

    value = request.GET.get('termino')

    if value:
        buscar = Manga.objects.filter(
            nombre_del_manga = value
        )
        return render(request, "home.html", {"post": buscar})
    else:
        return render(request, "home.html", {"mangas": manga})

#Vista y lógica realizada para poder buscar los mangas por parámetro de url (en prueba)
def manga_view(request, name):
    manga = Manga.objects.filter(nombre_del_manga__contains=name)

    if manga.exists():
        mensaje = f"Mangas obtenido {name}"
    else:
        mensaje = f"Lamentablemente no se encontró el manga: {name}"

    return HttpResponse(mensaje)

def about(request):
    return HttpResponse("Sobre surchaing manga")

def registrar_usuario(request):
    #Vista para el registro
    return HttpResponse("Formulario de registro")

def watchlist(request):
    #Vista para la watchlist
    return HttpResponse("Watchlist")

def imdbpro(request):
    #?
    return HttpResponse("En proceso")

#pagina principal
def index(request):
    return render(request, "index.html", {})