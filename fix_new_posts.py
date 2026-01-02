import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.models import Manga
from webcomics.utils import generate_depth_map, generate_3d_mesh

# Find posts without depth_map
posts_without_depth = Manga.objects.filter(front_page__isnull=False, depth_map='')

print(f"Encontrados {posts_without_depth.count()} posts sin depth map")

for manga in posts_without_depth:
    print(f"\n=== Procesando: {manga.nombre_del_manga} (ID: {manga.id}) ===")
    
    try:
        # Check if file exists
        if not os.path.exists(manga.front_page.path):
            print(f"❌ Archivo no existe: {manga.front_page.path}")
            continue
            
        print(f"✓ Archivo existe: {manga.front_page.name}")
        
        # Generate depth map
        print("Generando depth map...")
        depth_map_file = generate_depth_map(manga.front_page.file)
        
        if depth_map_file:
            manga.depth_map.save(
                f'depth_front_{manga.id}.png',
                depth_map_file,
                save=False
            )
            print(f"✓ Depth map generado")
        else:
            print(f"❌ Falló generación de depth map")
            
        # Try to generate 3D mesh
        print("Generando mesh 3D...")
        try:
            mesh_file = generate_3d_mesh(manga.front_page.file)
            if mesh_file:
                manga.mesh_3d.save(
                    f'mesh_front_{manga.id}.glb',
                    mesh_file,
                    save=False
                )
                print(f"✓ Mesh 3D generado")
        except Exception as e:
            print(f"⚠ Mesh 3D falló (normal si no hay token): {e}")
        
        # Mark as converted if we got at least depth map
        if manga.depth_map:
            manga.is_3d_converted = True
            
        manga.save()
        print(f"✓ Post actualizado")
        
    except Exception as e:
        print(f"❌ Error procesando {manga.id}: {e}")

print("\n=== PROCESO COMPLETADO ===")
