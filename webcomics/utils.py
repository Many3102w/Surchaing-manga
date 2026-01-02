import requests
from PIL import Image
from io import BytesIO
import os
import tempfile
import shutil
from django.core.files.base import ContentFile
from django.conf import settings
from gradio_client import Client, handle_file
import time


def generate_3d_mesh(image_file):
    """
    Generate a high-fidelity 3D GLB model using Trellis AI.
    This produces volumetric meshes that fill the shape perfectly.
    """
    try:
        # Save image to a temporary file
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img:
            image_file.seek(0)
            shutil.copyfileobj(image_file, temp_img)
            temp_img_path = temp_img.name

        print(f"Calling Trellis AI for high-fidelity 3D reconstruction...")
        token = getattr(settings, 'HUGGINGFACE_API_TOKEN', None)
        client = Client("JeffreyXiang/TRELLIS", token=token)
        
        # Step 1: Preprocess Image (Remove background, center, etc.)
        # predict(image, api_name="/preprocess_image") -> output_image_path
        preprocess_res = client.predict(
            image=handle_file(temp_img_path),
            api_name="/preprocess_image"
        )
        
        if not preprocess_res:
            print("Trellis Preprocess failed.")
            return None

        # Step 2: Image to 3D Latents
        # predict(image, multiimages, seed, ss_guidance_strength, ss_sampling_steps, slat_guidance_strength, slat_sampling_steps, multiimage_algo, api_name="/image_to_3d")
        print("Trellis: Generating 3D latents...")
        client.predict(
            image=handle_file(preprocess_res),
            multiimages=[],
            seed=0,
            ss_guidance_strength=7.5,
            ss_sampling_steps=12,
            slat_guidance_strength=3.0,
            slat_sampling_steps=12,
            multiimage_algo='stochastic',
            api_name="/image_to_3d"
        )

        # Step 3: Extract GLB
        # predict(mesh_simplify, texture_size, api_name="/extract_glb") -> (extracted_glb, download_glb)
        print("Trellis: Extracting aesthetic GLB...")
        extract_res = client.predict(
            mesh_simplify=0.95,
            texture_size=1024,
            api_name="/extract_glb"
        )
        
        if extract_res and len(extract_res) >= 1:
            glb_path = extract_res[0]
            if os.path.exists(glb_path):
                with open(glb_path, 'rb') as f:
                    content = ContentFile(f.read(), name='product_trellis_3d.glb')
                
                # Cleanup
                os.unlink(temp_img_path)
                print("✅ Trellis 3D Generation Successful.")
                return content
        
        return None
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "expired" in error_msg.lower():
            reason = "Hugging Face Token EXPIRED or INVALID"
        elif "quota" in error_msg.lower():
            reason = "ZeroGPU Daily Quota Exhausted"
        else:
            reason = f"Unhandled Error: {error_msg}"
            
        print(f"Error in Trellis generate_3d_mesh: {reason}")
        with open('DEBUG_ERROR.txt', 'a') as f:
            f.write(f"Trellis Error ({time.strftime('%Y-%m-%d %H:%M:%S')}): {reason}\n")
        return None


def generate_depth_map(image_file):
    """
    Generate a real depth map using Depth-Anything-V2 AI via Gradio Public Space.
    This provides true AI analysis of the garment shape.
    """
    try:
        # Save image to a temporary file for the API
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_img:
            image_file.seek(0)
            shutil.copyfileobj(image_file, temp_img)
            temp_img_path = temp_img.name

        print(f"Calling Depth-Anything-V2 AI for true analysis...")
        token = getattr(settings, 'HUGGINGFACE_API_TOKEN', None)
        client = Client("depth-anything/Depth-Anything-V2", token=token)
        
        # Predict: image
        # Returns: (depth_map_slider, grayscale_depth_map, 16bit_raw)
        result = client.predict(
            image=handle_file(temp_img_path),
            api_name="/on_submit"
        )
        
        # El resultado es una tupla, el mapa de grises es el segundo elemento
        if result and len(result) >= 2:
            grayscale_path = result[1]
            if os.path.exists(grayscale_path):
                with open(grayscale_path, 'rb') as f:
                    content = ContentFile(f.read(), name='depth_map_ai.png')
                
                # Cleanup
                os.unlink(temp_img_path)
                print("Successfully generated AI depth map.")
                return content
            
        return None
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "expired" in error_msg.lower():
            reason = "Hugging Face Token EXPIRED or INVALID"
        elif "quota" in error_msg.lower():
            reason = "ZeroGPU Daily Quota Exhausted"
        else:
            reason = f"Unhandled Error: {error_msg}"
            
        print(f"Error in generate_depth_map (AI): {reason}")
        with open('DEBUG_ERROR.txt', 'a') as f:
            f.write(f"Depth Error ({time.strftime('%Y-%m-%d %H:%M:%S')}): {reason}\n")
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
