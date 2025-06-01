from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import photo,Message
from channels.layers import get_channel_layer


@receiver(post_save, sender = User)
def create_photo_model(sender,instance,created,**kwargs):
    if created:
        photo_new = photo.objects.create(user=instance)
        print("new photo object is created with user ")

"""@receiver(post_save,sender=Message)
def send_message(sender,instance,created,**kwargs):
    if created:
        '''channel_layer = get_channel_layer()
        from asgiref.sync import async_to_sync
        async_to_sync(channel_layer.group_send)(
            "New_message",
        {   "type":"message",
            "id":instance.user.id,
            "message_id":instance.id,
            "room_id":instance.room.id,
            "message":instance.body,
        }
        )'''
        print('\nid :', instance.id,'\nmessage_body : ',instance.body,'\n')
        print("Message = ",instance.body,'\n','Message id = ',instance.id ,' ------->signals')"""
    