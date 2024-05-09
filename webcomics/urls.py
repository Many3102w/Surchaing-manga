from django.urls import path
from . import views

urlpatterns = [
    path("home/", views.home),
    path("manga/", views.manga_view, name="manga"),
    path("about/", views.about, name="about")
]
