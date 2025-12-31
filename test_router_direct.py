import requests

def test_router_direct_model():
    token = "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"
    model_id = "Intel/dpt-large"
    url = f"https://router.huggingface.co/hf-inference/{model_id}"
    
    test_image_path = 'C:/Users/Many/.gemini/antigravity/brain/e6b8b7a1-b6fa-4410-a279-5678ad5a47d1/test_manga_cover_1767092943383.png'
    with open(test_image_path, 'rb') as f:
        image_content = f.read()

    print(f"Testing router direct model at {url}...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(url, headers=headers, data=image_content, timeout=30)
        print(f"Status Code: {resp.status_code}")
        if resp.status_code == 200:
            print("✅ SUCCESS! Router direct model worked.")
        else:
            print(f"Response: {resp.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_router_direct_model()
