import requests

def test_legacy_with_accept():
    token = "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"
    model_id = "Intel/dpt-large"
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    
    test_image_path = 'C:/Users/Many/.gemini/antigravity/brain/e6b8b7a1-b6fa-4410-a279-5678ad5a47d1/test_manga_cover_1767092943383.png'
    with open(test_image_path, 'rb') as f:
        image_content = f.read()

    print(f"Testing legacy endpoint at {url} with Accept: image/png...")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "image/png"
        }
        resp = requests.post(url, headers=headers, data=image_content, timeout=30)
        print(f"Status Code: {resp.status_code}")
        if resp.status_code == 200:
            print("✅ SUCCESS! Accept header fixed the 410 error.")
        else:
            print(f"Response: {resp.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_legacy_with_accept()
