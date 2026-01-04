from PIL import Image
import os

def convert_to_png(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return
    
    try:
        img = Image.open(file_path)
        # Force conversion to RGB then save as PNG
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGBA')
        else:
            img = img.convert('RGB')
        
        # Save to a temporary name first
        temp_path = file_path + ".temp"
        img.save(temp_path, "PNG")
        
        # Replace original
        os.remove(file_path)
        os.rename(temp_path, file_path)
        print(f"Successfully converted {file_path} to PNG.")
    except Exception as e:
        print(f"Error converting {file_path}: {e}")

assets_dir = r"c:\Users\Many\Desktop\Surchaing-Admin\Surchaing-manga\mobile_app\assets"
convert_to_png(os.path.join(assets_dir, "icon.png"))
convert_to_png(os.path.join(assets_dir, "splash.png"))
