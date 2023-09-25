from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sen', on_delete=models.CASCADE)
    reciver = models.ForeignKey(User, related_name='rev', on_delete=models.CASCADE)
    msg = models.CharField(max_length=200)
    pict = models.ImageField(upload_to = "Message", blank = True, null = True)
    dat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.sender)
