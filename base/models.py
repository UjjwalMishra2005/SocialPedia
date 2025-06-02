from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic (models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
    # Predefined fields inherited from User:
    # - username
    # - first_name
    # - last_name
    # - email
    # - password
    # - is_staff
    # - is_active
    # - date_joined
    # - last_login
                                                                                    
class Room(models.Model):
    host = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    # ForeignKey represents many to one field means one host can have multiple rooms
    topic= models.ForeignKey(Topic,on_delete=models.SET_NULL,null=True)
    # In the similar way one topic can have multiple rooms
    id = models.AutoField(primary_key=True)
    participants = models.ManyToManyField(User,related_name='participants',blank=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created','-updated']

    def __str__(self):
        return self.name
from django.core.validators import MinLengthValidator
class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    body = models.TextField(null=False,blank=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[:50]
    class Meta:
        ordering = ['-created','-updated',]
        # -created means reverse order of created
from cloudinary.models import CloudinaryField
class photo(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,related_name="dp")
    image = CloudinaryField('image',default='o2pachscqy1o3ys4j0sw')
    


    


