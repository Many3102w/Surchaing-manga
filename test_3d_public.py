from gradio_client import Client, handle_file
import os

print("Attempting to generate 3D mesh WITHOUT token...")
try:
    import time
    start_time = time.time()
    # Use the validated token
    token = "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"
    # FIXED: Argument is 'token', not 'hf_token'
    client = Client("stabilityai/stable-fast-3d", token=token)
    
    print("Testing 3D generation with Token...")
    # input_image, foreground_ratio, remesh_option, vertex_count, texture_size
    result = client.predict(
        input_image=handle_file("media/front_pages/default_avatar_m8To3Yt.png"), 
        foreground_ratio=0.85,
        remesh_option="None",
        vertex_count=-1,
        texture_size=1024,
        api_name="/run_button"
    )
    end_time = time.time()
    print(f"Result: {result}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
except Exception as e:
    print("Error:", e)
