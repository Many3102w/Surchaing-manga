import requests

def test_router_vision():
    token = "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"
    model_id = "google/vit-base-patch16-224"
    # Testing several likely router paths
    paths = [
        f"https://router.huggingface.co/hf-inference/models/{model_id}",
        f"https://router.huggingface.co/hf-inference/{model_id}",
        f"https://router.huggingface.co/v1/models/{model_id}",
        f"https://router.huggingface.co/{model_id}"
    ]
    
    test_image_path = 'C:/Users/Many/.gemini/antigravity/brain/e6b8b7a1-b6fa-4410-a279-5678ad5a47d1/test_manga_cover_1767092943383.png'
    with open(test_image_path, 'rb') as f:
        image_content = f.read()

    headers = {"Authorization": f"Bearer {token}"}
    
    for url in paths:
        print(f"--- Testing Vision Model at {url} ---")
        try:
            resp = requests.post(url, headers=headers, data=image_content, timeout=20)
            print(f"Status Code: {resp.status_code}")
            if resp.status_code == 200:
                print("✅ SUCCESS! This URL works for vision.")
                return
            else:
                print(f"Response: {resp.text[:200]}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_router_vision()
