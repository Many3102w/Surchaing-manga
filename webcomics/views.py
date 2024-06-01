from django.shortcuts import render
from django.http import HttpResponse
from webcomics.models import Manga
from django.core.paginator import Paginator


# Create your views here.
#Vistas basadas en funciones

def home(request):
    #vista en progreso
    manga = Manga.objects.all()
    print(type(manga))

    value = request.GET.get('termino')

    if value:
        buscar = Manga.objects.filter(
            nombre_del_manga = value
        )
        
    else:
        return render(request, "home.html", {"mangas": manga})
    
def search(request):
    if request.method == "GET":
        manga = request.GET.get("manga")
        if manga:
            if len(manga) > 16:
                return HttpResponse("Error: El nombre es muy largo")
            else:
                manga_name = Manga.objects.filter(nombre_del_manga__icontains=manga)
                return render(request, 'search.html', {"manga_name": manga_name})
        else:
            return render(request, 'search.html', {})

#Vista y lógica realizada para poder buscar los mangas por parámetro de url (en prueba)
def manga_view(request):
    if request.method == "GET":
        manga = request
        manga = Manga.objects.filter(nombre_del_manga__contains=None)

    if manga.exists():
        mensaje = f"Mangas obtenido {None}"
    else:
        mensaje = f"Lamentablemente no se encontró el manga: {None}"

    return HttpResponse(mensaje)

def about(request):
    return render(request, "about.html")

def ingresar(request):
    return render(request, "login.html")

def watchlist(request):
    return HttpResponse("Watchlist")

def imdbpro(request):
    return render()

#pagina principal
def index(request):
    return render(request, "index.html", {})