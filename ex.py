import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MessagingSite.settings')
django.setup()
from MessagingSystem.models import Message
from django.contrib.auth.models import User
import json
from django.http import JsonResponse,HttpResponse
from django.core import serializers


if __name__ == '__main__':
    user_Obj = User.objects.filter(username="omer").first()
        # Get all the messages on th

    messages_for_specific_user = Message.objects.values_list().filter(receiver=user_Obj.id)
    print(messages_for_specific_user)
    # user_Obj = User.objects.filter(username="nitzan").first()
    # # Get all the messages on th

    # messages_for_specific_user = Message.objects.values_list().filter(receiver=user_Obj.id)

    # print(json.dumps(messages_for_specific_user, indent=4)

