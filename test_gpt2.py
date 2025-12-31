import requests

def test_gpt2():
    token = "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"
    model_id = "gpt2"
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"inputs": "The 3D conversion feature is"}
    
    print(f"Testing GPT-2 at {url}...")
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"Status Code: {resp.status_code}")
        if resp.status_code == 200:
            print(f"✅ SUCCESS! Response: {resp.json()}")
        else:
            print(f"Response: {resp.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_gpt2()
