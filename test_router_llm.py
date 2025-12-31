import requests

def test_router_llm():
    token = "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"
    url = "https://router.huggingface.co/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt2",
        "messages": [{"role": "user", "content": "Say hello"}],
        "max_tokens": 10
    }
    
    print(f"Testing router LLM at {url}...")
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
    test_router_llm()
