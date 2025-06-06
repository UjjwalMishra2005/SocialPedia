from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import photo,Message
from channels.layers import get_channel_layer


@receiver(post_save, sender = User)
def create_photo_model(sender,instance,created,**kwargs):
    if created:
        photo_new = photo.objects.create(user=instance)


    