import requests

def test_router_final_guess():
    token = "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"
    # Try several modern depth models
    models = [
        "LiheYoung/depth-anything-small-hf",
        "Intel/dpt-large",
        "LiheYoung/depth-anything-base-hf"
    ]
    
    test_image_path = 'C:/Users/Many/.gemini/antigravity/brain/e6b8b7a1-b6fa-4410-a279-5678ad5a47d1/test_manga_cover_1767092943383.png'
    with open(test_image_path, 'rb') as f:
        image_content = f.read()

    for model_id in models:
        url = f"https://router.huggingface.co/hf-inference/models/{model_id}"
        print(f"--- Testing {model_id} at {url} ---")
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/octet-stream",
                "X-Wait-For-Model": "true"
            }
            resp = requests.post(url, headers=headers, data=image_content, timeout=40)
            print(f"Status Code: {resp.status_code}")
            if resp.status_code == 200:
                print(f"✅ SUCCESS! {model_id} works on the router.")
                with open(f"depth_result_{model_id.replace('/', '_')}.png", 'wb') as out:
                    out.write(resp.content)
                return
            else:
                print(f"Response: {resp.text[:200]}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_router_final_guess()
