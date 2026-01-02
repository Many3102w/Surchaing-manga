import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.models import Manga

# Get the latest manga
latest = Manga.objects.latest('id')

print(f"=== ÚLTIMO POST CREADO ===")
print(f"ID: {latest.id}")
print(f"Nombre: {latest.nombre_del_manga}")
print(f"Front page field: {latest.front_page}")
print(f"Front page name: {latest.front_page.name if latest.front_page else 'None'}")

if latest.front_page:
    print(f"Front page URL: {latest.front_page.url}")
    try:
        print(f"Front page path: {latest.front_page.path}")
        print(f"File exists: {os.path.exists(latest.front_page.path)}")
        if os.path.exists(latest.front_page.path):
            print(f"File size: {os.path.getsize(latest.front_page.path)} bytes")
    except Exception as e:
        print(f"Error checking file: {e}")
else:
    print("NO FRONT PAGE UPLOADED!")

print(f"\nDepth map: {latest.depth_map}")
print(f"Mesh 3D: {latest.mesh_3d}")
print(f"Is 3D converted: {latest.is_3d_converted}")
