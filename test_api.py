from huggingface_hub import InferenceClient
import os
import django
import sys

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webcomic.settings')
django.setup()

def test_client_full_base_url():
    token = "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"
    model_id = "Intel/dpt-large"
    
    # Try to force the full URL as base
    # Note: If the client appends the model ID again, this will fail with 404
    # But if we call post() with NO model, it might just use the base.
    full_url = f"https://router.huggingface.co/hf-inference/models/{model_id}"
    print(f"Testing InferenceClient with base_url={full_url}...")
    client = InferenceClient(base_url=full_url, token=token)
    
    test_image_path = 'C:/Users/Many/.gemini/antigravity/brain/e6b8b7a1-b6fa-4410-a279-5678ad5a47d1/test_manga_cover_1767092943383.png'
    with open(test_image_path, 'rb') as f:
        image_content = f.read()

    try:
        # Call post with NO model to avoid it appending to the base_url
        response = client.post(data=image_content)
        print(f"✅ SUCCESS! Status: {response.status_code}")
        print(f"Response headers: {response.headers}")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_client_full_base_url()
