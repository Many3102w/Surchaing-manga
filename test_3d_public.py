from gradio_client import Client
import os

print("Attempting to generate 3D mesh WITHOUT token...")
try:
    client = Client("stabilityai/stable-fast-3d")
    
    # Using /run_button
    # input_image, foreground_ratio, remesh_option, vertex_count, texture_size
    result = client.predict(
        input_image="media/front_pages/default_avatar_m8To3Yt.png", 
        foreground_ratio=0.85,
        remesh_option="None",
        vertex_count=-1,
        texture_size=1024,
        api_name="/run_button"
    )
    print("Result:", result)
except Exception as e:
    print("Error:", e)
