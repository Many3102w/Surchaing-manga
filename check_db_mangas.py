import os
import django
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.models import Manga

def check_mangas():
    print(f"{'ID':<5} | {'Nombre':<20} | {'3D?':<5} | {'Depth Map Path'}")
    print("-" * 60)
    for manga in Manga.objects.all()[:10]:
        depth_path = manga.depth_map.path if manga.depth_map else "None"
        exists = os.path.exists(depth_path) if manga.depth_map else False
        print(f"{manga.id:<5} | {manga.nombre_del_manga[:20]:<20} | {manga.is_3d_converted:<5} | {depth_path} (Exists: {exists})")

if __name__ == "__main__":
    check_mangas()
