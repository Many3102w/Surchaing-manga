from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from webcomics.views import index

urlpatterns = [
    path("", index, name="index"),
    path('home/', views.home, name="home"),
    path('ingresar/', views.ingresar, name='ingresar'),
    path("manga_view/<str:name>/", views.manga_view),
    path("search/", views.search, name='search'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path("about/", views.about, name="about"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
