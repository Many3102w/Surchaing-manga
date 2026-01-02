import requests
import os

token = "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"
model_id = "LiheYoung/depth-anything-large-hf"

urls = [
    f'https://router.huggingface.co/hf-inference/models/{model_id}',
    f'https://router.huggingface.co/hf-inference/{model_id}',
]

headers = {"Authorization": f"Bearer {token}"}
test_image_url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg"
image_data = requests.get(test_image_url).content

for url in urls:
    print(f"\nTesting URL: {url}")
    try:
        response = requests.post(url, headers=headers, data=image_data, timeout=10)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ SUCCESS!")
        else:
            print(f"Error: {response.text[:200]}")
    except Exception as e:
        print(f"FAILED: {e}")
