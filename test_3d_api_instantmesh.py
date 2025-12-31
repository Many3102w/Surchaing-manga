from gradio_client import Client
import os

try:
    client = Client("TencentARC/InstantMesh")
    print("API Endpoints:")
    client.view_api()
except Exception as e:
    print(f"Error connecting to InstantMesh: {e}")
