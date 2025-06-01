import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.shortcuts import get_object_or_404
from channels.db import database_sync_to_async
from django.template.loader import render_to_string
from asgiref.sync import sync_to_async

class BaseConsumer(AsyncWebsocketConsumer):
    
    @database_sync_to_async
    def get_object(self,room_name):
        from base.models import Room
        return get_object_or_404(Room,name=room_name)
    
    async def connect(self):
        try :
            self.user = self.scope['user']
            self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
            self.room_object = await self.get_object(self.chatroom_name)
        except Exception as e:
            print('error occured: ',e)
            return

        self.safe_group_name =self.chatroom_name.replace(" ", "_") 
        await self.channel_layer.group_add(
            self.safe_group_name,self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'Connected'
        }))

    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(
            self.safe_group_name,self.channel_name
        )

    @database_sync_to_async
    def create_message(self,body):
        from base.models import Message
        message_saved = Message.objects.create(
            user = self.user,
            room = self.room_object,
            body = body
        )
        self.room_object.participants.add(self.user)
        return message_saved
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        if type == "save":
            body = text_data_json['body']
            
            message = await self.create_message(body)
            print("type is :",type)
            event = {
                'type':'message_handler',
                'message_id':message.id,
            }
            await self.channel_layer.group_send(
                self.safe_group_name,event
            )


    @database_sync_to_async
    def get_message_by_id(self, id):
        from base.models import Message
        return Message.objects.get(id=id)

    async def message_handler(self, event):
        message_id = event['message_id']
        message = await self.get_message_by_id(message_id)

        context = {
            "message": message,
            "user": self.user,
            "chat_group": self.room_object  
        }

        html = await sync_to_async(render_to_string)(
            "chat_messages_partial.html", context=context
        )
        await self.send(text_data=html)


    async def message(self, event):
    
         await self.send(text_data=json.dumps(event))
