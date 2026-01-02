import os
import django
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.models import Manga

def check_urls():
    print(f"{'ID':<5} | {'Nombre':<20} | {'URL'}")
    print("-" * 60)
    for manga in Manga.objects.filter(is_3d_converted=True)[:10]:
        url = manga.depth_map.url if manga.depth_map else "None"
        print(f"{manga.id:<5} | {manga.nombre_del_manga[:20]:<20} | {url}")

if __name__ == "__main__":
    check_urls()
