from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import validate_comma_separated_integer_list



class Message(models.Model):

    # sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name="sender")
    sender = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    message = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    creation_date = models.CharField(max_length=50)
    read = models.BooleanField(blank=False,default=False)
 

    def __str__(self):
        return str(self.sender) + ':'  + str(self.receiver) + ':' + str(self.message)  + ':' + str(self.subject) + ':' + str(self.creation_date) + ':' + str(self.read)

