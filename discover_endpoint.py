from huggingface_hub import InferenceClient

def discover_endpoint():
    token = "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"
    models = ["Intel/dpt-large", "LiheYoung/depth-anything-large-hf"]
    client = InferenceClient(token=token)
    
    for model_id in models:
        print(f"--- Discovering endpoint for {model_id} ---")
        try:
            info = client.get_endpoint_info(model=model_id)
            print(f"✅ Found Info: {info}")
        except Exception as e:
            print(f"❌ Failed to get info: {e}")

if __name__ == "__main__":
    discover_endpoint()
