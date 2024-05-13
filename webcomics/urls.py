from django.urls import path
from . import views
from webcomics.views import index


urlpatterns = [
    path("", index),
    path('home/', views.home, name="home"),
    path("manga/<str:name>/", views.manga_view),
    path("about/", views.about, name="about")
]
