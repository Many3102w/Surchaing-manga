import requests

def test_router_full_headers():
    token = "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"
    model_id = "Intel/dpt-large"
    url = "https://router.huggingface.co/hf-inference"
    
    test_image_path = 'C:/Users/Many/.gemini/antigravity/brain/e6b8b7a1-b6fa-4410-a279-5678ad5a47d1/test_manga_cover_1767092943383.png'
    with open(test_image_path, 'rb') as f:
        image_content = f.read()

    print(f"Testing router at {url} with Full Headers...")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Model-Id": model_id,
            "X-Inference-Task": "depth-estimation",
            "Content-Type": "application/octet-stream"
        }
        resp = requests.post(url, headers=headers, data=image_content, timeout=30)
        print(f"Status Code: {resp.status_code}")
        if resp.status_code == 200:
            print("✅ SUCCESS! Full headers worked.")
        else:
            print(f"Response: {resp.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_router_full_headers()
