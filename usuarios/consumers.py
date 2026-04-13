import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BarberoConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # Unificamos el nombre a "barbero"
        await self.channel_layer.group_add("barbero", self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({"mensaje": "Connected!"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("barbero", self.channel_name)

    # El nombre de este método DEBE coincidir con el "type" enviado en la vista
    async def nueva_cita(self, event):
        # 'event' contiene directamente el diccionario que enviaste desde la vista
        print("🔥 Notificación recibida en el consumer:", event)

        await self.send(text_data=json.dumps({
            "accion": event.get("accion"),
            "id": event.get("id"),
            "titulo": event.get("titulo"),
            "descripcion": event.get("descripcion"),
            "estado": event.get("estado", "N/A"),
        }))