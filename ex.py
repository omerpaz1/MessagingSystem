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

def getit(user_name):
    # get the user name from the request 
    # get the user id by given the user_name from the User object.
    try:
        user_obj = User.objects.filter(username=user_name).first().id
    except:
        print("asdas")
        return HttpResponse({"not a valid argument" : "Not Found"})

    # get all the unreaded messages that sent to the requsted user
    return HttpResponse(json.dumps(list(Message.objects.values().filter(receiver=user_obj).filter(read=False))),content_type='application/json')



if __name__ == '__main__':
    try:
        print(User.objects.filter(username="ASDAS").first().id)
    except:
        print("BAD")



