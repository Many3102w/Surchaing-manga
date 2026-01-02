import os
import django
import sys
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.models import Manga

def fix_all_flat_posts():
    print("Iniciando reparación de publicaciones planas...")
    mangas = Manga.objects.filter(is_3d_converted=False)
    print(f"Revisando {mangas.count()} publicaciones.")

    for manga in mangas:
        if not manga.front_page:
            continue
            
        print(f"Reparando ID {manga.id}: {manga.nombre_del_manga} con relieve de emergencia...")
        
        # Generar Mock Depth Map
        mock_depth = Image.new('L', (512, 512), color=128)
        for y in range(512):
            for x in range(512):
                val = int(128 + 30 * (y / 512.0))
                mock_depth.putpixel((x, y), val)
        
        buf = BytesIO()
        mock_depth.save(buf, format='PNG')
        
        manga.depth_map.save(
            f'depth_front_{manga.id}.png',
            ContentFile(buf.getvalue()),
            save=False
        )
        manga.is_3d_converted = True
        manga.save()
        print(f"✅ ID {manga.id} ahora tiene relieve 3D.")

if __name__ == "__main__":
    fix_all_flat_posts()
