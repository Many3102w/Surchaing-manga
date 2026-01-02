import os
import django
import sys
import requests
import time
from django.core.files.base import ContentFile

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.models import Manga
from django.conf import settings

def regenerate_missing_3d():
    print("Iniciando regeneración de 3D para publicaciones fallidas...")
    api_url = settings.HUGGINGFACE_API_URL
    api_token = settings.HUGGINGFACE_API_TOKEN
    
    if not api_token or 'rtnn' in api_token: # Check if it's still the old/expired token
        print("ERROR: Primero debes configurar tu nuevo token en HUGGINGFACE_API_TOKEN.")
        return

    mangas = Manga.objects.filter(is_3d_converted=False)
    print(f"Encontrados {mangas.count()} mangas sin 3D.")

    for manga in mangas:
        if not manga.front_page:
            continue
            
        print(f"Procesando ID {manga.id}: {manga.nombre_del_manga}...")
        try:
            with open(manga.front_page.path, 'rb') as f:
                image_data = f.read()
            
            headers = {"Authorization": f"Bearer {api_token}"}
            response = requests.post(api_url, headers=headers, data=image_data, timeout=30)
            
            if response.status_code == 200:
                manga.depth_map.save(f'depth_front_{manga.id}.png', ContentFile(response.content), save=False)
                manga.is_3d_converted = True
                manga.save()
                print(f"✅ 3D generado con éxito para {manga.nombre_del_manga}")
            elif response.status_code == 401:
                print("❌ ERROR: El token sigue siendo inválido (401).")
                break
            else:
                print(f"❌ Fallo en API: {response.status_code}")
        except Exception as e:
            print(f"❌ Error procesando {manga.nombre_del_manga}: {e}")
        
        time.sleep(1) # Breath

if __name__ == "__main__":
    regenerate_missing_3d()
