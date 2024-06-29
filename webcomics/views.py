from django.shortcuts import render
from django.views.generic import TemplateView
from webcomics.models import Manga

class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mangas'] = Manga.objects.all()
        return context


class SearchView(TemplateView):
    template_name = "search.html"

    def get(self, request, *args, **kwargs):
        manga = request.GET.get("manga")
        if manga:
            if len(manga) > 16:
                return HttpResponse("Error: El nombre es muy largo")
            else:
                manga_name = Manga.objects.filter(nombre_del_manga__icontains=manga)
                return render(request, self.template_name, {"manga_name": manga_name})
        return render(request, self.template_name, {})


class MangaView(TemplateView):
    template_name = "manga.html"

    def get(self, request, *args, **kwargs):
        manga_name = kwargs.get('name')
        manga = Manga.objects.filter(nombre_del_manga__icontains=manga_name)
        if manga.exists():
            mensaje = f"Mangas obtenido {manga_name}"
        else:
            mensaje = f"Lamentablemente no se encontró el manga: {manga_name}"
        return HttpResponse(mensaje)


class AboutView(TemplateView):
    template_name = "about.html"


class IngresarView(TemplateView):
    template_name = "login.html"


class LibraryView(TemplateView):
    template_name = "library.html"

class HelpView(TemplateView):
    template_name = "help.html"

class TeamView(TemplateView):
    template_name = "team.html"

class IndexView(TemplateView):
    template_name = "index.html"
