from django.contrib import admin
from MessagingSystem.models import Message,UnreadMessages

admin.site.register(Message)
admin.site.register(UnreadMessages)