from django.urls import path
from . import views
from webcomics.views import index


urlpatterns = [
    path("index/", index),
    path("manga/", views.manga_view, name="manga"),
    path("about/", views.about, name="about")
]
