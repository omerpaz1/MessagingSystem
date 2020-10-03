from MessagingSystem.models import Message
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotFound,HttpResponseServerError
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
        the user that will be the 'sender' of the message
    receiver : str
        the user that will be the ;receiver; of the message
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

        # get the sender and the receiver as a User obj
        
        sender_user_Obj = User.objects.filter(username=sender).first()
        receiver_user_Obj = User.objects.filter(username=receiver).first()
        # check if the sender or the reciver objects does not exists
        if sender_user_Obj == None or receiver_user_Obj == None:
            return HttpResponseNotFound("sender or receiver user name does not exsit")

        #Create a new message and save in db
        the_current_date = date.today()
        try:
            msg = Message(sender=sender,receiver=receiver,message=msg,subject=subject,creation_date=str(the_current_date))
            msg.save()
        except:
            return HttpResponseServerError("there is an error when creating a new message obj")

        # return HttpResponse(json.dumps(model_to_dict(msg)), content_type='application/json')
        return HttpResponse("The message was created successfully")


@csrf_exempt
def get_all_messages(request):
    """
    Receive all messages for a specific user

    Parameters
    ----------
    user_name : str
        the user that we want to receive heis all messages 

    Returns
    -------
    HttpResponse
        a json object that contains all the messages of the specific user
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
            messages_for_specific_user = Message.objects.values().filter(receiver=user_Obj.username)
        except:
            return HttpResponseNotFound("user name does not exsit")

        # convert model object to a json
        return HttpResponse(json.dumps(list(messages_for_specific_user)),content_type='application/json')

@csrf_exempt
def get_all_unread_messages(request):
    """
    get all the unreaded messages of a user that requsted.

    Parameters
    ----------
    user_name : str
        the user that we will get heis unreaded messages

    Returns
    -------
    HttpResponse
         a json object that contains all the unreaded messages
        or a empty dict if doesn't have any messages

    """
    if request.method == 'POST':
        # get the user name from the request 
        user_name = request.POST.get('user_name')

        try:
             # get the user id by given the user_name from the User object.
            user_obj = User.objects.filter(username=user_name).first()
            # get all the unreaded messages that sent to the requsted user
            return HttpResponse(json.dumps(list(Message.objects.values().filter(receiver=user_obj.username).filter(read=False))),content_type='application/json')
        except:
            return HttpResponseNotFound("user name does not exsit")
        

@csrf_exempt
def read_message(request):
    """
    read the last message that sent to a requsted user

    Parameters
    ----------
    user_name : str
        the user that we will get heis last message and read it

    Returns
    -------
    HttpResponse
        a json object that the message that we pick to read

    """

    if request.method == 'POST':
        # get the user name from the request 
        user_name = request.POST.get('user_name')   

        # get the user id by given the user_name from the User object.
        user_obj = User.objects.filter(username=user_name).first()
        if user_obj == None:
            return HttpResponseNotFound("user name doesn't exsit")

        try:
            # pop one message from all the unreaded messages for the user
            unreaded_msg_obj = list(Message.objects.filter(receiver=user_obj.username).filter(read=False)).pop()
        except:
            return HttpResponseNotFound("There is not unreaded messages left")
        else:
            # make the message as Ture and return it
            unreaded_msg_obj.read = True
            unreaded_msg_obj.save()   

            return HttpResponse(json.dumps(model_to_dict(unreaded_msg_obj)),content_type='application/json')

@csrf_exempt
def delete_message(request):

    """
    delete a message of a requested user

    Parameters
    ----------
    user_name : str
        the user that we want to delete message from heis messages

    Returns
    -------
    None

    """

    if request.method == 'POST':
        # get the user name and the message id from the request 
        user_name = request.POST.get('user_name')  
        msg_id =  request.POST.get('msg_id')  

        msg_obj = Message.objects.filter(id=msg_id).first()
        # check if the requested message exsit
        if msg_obj == None:
            return HttpResponseNotFound("message object does not exsit")

        # if the sender or the receiver equal to the user name in the request, we delete the message.
        if msg_obj.sender == user_name or msg_obj.receiver == user_name:
            try:
                msg_obj.delete()
            except:
                return HttpResponseServerError("can not delete this object")

            return HttpResponse("The message was deleted successfully")
    