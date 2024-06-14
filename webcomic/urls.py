from django.contrib import admin
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('administrador/', admin.site.urls),
    path('', include("webcomics.urls"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
