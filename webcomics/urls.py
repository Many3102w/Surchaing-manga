from django.urls import path
from . import views
from webcomics.views import index


urlpatterns = [
<<<<<<< HEAD
    path("index/", index),
=======
    path('', views.home, name="home"),
>>>>>>> 1fc108e64255ec14183d872d32a8f438e1402d67
    path("manga/", views.manga_view, name="manga"),
    path("about/", views.about, name="about")
]
