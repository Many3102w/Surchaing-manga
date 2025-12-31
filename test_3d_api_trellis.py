from gradio_client import Client
import os

try:
    client = Client("JeffreyXiang/TRELLIS")
    print("API Endpoints:")
    client.view_api()
except Exception as e:
    print(f"Error connecting to TRELLIS: {e}")
