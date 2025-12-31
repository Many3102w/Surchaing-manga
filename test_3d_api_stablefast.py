from gradio_client import Client
import os

try:
    client = Client("stabilityai/stable-fast-3d")
    print("API Endpoints:")
    client.view_api()
except Exception as e:
    print(f"Error connecting to StableFast3D: {e}")
