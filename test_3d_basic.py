from gradio_client import Client, handle_file
import os

try:
    print("Connecting to StableFast3D...")
    client = Client("stabilityai/stable-fast-3d")
    
    # Path to the sweatshirt image
    img_path = "C:/Users/Many/.gemini/antigravity/brain/e6b8b7a1-b6fa-4410-a279-5678ad5a47d1/uploaded_image_1767098220423.png"
    
    print(f"Generating 3D model for: {img_path}")
    result = client.predict(
        input_image=handle_file(img_path),
        api_name="/run_button"
    )
    
    print(f"Success! Result: {result}")

except Exception as e:
    print(f"Error: {e}")
