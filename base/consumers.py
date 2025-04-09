import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .forms import MessageForm
from .models import Room,Message
from django.contrib.auth.models import User


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
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action',False)
        if action=="delete_message":
            message_id = text_data_json.get('message_id')
            if message_id:
                deleted = await self.deleteMessage(message_id)
                if deleted:
                    await self.channel_layer.group_send(
                        "New_message",
                        {
                            "type":"delete_message",
                            "message_id":message_id
                        }
                    )
        else:
        
            message = text_data_json['message']
            room_id = text_data_json['room_id']
            user_id = text_data_json['user_id']
            message_id = await self.validate_and_save_message(message,room_id,user_id)

        # await self.channel_layer.group_send(
        #     "New_message",{
        #         "type":"message",
        #         "id":message_id,
        #         "message":message,
        #     }
        # )
    

    
    
    async def message(self,event):
        message = event.get('message')
        id = event.get('id')
        type = event.get('type')
        await self.send(text_data=json.dumps({
            "message":message,
            "id":id,
            "type":type
        }))

    @database_sync_to_async
    def validate_and_save_message(self,message,room_id,user_id):
        room = Room.objects.get(id=room_id)
        user = User.objects.get(id=user_id)
        form = MessageForm(data={
            "body":message,
            "room":room,
            "user":user,
        })
        room.participants.add(user)
        if form.is_valid():
            saved_form = form.save()
            print('MessageForm is saved successfully')
            return saved_form.id
        else:
            print(f"errors in messageform : {form.errors}")
            return False
        
    @database_sync_to_async
    def deleteMessage(self,id):
        try:
            message = Message.objects.get(id=id)
            
        except Message.DoesNotExist :
            print("Message Does not exists")
            return False
        except:
            print("something went wrong while deleting message")
            return False
        else:
            
            print(f"Message : {message} is deleted from database--->consumers")
            message.delete()
            return True
        
    async def delete_message(self,event):
        message_id = event.get("message_id")
        await self.send(text_data=json.dumps({
            "type":"delete_message",
            "message_id":message_id
        }))
