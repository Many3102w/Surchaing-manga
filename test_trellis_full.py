from gradio_client import Client, handle_file
import os

try:
    print("Connecting to TRELLIS...")
    client = Client("JeffreyXiang/TRELLIS")
    
    # Path to the sweatshirt image
    img_path = "C:/Users/Many/.gemini/antigravity/brain/e6b8b7a1-b6fa-4410-a279-5678ad5a47d1/uploaded_image_1767098220423.png"
    
    if not os.path.exists(img_path):
        print(f"Image not found: {img_path}")
        exit(1)

    print(f"1. Preprocessing image: {img_path}")
    preprocess_res = client.predict(image=handle_file(img_path), api_name="/preprocess_image")
    print(f"Preprocess result: {preprocess_res}")

    print("2. Generating 3D model (this may take a while)...")
    # predict(image, multiimages, seed, ss_guidance_strength, ss_sampling_steps, slat_guidance_strength, slat_sampling_steps, multiimage_algo, api_name="/image_to_3d") -> output_0
    image_to_3d_res = client.predict(
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
    print("3D generation done.")

    print("3. Extracting GLB...")
    # predict(mesh_simplify, texture_size, api_name="/extract_glb") -> (extracted_glb, download_glb)
    extract_res = client.predict(
        mesh_simplify=0.95,
        texture_size=1024,
        api_name="/extract_glb"
    )
    
    glb_path = extract_res[0]
    print(f"Success! GLB saved at: {glb_path}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
