from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
    IndexView, HomeView, IngresarView, LibraryView, TeamView,
    SearchView, AboutView, LoginView, CreatePostView, like_manga,
    toggle_favorite, add_comment, delete_post, toggle_vendido,
    update_warehouse, SuperUserDashboardView
)
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('toggle_vendido/<int:manga_id>/', toggle_vendido, name='vendido_toggle'),
    path("", IndexView.as_view(), name="index"),
    path('home/', HomeView.as_view(), name="home"),
    path('ingresar/', IngresarView.as_view(), name='ingresar'),

    path("library/", LibraryView.as_view(), name='library'),
    path("team/", TeamView.as_view(), name='team'),

    path("search/", SearchView.as_view(), name='search'),
    path("about/", AboutView.as_view(), name="about"),
    path('login/', LoginView.as_view(), name='login'),
    
    # Social Features
    path('create_post/', CreatePostView.as_view(), name='create_post'),
    path('like/<int:manga_id>/', like_manga, name='like_manga'),
    path('favorite/<int:manga_id>/', toggle_favorite, name='toggle_favorite'),
    path('comment/<int:manga_id>/', add_comment, name='add_comment'),
    path('delete_post/<int:manga_id>/', delete_post, name='delete_post'),
    path('update_warehouse/', update_warehouse, name='update_warehouse'),
    path('superuser/', SuperUserDashboardView.as_view(), name='superuser_dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
