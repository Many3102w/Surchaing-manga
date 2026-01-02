import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.models import Manga

# Find the post named "fda"
try:
    fda_post = Manga.objects.filter(nombre_del_manga__icontains='fda').latest('id')
    
    print(f"=== POST 'fda' ===")
    print(f"ID: {fda_post.id}")
    print(f"Nombre: {fda_post.nombre_del_manga}")
    print(f"Front page field: {fda_post.front_page}")
    print(f"Front page name: {fda_post.front_page.name if fda_post.front_page else 'None'}")
    
    if fda_post.front_page:
        print(f"Front page URL: {fda_post.front_page.url}")
        try:
            print(f"Front page path: {fda_post.front_page.path}")
            print(f"File exists: {os.path.exists(fda_post.front_page.path)}")
            if os.path.exists(fda_post.front_page.path):
                print(f"File size: {os.path.getsize(fda_post.front_page.path)} bytes")
        except Exception as e:
            print(f"Error checking file: {e}")
    else:
        print("❌ NO FRONT PAGE UPLOADED!")
    
    print(f"\nDepth map: {fda_post.depth_map}")
    print(f"Mesh 3D: {fda_post.mesh_3d}")
    print(f"Is 3D converted: {fda_post.is_3d_converted}")
    
except Manga.DoesNotExist:
    print("No se encontró ningún post con 'fda' en el nombre")
