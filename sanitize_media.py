import os
import django
import shutil
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.models import Manga

def sanitize_filename(instance, field_name, prefix):
    field = getattr(instance, field_name)
    if not field:
        return False
        
    old_path = field.path
    old_name = os.path.basename(old_path)
    
    # Si el nombre es corto y seguro, no hacer nada
    if len(old_name) < 40 and " " not in old_name:
        return False
        
    ext = os.path.splitext(old_name)[1].lower()
    if not ext:
        ext = '.png' if 'depth' in prefix else '.jpg'
        
    # Crear nombre nuevo corto basado en ID o UUID si no hay ID
    new_name = f"{prefix}_{instance.id if instance.id else uuid.uuid4().hex[:8]}{ext}"
    relative_dir = os.path.dirname(field.name)
    new_relative_path = os.path.join(relative_dir, new_name)
    new_path = os.path.join(os.path.dirname(old_path), new_name)
    
    print(f"Renombrando: {old_name} -> {new_name}")
    
    try:
        if os.path.exists(old_path):
            shutil.move(old_path, new_path)
            field.name = new_relative_path
            return True
        else:
            print(f"  ⚠ Archivo no encontrado físicamente: {old_path}")
            return False
    except Exception as e:
        print(f"  ❌ Error al mover archivo: {e}")
        return False

def run_sanitization():
    mangas = Manga.objects.all()
    count = 0
    total = mangas.count()
    print(f"Iniciando sanitización de {total} mangas...")
    
    for manga in mangas:
        changed = False
        # Sanitizar portada
        if sanitize_filename(manga, 'front_page', 'front'):
            changed = True
        # Sanitizar depth map
        if sanitize_filename(manga, 'depth_map', 'depth'):
            changed = True
            
        if changed:
            manga.save()
            count += 1
            
    print(f"\n--- Resumen ---")
    print(f"Mangas actualizados: {count}")
    print(f"Proceso completado.")

if __name__ == "__main__":
    run_sanitization()
