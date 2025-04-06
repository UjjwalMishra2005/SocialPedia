import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BaseConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        await self.channel_layer.group_add(
            "New_message",
            self.channel_name
        )
        await self.accept()
        await self.send(text_data = json.dumps({
            'type':'connection_established',
            'message':'Connected'
            
        }))
    async def receive(self,text_data):
        pass