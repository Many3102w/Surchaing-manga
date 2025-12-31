import json

def find_models():
    try:
        with open('router_models.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        models = data.get('data', [])
        print(f"Total models in router: {len(models)}")
        
        depth_models = []
        vision_models = []
        
        for m in models:
            mid = m.get('id', '')
            arch = m.get('architecture', {})
            inputs = arch.get('input_modalities', [])
            
            if 'depth' in mid.lower():
                depth_models.append(m)
            if 'image' in inputs:
                vision_models.append(m)
        
        print("\n--- Models containing 'depth' ---")
        for m in depth_models:
            print(f"ID: {m['id']}")
            print(f"  Architecture: {m.get('architecture')}")
            print(f"  Providers: {[p['provider'] for p in m.get('providers', [])]}")
        
        print(f"\nTotal vision models (image input): {len(vision_models)}")
        if not depth_models:
            print("Found NO models with 'depth' in ID. Checking vision models for depth-related tags/architectures...")
            # For brevity, only print first 10
            for m in vision_models[:20]:
                print(f"ID: {m['id']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_models()
