# from os import name
# from tempfile import NamedTemporaryFile
# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

class UserInfo(models.Model) :
    # FK to user
    user =  models.OneToOneField(User , on_delete= models.CASCADE)
    name  =  models.CharField(max_length=100)
    email  =  models.EmailField()
    image = models.ImageField(upload_to='profile_images/' , blank = True ,  null  = True)

    def __str__(self):
        return self.name
# class CustomUser(AbstractUser):
#     profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
#     def __str__(self):
#         return self.username

class ChatRoom(models.Model):
    name=models.CharField(max_length=100)
    participants=models.ManyToManyField(User,related_name='chat_rooms')
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Message(models.Model):
    content=models.TextField()
    #foreignkey=one to many
    sender=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name='sent_messages')
    chatroom=models.ForeignKey(ChatRoom,on_delete=models.CASCADE,related_name='messages')
    timestamp=models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering=['timestamp']
    # def __str__(self):
    #     return f"{self.sender} @ {self.chatRoom}: {self.content[:30]}"

