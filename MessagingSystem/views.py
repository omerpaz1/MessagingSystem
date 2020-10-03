from MessagingSystem.models import Message,UnreadMessages
from django.contrib.auth.models import User
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.forms.models import model_to_dict
from datetime import date

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
        msg = str(request.POST.get('msg'))
        subject = str(request.POST.get('subject'))

        # convert the sender and the reciver names to a user objects.

        sender_user_Obj = User.objects.filter(username=sender).first()
        receiver_user_Obj = User.objects.filter(username=receiver).first()

        #Create a new message and save in db
        the_current_date = date.today()
        try:
            msg = Message(sender=sender_user_Obj,receiver=receiver_user_Obj,message=msg,subject=subject,creation_date=str(the_current_date))
            msg.save()
        except:
            return HttpResponse({"there is a non valid parameter" : -1})

        # convert model object to a json
        return HttpResponse(json.dumps(model_to_dict(msg)), content_type='application/json')



@csrf_exempt
def get_all_messages(request):
    """
    Receive all messages for a specific user

    Parameters
    ----------
    user_name : str
        The name of the sender of the message

    Returns
    -------
    HttpResponse
        contains a json object that contains all the messages of the specific user
        or a empty dict if doesn't have any messages

    """
    if request.method == 'POST':
        # List of messages of the requested user
        user_messages = []

        # get the user name from the request 
        user_name = request.POST.get('user_name')

        
        # convert the user name to a user objects.
        user_Obj = User.objects.filter(username=user_name).first()

        # get all the messages of the specific user that requsted 
        try:
            messages_for_specific_user = Message.objects.values().filter(receiver=user_Obj.id)
        except:
            return HttpResponse({"user name doesn't exsits" : -1})

        # convert model object to a json
        return HttpResponse(json.dumps(list(messages_for_specific_user)),content_type='application/json')

@csrf_exempt
def get_all_unread_messages(request):
    """
    get all the unreaded messages of a user that requsted.

    Parameters
    ----------
    user_name : str
        The name of the requsted user to get heis unreaded messages

    Returns
    -------
    HttpResponse
        contains a json object that contains all the unreaded messages
        or a empty dict if doesn't have any messages

    """
    if request.method == 'POST':
        # get the user name from the request 
        user_name = request.POST.get('user_name')

        # get the user id by given the user_name from the User object.
        try:
            user_obj = User.objects.filter(username=user_name).first().id
            # get all the unreaded messages that sent to the requsted user
            return HttpResponse(json.dumps(list(Message.objects.values().filter(receiver=user_obj).filter(read=False))),content_type='application/json')
        except:
            return JsonResponse({"user name doesn't exsits" : -1})
    

@csrf_exempt
def read_message(request):
    json_response = get_all_unread_messages(request)
    all_unreaded_msgs = json.loads(json_response.content)
    try:
        unreaded_msg_dict = all_unreaded_msgs.pop()
    except:
        return HttpResponse({"There is not unreaded messages left" : -1})
        
    unreaded_msg = Message.objects.filter(id=unreaded_msg_dict.get('id')).first()
    unreaded_msg.read = True
    unreaded_msg.save()
    return HttpResponse(json.dumps(unreaded_msg_dict),content_type='application/json')

@csrf_exempt
def delete_message(request):
    pass


