import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MessagingSite.settings')
django.setup()
from MessagingSystem.models import Message,UnreadMessages
from django.contrib.auth.models import User
import json
from MessagingSystem.views import *
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from datetime import date
from django.forms.models import model_to_dict
import re

def foo(msg_id,user_name):
    msg_obj = Message.objects.filter(id=msg_id).first()
    if msg_obj == None:
        print("no exsit")
        return 0
    if msg_obj.sender == user_name or msg_obj.receiver == user_name:
        print("to delete")
        msg_obj.delete()
        print(msg_obj)
        return 0

if __name__ == '__main__':
    foo(41,"nitzan")

    # if msg.sender == "omer" or msg.receiver == "omer":
    #     print(msg.id)

