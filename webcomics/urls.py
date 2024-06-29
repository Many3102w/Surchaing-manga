from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path('home/', HomeView.as_view(), name="home"),
    path('ingresar/', IngresarView.as_view(), name='ingresar'),
    path("manga_view/<str:name>/", MangaView.as_view(), name='manga_view'),
    path("library/", LibraryView.as_view(), name='library'),
    path("team/", TeamView.as_view(), name='team'),
    path("help/", HelpView.as_view(), name='help'),
    path("search/", SearchView.as_view(), name='search'),
    path("about/", AboutView.as_view(), name="about"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
