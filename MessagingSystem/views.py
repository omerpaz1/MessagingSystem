from django.http import HttpResponse
from django.shortcuts import render , redirect
from MessagingSystem.models import Message
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers
import json


def write_message(request):
    """
    write a new message by user to other user

    Parameters
    ----------
    sender : str
        The name of the sender of the message
    receiver : str
        The name of the receiver of the message
    message : str
        content of the message
    subject : str
        The subject of the message 

    Returns
    -------
    None
    """ 
    if request.method == 'GET':

        # convert the sender and the reciver names to a user objects.
        
        sender_user_Obj = User.objects.filter(username="omer").first()
        receiver_user_Obj = User.objects.filter(username="tal").first()

        #Create a new message and save in db
        msg = Message(sender=sender_user_Obj,receiver=receiver_user_Obj,message="here",subject="test")
        msg.save()
        a = Message.objects.filter(id=msg.id).first()


        return JsonResponse(list,safe=False)
        # return JsonResponse({"models_to_return": list(msg)}, safe=False)
    # return JsonResponse({"models_to_return": list(msg)},safe=False)


def get_all_messages(request):
    """
    Receive all messages for a specific user

    Parameters
    ----------
    username : str
        The name of the sender of the message

    Returns
    -------
    QuerySet
        a QuerySet that contains all the messages of the specific user
    """ 

    if request.method == 'POST':
        # List of messages of the requested user
        user_messages = []
        user_post_option = request.POST.get('paz',False)
        # convert the user name to a user objects.
        user_Obj = User.objects.filter(username=user_post_option).first()
        # Get all the messages on th

        messages_for_specific_user = Message.objects.values_list().filter(receiver=user_Obj.id)
        return JsonResponse(list(messages_for_specific_user),safe=False)

def get_all_unread_messages(request):
    pass

def read_message(request):
    pass

def delete_message(request):
    pass