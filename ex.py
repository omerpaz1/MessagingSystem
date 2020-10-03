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


if __name__ == '__main__':
    # id_msg = 3
    # msg = Message.objects.filter(id=id_msg).first()
    # print(msg)
    # if msg.sender == "omer" or msg.reciver == "omer":
    #     print(msg.id)
    Message.objects.all().delete()


