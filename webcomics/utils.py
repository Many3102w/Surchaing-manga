import requests
from PIL import Image
from io import BytesIO
import os
import tempfile
import shutil
from django.core.files.base import ContentFile
from django.conf import settings
from transformers import pipeline
from gradio_client import Client
import time


# Initialize the depth estimation pipeline (loaded once)
_depth_estimator = None

def get_depth_estimator():
    """Lazy-load the depth estimation model."""
    global _depth_estimator
    if _depth_estimator is None:
        print("Loading depth estimation model...")
        _depth_estimator = pipeline(
            "depth-estimation",
            model="LiheYoung/depth-anything-small-hf",  # Using small model for faster loading
        )
        print("Model loaded successfully!")
    return _depth_estimator


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
        import traceback
        traceback.print_exc()
        return None


def generate_depth_map(image_file):
    """
    Generate a depth map from a 2D image using local Hugging Face model.
    No API calls needed - runs entirely on the server.
    """
    try:
        # Read image data
        image_file.seek(0)
        image = Image.open(image_file)
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        print(f"Generating depth map for image of size {image.size}...")
        
        # Get the depth estimator
        depth_estimator = get_depth_estimator()
        
        # Generate depth map
        result = depth_estimator(image)
        depth_map_image = result["depth"]
        
        # Convert to RGB for saving
        if depth_map_image.mode != 'RGB':
            depth_map_image = depth_map_image.convert('RGB')
        
        # Save to BytesIO
        output = BytesIO()
        depth_map_image.save(output, format='PNG')
        output.seek(0)
        
        print("Successfully generated depth map locally.")
        return ContentFile(output.read(), name='depth_map.png')
            
    except Exception as e:
        print(f"Error in generate_depth_map: {e}")
        import traceback
        traceback.print_exc()
        return None


def create_3d_effect_data(original_image_path, depth_map_path):
    """
    Create metadata for 3D effect rendering.
    Returns a dict with paths and settings for frontend 3D display.
    
    Args:
        original_image_path: Path to the original image
        depth_map_path: Path to the depth map image
        
    Returns:
        dict with 3D effect configuration
    """
    return {
        'original': original_image_path,
        'depth_map': depth_map_path,
        'parallax_strength': 0.3,  # Adjustable parallax effect strength
        'depth_scale': 1.0  # Adjustable depth scale
    }
