from gradio_client import Client, handle_file
import requests
import os

token = "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"
headers = {"Authorization": f"Bearer {token}"}

def test_token():
    print(f"Testing token via HTTP...")
    response = requests.get("https://huggingface.co/api/whoami-v2", headers=headers)
    if response.status_code == 200:
        print("✅ HTTP Token is VALID.")
    else:
        print(f"❌ HTTP Token is INVALID: {response.status_code}")
        return

    print(f"Testing token via gradio_client...")
    try:
        # Probamos inicializar el cliente con el argumento corregido 'token'
        client = Client("depth-anything/Depth-Anything-V2", token=token)
        print("✅ Gradio Client initialized successfully with token.")
    except Exception as e:
        print(f"❌ Gradio Client failed: {e}")

if __name__ == "__main__":
    test_token()
