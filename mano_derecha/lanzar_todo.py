import subprocess
import time
import sys
import os

def lanzar():
    print("🚀 ARRANCANDO MANO DERECHA (Versión Producción)...")
    
    # Esto detecta automáticamente dónde está parado el script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Rutas corregidas (sin repetir 'mano_derecha')
    api_path = os.path.join(base_dir, "api", "app.py")
    bot_path = os.path.join(base_dir, "automation", "bot.py")

    # Verificación de seguridad
    if not os.path.exists(api_path):
        print(f"❌ Error: No encuentro el archivo en {api_path}")
        return

    # 1. Lanzamos la API (Web)
    p_api = subprocess.Popen([sys.executable, api_path])
    time.sleep(2) 
    
    # 2. Lanzamos el Bot
    p_bot = subprocess.Popen([sys.executable, bot_path])
    
    try:
        print("✅ Todo encendido. Presioná Ctrl+C para apagar.")
        p_api.wait()
        p_bot.wait()
    except KeyboardInterrupt:
        p_api.terminate()
        p_bot.terminate()
        print("\n🛑 Sistema apagado.")

if __name__ == "__main__":
    lanzar()