from MessagingSystem.models import Message
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.forms.models import model_to_dict

import json

@csrf_exempt
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
    if request.method == 'POST':

        # get request info from the body.
        sender = request.POST.get('sender')
        receiver = request.POST.get('receiver')
        msg = request.POST.get('msg')
        subject = request.POST.get('subject')
        # convert the sender and the reciver names to a user objects.
        sender_user_Obj = User.objects.filter(username=sender).first()
        receiver_user_Obj = User.objects.filter(username=receiver).first()

        # #Create a new message and save in db
        msg = Message(sender=sender_user_Obj,receiver=receiver_user_Obj,message=msg,subject=subject)
        msg.save()
        # convert model object to a json
        dict_obj = model_to_dict(msg)
        serialized = json.dumps(dict_obj)
        return HttpResponse(serialized, content_type='application/json')



@csrf_exempt
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
        user_name = request.POST.get('user_name')
        print(request.GET)
        # convert the user name to a user objects.
        user_Obj = User.objects.filter(username=user_name).first()
        # Get all the messages on th

        messages_for_specific_user = Message.objects.values_list().filter(receiver=user_Obj.id)
        qs_json = serializers.serialize('json', messages_for_specific_user)
        return HttpResponse(qs_json, content_type='application/json')

@csrf_exempt
def get_all_unread_messages(request):
    pass

@csrf_exempt
def read_message(request):
    pass

@csrf_exempt
def delete_message(request):
    pass