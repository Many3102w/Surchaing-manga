import requests
import json

def get_router_models():
    url = "https://router.huggingface.co/v1/models"
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            models = data.get('data', [])
            print(f"Total models: {len(models)}")
            
            # Filter for anything that looks like depth or image-to-image/image-to-text
            results = []
            for m in models:
                mid = m.get('id', '')
                arch = m.get('architecture', {})
                inputs = arch.get('input_modalities', [])
                outputs = arch.get('output_modalities', [])
                
                if 'depth' in mid.lower() or 'image' in inputs:
                    results.append(m)
            
            print(f"Found {len(results)} potential vision/depth models.")
            for m in results:
                print(f"ID: {m['id']} | Inputs: {m.get('architecture', {}).get('input_modalities')} | Providers: {[p['provider'] for p in m.get('providers', [])]}")
        else:
            print(f"Failed to get models: {resp.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_router_models()
