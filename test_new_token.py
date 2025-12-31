import os
import django
import sys
from django.core.files.uploadedfile import SimpleUploadedFile

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

from webcomics.utils import generate_depth_map
from django.conf import settings

def test_new_token():
    print(f"Testing with NEW TOKEN: {settings.HUGGINGFACE_API_TOKEN[:20]}...")
    print(f"Model: {settings.HUGGINGFACE_DEPTH_MODEL}")
    print(f"URL: {settings.HUGGINGFACE_API_URL}")
    
    test_image_path = 'C:/Users/Many/.gemini/antigravity/brain/e6b8b7a1-b6fa-4410-a279-5678ad5a47d1/test_manga_cover_1767092943383.png'
    
    if not os.path.exists(test_image_path):
        print(f"Test image not found at {test_image_path}")
        return

    with open(test_image_path, 'rb') as f:
        image_content = f.read()
        uploaded_file = SimpleUploadedFile("test.png", image_content, content_type="image/png")
        
        print("\nCalling generate_depth_map...")
        result = generate_depth_map(uploaded_file)
        
        if result:
            print("✅ ✅ ✅ SUCCESS! Depth map generated with new token!")
            with open('depth_map_SUCCESS.png', 'wb') as out:
                out.write(result.read())
            print("Depth map saved to depth_map_SUCCESS.png")
        else:
            print("❌ Still failed. Check console logs above.")

if __name__ == "__main__":
    test_new_token()
