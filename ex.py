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
from rest_framework.authtoken.models import Token



if __name__ == '__main__':

    token = Token.objects.create(user=User.objects.filter(id=1).first())
    print(token.key)