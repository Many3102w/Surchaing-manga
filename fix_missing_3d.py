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

from webcomics.utils import generate_depth_map, generate_3d_mesh

def fix_all_flat_posts():
    print("Iniciando generación MASIVA de 3D REAL (Trellis AI)...")
    mangas = Manga.objects.all()
    print(f"Procesando {mangas.count()} prendas para conversión 3D...")

    for manga in mangas:
        if not manga.front_page or not os.path.exists(manga.front_page.path):
            print(f"⚠️ Saltando ID {manga.id}: Archivo no encontrado.")
            continue
            
        print(f"🚀 Procesando ID {manga.id}: {manga.nombre_del_manga}...")
        
        # 1. Depth Map (Base Analysis)
        try:
            depth_map_file = generate_depth_map(manga.front_page.file)
            if depth_map_file:
                manga.depth_map.save(
                    f'depth_front_{manga.id}.png',
                    depth_map_file,
                    save=False
                )
        except Exception as e:
            print(f"❌ Error Depth Map ID {manga.id}: {e}")

        # 2. 3D GLB Model (Trellis AI - High Fidelity)
        try:
            print("   ⏳ Generando malla 3D de alta fidelidad...")
            if not manga.mesh_3d: # Only if missing or forced
                mesh_file = generate_3d_mesh(manga.front_page.file)
                if mesh_file:
                    manga.mesh_3d.save(
                        f'mesh_trellis_{manga.id}.glb',
                        mesh_file,
                        save=False
                    )
                    print("   ✅ GLB Generado.")
                else:
                    print("   ⚠️ Falló generación de GLB (Trellis API ocupada?)")
        except Exception as e:
            print(f"   ❌ Error 3D Mesh ID {manga.id}: {e}")

        manga.is_3d_converted = True
        manga.save()
        print(f"✨ ID {manga.id} actualizado.")

if __name__ == "__main__":
    fix_all_flat_posts()
