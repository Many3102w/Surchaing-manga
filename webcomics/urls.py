from django.urls import path
from . import views
from webcomics.views import index

urlpatterns = [
    path("", index, name="index"),
    path('home/', views.home, name="home"),
    path('ingresar/', views.ingresar, name='ingresar'),
    path("manga_view/<str:name>/", views.manga_view),
    path("search/", views.search_manga, name='name'),
    path('watchlist/', views.watchlist, name='watchlist'),
    path("about/", views.about, name="about"),
]
