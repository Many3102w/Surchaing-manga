from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Manga, Like, Comment, Favorite
from .forms import MangaForm, CommentForm

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


class LoginView(TemplateView):
    template_name = "login.html"


class AboutView(TemplateView):
    template_name = "about.html"


class IngresarView(TemplateView):
    template_name = "login.html"


class LibraryView(TemplateView):
    template_name = "library.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # We rely on context processor for mangas, but we can add forms here
        context['comment_form'] = CommentForm()
        return context

class CreatePostView(UserPassesTestMixin, CreateView):
    model = Manga
    form_class = MangaForm
    template_name = "create_post.html"
    success_url = reverse_lazy('library')

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.fecha_de_carga = timezone.now()
        # Calificacion default 0
        return super().form_valid(form)

@login_required
def delete_post(request, manga_id):
    if not request.user.is_superuser:
        return redirect('library')
    
    manga = get_object_or_404(Manga, id=manga_id)
    manga.delete()
    return redirect('library')

@login_required
def toggle_favorite(request, manga_id):
    if request.method == 'POST':
        manga = get_object_or_404(Manga, id=manga_id)
        fav, created = Favorite.objects.get_or_create(user=request.user, manga=manga)
        if not created:
            fav.delete()
            favorited = False
        else:
            favorited = True
        return JsonResponse({'favorited': favorited})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def like_manga(request, manga_id):
    if request.method == 'POST':
        manga = get_object_or_404(Manga, id=manga_id)
        like, created = Like.objects.get_or_create(user=request.user, manga=manga)
        if not created:
            like.delete()
            liked = False
        else:
            liked = True
        return JsonResponse({'liked': liked, 'count': manga.likes.count()})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def add_comment(request, manga_id):
    if request.method == 'POST':
        manga = get_object_or_404(Manga, id=manga_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.manga = manga
            comment.save()
            return redirect('library') # Or return JSON for AJAX
    return redirect('library')

class HelpView(TemplateView):
    template_name = "help.html"

from django.db.models import Q

class TeamView(TemplateView):
    template_name = "team.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all active users and prefetch profile to avoid N+1
        # We use prefetch_related because 'profile' is a reverse OneToOne relation,
        # although select_related is supported for reverse OneToOne, prefetch in this case is safer if structure varies.
        # Actually, let's just use select_related if sure, but prefetch is safer for avoiding join filtering issues.
        # Wait, simple approach: Fetch all users, filter in python.
        users = User.objects.filter(is_active=True).select_related('profile')
        
        members_data = []
        for user in users:
            # Determine if user should be shown
            # Show if Superuser OR (has profile AND has role)
            has_profile = hasattr(user, 'profile')
            has_role = has_profile and user.profile.role
            
            if not user.is_superuser and not has_role:
                continue

            # Prepare data
            role = "Miembro"
            country = ""
            avatar_url = None

            if has_profile:
                profile = user.profile
                if profile.avatar:
                    avatar_url = profile.avatar.url
                if profile.role:
                    role = profile.role
                if profile.country:
                    country = profile.country
            
            # Fallback for superuser with no role
            if user.is_superuser and not has_role:
                role = "Superuser"

            members_data.append({
                'username': user.username,
                'avatar_url': avatar_url,
                'role': role,
                'country': country
            })
        
        context['team_members'] = members_data
        return context

class IndexView(TemplateView):
    template_name = "index.html"


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


class LoginView(TemplateView):
    template_name = "login.html"


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
