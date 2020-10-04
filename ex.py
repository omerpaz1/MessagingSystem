import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MessagingSite.settings')
django.setup()
from MessagingSystem.models import Message
from django.contrib.auth.models import User
import json
from MessagingSystem.views import *
from django.http import JsonResponse,HttpResponse,HttpResponseServerError
from django.core import serializers
from datetime import date
from django.forms.models import model_to_dict
from rest_framework.authtoken.models import Token
import re

def foo():
    return HttpResponseServerError("server got an error by try get data")

if __name__ == '__main__':
    user3 = User.objects.filter(id=3).first() 
    user4 = User.objects.filter(id=4).first()

    Token.objects.create(user=user3)
    Token.objects.create(user=user4)