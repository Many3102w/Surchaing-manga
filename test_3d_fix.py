from gradio_client import Client, handle_file
import os

print("Testing StableFast3D with handle_file...")
try:
    client = Client("stabilityai/stable-fast-3d")
    
    # Use a real image from the media folder
    img_path = "media/front_pages/default_avatar_m8To3Yt.png"
    
    result = client.predict(
        input_image=handle_file(img_path),
        foreground_ratio=0.85,
        remesh_option="None",
        vertex_count=-1,
        texture_size=1024,
        api_name="/run_button"
    )
    print("Result:", result)
except Exception as e:
    print("Error:", e)
