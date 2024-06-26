from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from webcomics.models import Manga
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    manga = Manga.objects.all()[0:9]

    value = request.GET.get('termino')

    if value:
        buscar = Manga.objects.filter(
            nombre_del_manga = value
        )
        return render(request, "home.html", {"post": buscar})
    else:
        return render(request, "home.html", {"mangas": manga})

def manga_view(request):
    return HttpResponse("manga")

def about(request):
    return HttpResponse("Sobre surchaing manga")