from gradio_client import Client
import os

try:
    client = Client("TencentARC/Hunyuan3D-2.1")
    print("API Endpoints:")
    client.view_api()
except Exception as e:
    print(f"Error connecting to Hunyuan3D: {e}")
