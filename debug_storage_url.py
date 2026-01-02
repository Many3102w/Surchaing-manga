import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from django.core.files.storage import default_storage
from webcomics.models import Manga

print(f"DEFAULT_FILE_STORAGE: {settings.DEFAULT_FILE_STORAGE}")
print(f"Storage Class: {default_storage.__class__.__name__}")

# Check CLOUDINARY_STORAGE setting
print(f"CLOUDINARY_STORAGE setting: {getattr(settings, 'CLOUDINARY_STORAGE', 'Not Set')}")

# Try to generate a URL for a dummy file
name = 'front_pages/test_image.png'
url = default_storage.url(name)
print(f"Generated URL for '{name}': {url}")

# Check the last manga URL
last_manga = Manga.objects.last()
if last_manga and last_manga.front_page:
    print(f"Last Manga ID: {last_manga.id}")
    print(f"Last Manga Image Field: {last_manga.front_page}")
    print(f"Last Manga Image URL: {last_manga.front_page.url}")
    print(f"Last Manga Image Path: {last_manga.front_page.path if hasattr(last_manga.front_page, 'path') else 'No Path'}")
else:
    print("No manga with front_page found.")
