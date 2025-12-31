import requests
import os

def test_variations():
    token = "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"
    model_id = "Intel/dpt-large"
    
    variations = [
        f"https://huggingface.co/api/inference/models/{model_id}",
        f"https://api-inference.huggingface.co/v1/models/{model_id}",
        f"https://api.huggingface.co/inference/models/{model_id}",
        f"https://router.huggingface.co/inference/models/{model_id}",
        f"https://router.huggingface.co/api/models/{model_id}",
        f"https://huggingface.co/api/models/{model_id}/inference",
    ]
    
    test_image_path = 'C:/Users/Many/.gemini/antigravity/brain/e6b8b7a1-b6fa-4410-a279-5678ad5a47d1/test_manga_cover_1767092943383.png'
    with open(test_image_path, 'rb') as f:
        image_content = f.read()

    headers = {"Authorization": f"Bearer {token}"}
    
    for url in variations:
        print(f"--- Testing Variation: {url} ---")
        try:
            resp = requests.post(url, headers=headers, data=image_content, timeout=15)
            print(f"Status Code: {resp.status_code}")
            if resp.status_code == 200:
                print("✅ SUCCESS!")
                return
            else:
                print(f"Response: {resp.text[:100]}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_variations()
