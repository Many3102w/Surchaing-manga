import os
import django
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.models import Manga
from webcomics.utils import generate_depth_map, generate_3d_mesh

def fix_specific_item():
    target_price = 111.00
    try:
        manga = Manga.objects.filter(precio=target_price).first()
        if not manga:
            print("❌ No se encontró el manga con precio 111.00")
            return

        print(f"🎯 Objetivo encontrado: {manga.nombre_del_manga} (ID: {manga.id})")
        print(f"   - Front Page: {manga.front_page.path if manga.front_page else 'MISSING'}")
        
        # Force Depth Map Generation
        print("   ⏳ Intentando generar Depth Map...")
        depth_content = generate_depth_map(manga.front_page.file)
        if depth_content:
            manga.depth_map.save(f'depth_{manga.id}.png', depth_content, save=False)
            print("   ✅ Depth Map generado con éxito.")
        else:
            print("   ❌ FALLÓ la generación de Depth Map.")

        # Force GLB Generation
        print("   ⏳ Intentando generar GLB (Trellis)...")
        mesh_content = generate_3d_mesh(manga.front_page.file)
        if mesh_content:
            manga.mesh_3d.save(f'mesh_{manga.id}.glb', mesh_content, save=False)
            print("   ✅ GLB generado con éxito.")
        else:
            print("   ❌ FALLÓ la generación de GLB.")

        manga.is_3d_converted = True
        manga.save()
        print("💾 Guardado item en BD.")

    except Exception as e:
        print(f"🔥 EXCEPCIÓN: {e}")

if __name__ == "__main__":
    fix_specific_item()
