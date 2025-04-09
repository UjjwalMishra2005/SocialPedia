from django.forms import ModelForm
from .models import Room,Message,User,photo

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body','room','user']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email','password']
class PhotoForm(ModelForm):
    class Meta:
        model = photo
        fields = ['user','image']