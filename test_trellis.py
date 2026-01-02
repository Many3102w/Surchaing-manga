from gradio_client import Client, handle_file
import time
import os

token = "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"
input_image_path = "media/front_pages/default_avatar_m8To3Yt.png"

def test_trellis():
    print("Testing Trellis 3D Generation with Token...")
    start_time = time.time()
    
    try:
        client = Client("JeffreyXiang/TRELLIS", token=token)
        
        # Step 1: Preprocess
        print("1. Preprocessing...")
        preprocess_res = client.predict(
            image=handle_file(input_image_path),
            api_name="/preprocess_image"
        )
        print(f"   Preprocess done: {preprocess_res}")

        # Step 2: Latents
        print("2. Generating Latents (This takes time)...")
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
        print("   Latents done.")

        # Step 3: Extract GLB
        print("3. Extracting GLB...")
        extract_res = client.predict(
            mesh_simplify=0.95,
            texture_size=1024,
            api_name="/extract_glb"
        )
        print(f"   Extract Result: {extract_res}")
        
        end_time = time.time()
        print(f"✅ Success! Total time: {end_time - start_time:.2f} seconds")

    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_trellis()
