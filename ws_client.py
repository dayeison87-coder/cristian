import websocket
import json
import time

def on_message(ws, message):
    print("📩 Mensaje recibido:", message)

def on_error(ws, error):
    print("❌ Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("🔌 Conexión cerrada")

def on_open(ws):
    print("Conectado!")

if __name__ == "__main__":
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp(
        "ws://127.0.0.1:8000/ws/barbero/",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    while True:
        try:
            ws.run_forever()
        except Exception as e:
            print("Reintentando...", e)
            time.sleep(3)