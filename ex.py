import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MessagingSite.settings')
django.setup()
from MessagingSystem.models import Message
from django.contrib.auth.models import User




if __name__ == '__main__':
    a = Message.objects.values_list().filter(receiver=2)
    print(a)

