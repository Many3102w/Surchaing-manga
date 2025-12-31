from huggingface_hub import InferenceClient

def test_router_manual_url():
    token = "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"
    # Testing with the router base URL
    base_url = "https://router.huggingface.co/hf-inference"
    client = InferenceClient(token=token, base_url=base_url)
    
    print(f"Testing text-generation on router via {base_url}...")
    try:
        result = client.text_generation("The future of AI is", model="gpt2")
        print(f"✅ SUCCESS! Result: {result}")
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    test_router_manual_url()
