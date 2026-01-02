import requests
from PIL import Image
from io import BytesIO
import os
import tempfile
import shutil
from django.core.files.base import ContentFile
from django.conf import settings
from gradio_client import Client
import time


def generate_3d_mesh(image_file):
    """
    Generate a 3D GLB model from an image using StableFast3D AI via Gradio API.
    """
    try:
        # Save image to a temporary file for the API
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img:
            image_file.seek(0)
            shutil.copyfileobj(image_file, temp_img)
            temp_img_path = temp_img.name

        print(f"Calling StableFast3D AI for image: {temp_img_path}")
        client = Client("stabilityai/stable-fast-3d")
        
        # Predict: input_image, foreground_ratio=0.85, remesh_option='None', vertex_count=-1, texture_size=1024
        result = client.predict(
            input_image={"path": temp_img_path},
            foreground_ratio=0.85,
            remesh_option="None",
            vertex_count=-1,
            texture_size=1024,
            api_name="/run_button"
        )
        
        # Result is (preview_image, glb_path)
        if result and len(result) >= 2:
            glb_path = result[1]
            if os.path.exists(glb_path):
                with open(glb_path, 'rb') as f:
                    content = ContentFile(f.read(), name='product_3d.glb')
                
                # Cleanup
                os.unlink(temp_img_path)
                return content
        
        return None
    except Exception as e:
        print(f"Error in generate_3d_mesh: {e}")
        return None


def generate_depth_map(image_file):
    """
    Generate a depth map from a 2D image using Hugging Face API.
    Calls external API instead of running locally to save memory/space.
    """
    try:
        # Get settings
        api_url = getattr(settings, 'HUGGINGFACE_API_URL', 'https://api-inference.huggingface.co/models/LiheYoung/depth-anything-small-hf')
        api_token = getattr(settings, 'HUGGINGFACE_API_TOKEN', None)
        
        if not api_token:
            print("No Hugging Face token found, skipping depth map.")
            return None

        # Read image data
        image_file.seek(0)
        image_data = image_file.read()
        
        print(f"Calling Hugging Face API for depth map...")
        headers = {"Authorization": f"Bearer {api_token}"}
        
        # Retry logic if model is loading
        for i in range(3):
            response = requests.post(api_url, headers=headers, data=image_data, timeout=20)
            if response.status_code == 200:
                print("Successfully generated depth map via API.")
                return ContentFile(response.content, name='depth_map.png')
        print(f"La API de IA falló o no hay token. Generando relieve de emergencia (Mock)...")
        # Generate a simple gradient depth map as fallback
        mock_depth = Image.new('L', (512, 512), color=128)
        # Add some variation so it's not totally flat
        for y in range(512):
            for x in range(512):
                val = int(128 + 30 * (y / 512.0))
                mock_depth.putpixel((x, y), val)
        
        buf = BytesIO()
        mock_depth.save(buf, format='PNG')
        return ContentFile(buf.getvalue(), name='depth_map_fallback.png')
            
    except Exception as e:
        print(f"Error in generate_depth_map (API): {e}")
        return None


def create_3d_effect_data(original_image_path, depth_map_path):
    """
    Create metadata for 3D effect rendering.
    """
    return {
        'original': original_image_path,
        'depth_map': depth_map_path,
        'parallax_strength': 0.3,
        'depth_scale': 1.0
    }
