from django.urls import path
from . import views
from webcomics.views import index


urlpatterns = [
    path("", index),
    path('home/', views.home, name="home"),
    path('surchaingmanga/', views.registrar_usuario, name='registrarse'),
    path("manga/<str:name>/", views.manga_view),
    path('watchlist/', views.watchlist, name='watchlist'),
    path('imdbpro/', views.imdbpro, name='imdbpro'),
    path("about/", views.about, name="about"),
]
