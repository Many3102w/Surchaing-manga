from django.urls import path
from . import views

urlpatterns = [
    path("surchaing_manga/home/", views.home),
    path("manga/", views.manga_view, name="manga"),
    path("surchaing_manga/about", views.about, name="about")
]