import time
import requests
import datetime
import sys

# URL de tu proyecto en Render
URL = "https://moda-gomez.onrender.com/ping/"
INTERVALO_MINUTOS = 14 # Render duerme a los 15 min, 14 es seguro.

def ping_server():
    print(f"[{datetime.datetime.now()}] 🤖 Bot Anti-Sleep Iniciado...")
    print(f"Target: {URL}")
    print(f"Intervalo: {INTERVALO_MINUTOS} minutos")
    print("-" * 40)
    
    while True:
        try:
            print(f"[{datetime.datetime.now()}] 📡 Enviando ping...", end=" ")
            response = requests.get(URL, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ ÉXITO (Status: {response.status_code})")
            else:
                print(f"⚠️ ALERTA (Status: {response.status_code})")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            
        # Esperar X minutos
        time.sleep(INTERVALO_MINUTOS * 60)

if __name__ == "__main__":
    try:
        ping_server()
    except KeyboardInterrupt:
        print("\n🛑 Bot detenido por el usuario.")
        sys.exit(0)
