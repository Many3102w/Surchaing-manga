import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.models import Manga
from webcomics.utils import generate_3d_mesh

mangas = Manga.objects.filter(mesh_3d='')
print(f"Found {mangas.count()} mangas without 3D mesh.")

for manga in mangas:
    if manga.front_page:
        print(f"Generating 3D mesh for: {manga.nombre_del_manga} (ID: {manga.id})...")
        try:
            mesh_file = generate_3d_mesh(manga.front_page.file)
            if mesh_file:
                manga.mesh_3d.save(f'mesh_{manga.id}.glb', mesh_file, save=True)
                manga.is_3d_converted = True
                manga.save()
                print(f"Success for {manga.nombre_del_manga}")
            else:
                print(f"Failed to generate for {manga.nombre_del_manga}")
        except Exception as e:
            print(f"Error for {manga.nombre_del_manga}: {e}")
