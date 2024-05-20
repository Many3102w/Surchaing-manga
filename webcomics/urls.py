from django.urls import path
from . import views
from webcomics.views import index

urlpatterns = [
    path("", index),
    path('home/', views.home, name="home"),
    path('surchaingmanga/ingresar/', views.ingresar, name='ingresar'),
    path("surchaingmanga/manga_view/<str:name>/", views.manga_view),
    path("search/", views.search_manga, name='name'),
    path('surchaingmanga/watchlist/', views.watchlist, name='watchlist'),
    path('surchaingmannga/imdbpro/', views.imdbpro, name='imdbpro'),
    path("surchaingmanga/about/", views.about, name="about"),
]
