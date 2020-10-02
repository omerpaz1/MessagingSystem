from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")
    message = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    creation_date = models.DateField(auto_now_add=True)
 

    def __str__(self):
        return '(Sender: ' + str(self.sender) + ') (Receiver: '  + str(self.receiver) + ') (Message: '  + str(self.message)  + ') (Subject: ' + str(self.subject) + ') (Creation date: ' + str(self.creation_date) +')'