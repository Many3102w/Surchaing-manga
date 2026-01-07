import threading
import time
import requests
import os
import logging

APP_URL = os.environ.get("RENDER_EXTERNAL_URL", "https://moda-gomez.onrender.com")
PING_URL = f"{APP_URL}/ping/"
INTERVAL = 14 * 60  # 14 minutes in seconds

logger = logging.getLogger(__name__)

def ping_server():
    while True:
        try:
            logger.info(f"Pinging {PING_URL} to keep server alive...")
            response = requests.get(PING_URL, timeout=10)
            logger.info(f"Ping result: {response.status_code}")
        except Exception as e:
            logger.error(f"Error pinging server: {e}")
        time.sleep(INTERVAL)

def start_keep_alive():
    try:
        # Start the background thread
        thread = threading.Thread(target=ping_server, daemon=True)
        thread.start()
        logger.info("Keep-alive thread started.")
    except Exception as e:
         logger.error(f"Failed to start keep-alive thread: {e}")
