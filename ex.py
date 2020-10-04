import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MessagingSite.settings')
django.setup()
from MessagingSystem.models import Message
from django.contrib.auth.models import User
import json
from MessagingSystem.views import *
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from datetime import date
from django.forms.models import model_to_dict
import re



if __name__ == '__main__':

    sender_user_Obj = User.objects.filter(id="3").first()
    print(sender_user_Obj)
