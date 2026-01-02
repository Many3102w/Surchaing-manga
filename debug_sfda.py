import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.models import Manga

# Find the post "sfda"
try:
    sfda_post = Manga.objects.filter(nombre_del_manga__icontains='sfda').latest('id')
    
    print(f"=== POST 'sfda' ===")
    print(f"ID: {sfda_post.id}")
    print(f"Nombre: {sfda_post.nombre_del_manga}")
    print(f"Talla: {sfda_post.talla}")
    print(f"Precio: {sfda_post.precio}")
    
    print(f"\n--- IMAGEN PRINCIPAL ---")
    print(f"Front page field: {sfda_post.front_page}")
    print(f"Front page bool: {bool(sfda_post.front_page)}")
    
    if sfda_post.front_page:
        print(f"Front page name: {sfda_post.front_page.name}")
        print(f"Front page URL: {sfda_post.front_page.url}")
        try:
            print(f"Front page path: {sfda_post.front_page.path}")
            print(f"File exists: {os.path.exists(sfda_post.front_page.path)}")
            if os.path.exists(sfda_post.front_page.path):
                print(f"File size: {os.path.getsize(sfda_post.front_page.path)} bytes")
        except Exception as e:
            print(f"Error checking file: {e}")
    else:
        print("❌ NO FRONT PAGE UPLOADED!")
    
    print(f"\n--- DATOS 3D ---")
    print(f"Depth map: {sfda_post.depth_map}")
    print(f"Depth map bool: {bool(sfda_post.depth_map)}")
    
    if sfda_post.depth_map:
        print(f"Depth map URL: {sfda_post.depth_map.url}")
        try:
            print(f"Depth map path: {sfda_post.depth_map.path}")
            print(f"Depth file exists: {os.path.exists(sfda_post.depth_map.path)}")
        except Exception as e:
            print(f"Error checking depth file: {e}")
    
    print(f"\nMesh 3D: {sfda_post.mesh_3d}")
    print(f"Is 3D converted: {sfda_post.is_3d_converted}")
    
except Manga.DoesNotExist:
    print("❌ No se encontró ningún post con 'sfda' en el nombre")
except Exception as e:
    print(f"❌ Error: {e}")
