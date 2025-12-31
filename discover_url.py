import requests
from huggingface_hub import InferenceClient
from unittest.mock import patch

def discover_url():
    token = "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"
    model_id = "gpt2" # Simple model
    client = InferenceClient(token=token)
    
    print("Intercepting requests.post from InferenceClient...")
    with patch("requests.post") as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = [{"generated_text": "test"}]
        
        try:
            # Try a simple text generation
            client.text_generation("Hello", model=model_id)
        except Exception as e:
            print(f"Client failed but maybe we caught the URL: {e}")
        
        if mock_post.called:
            args, kwargs = mock_post.call_args
            print(f"✅ Intercepted URL: {args[0]}")
            print(f"Intercepted Headers: {kwargs.get('headers')}")
        else:
            print("❌ requests.post was not called directly. Trying httpx...")
            with patch("httpx.Client.post") as mock_httpx_post:
                 mock_httpx_post.return_value.status_code = 200
                 try:
                     client.text_generation("Hello", model=model_id)
                 except: pass
                 if mock_httpx_post.called:
                     args, kwargs = mock_httpx_post.call_args
                     # In httpx, the first arg might be the URL or it might be in kwargs
                     url = args[0] if args else kwargs.get('url')
                     print(f"✅ Intercepted URL (httpx): {url}")
                 else:
                     print("❌ Still not caught. The library might be using a newer method.")

if __name__ == "__main__":
    discover_url()
