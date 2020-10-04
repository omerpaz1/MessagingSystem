from MessagingSystem.models import Message
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from datetime import date
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from MessagingSystem.forms import MessageForm,UserID,DeleteMessage

DateToJson = lambda obj: (
    obj.isoformat()
    if isinstance(obj, date)
    else None
)

import json

@api_view(['POST'])
@csrf_exempt
def write_message(request):
    """
    Write a new message by user to other user.
    We assume that request variables are:
        sender {int} -- the sender id.
        receiver {int} -- the receiver id.
        message {str} -- the message the sender wants to send to the receiver, message limit is 100 chars.
        subject {str} -- the subject of message, subject limit is 50 chars.

    Arguments:
        request {Request} -- Request object.

    Returns:
        Response -- The appropriate HttpResponse object.
    """

    # get request info from the body.
    form = MessageForm(request.POST)
    if form.is_valid():
        sender = request.POST.get('sender')
        receiver = request.POST.get('receiver')
        msg = request.POST.get('msg')
        subject = request.POST.get('subject')
    else:
        return HttpResponseNotFound("not valid form")
  

    # get the sender and the receiver as a User obj
    sender_user_Obj = User.objects.filter(id=sender).first()
    receiver_user_Obj = User.objects.filter(id=receiver).first() 

    # check if the sender or the reciver objects does not exists
    if not sender_user_Obj or not receiver_user_Obj:
        return HttpResponseNotFound("sender or receiver does not exist")

    # Create a new message and save in db
    Message.objects.create(sender=sender_user_Obj,receiver=receiver_user_Obj,message=msg,subject=subject,creation_date=date.today())

    return HttpResponse("The message was created successfully")

@api_view(['GET'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_messages(request):
    """
    Receive all messages for a specific user

    We assume that request variable is:
        user_id {int} -- the requested user id


    Arguments:
        request {Request} -- Request object.

    Returns:
        Response -- The appropriate HttpResponse object.
    """
    # check if the request user is a superuser
    if request.user.is_superuser:

        form = UserID(request.GET)

        if form.is_valid():
            user_id = request.GET.get('user_id')   
        else:
            return HttpResponseNotFound("not valid form")

        # get user object from the user_id
        user_obj = User.objects.filter(id=user_id).first()

        if not user_obj:
            return HttpResponseNotFound("user object does not exist")
    # the user is authenticated then get the user from the request.
    else:
        user_obj = request.user

    # get all the messages of the specific user that requsted 
    messages_for_specific_user = Message.objects.values().filter(receiver=user_obj,visible=True)

    # convert model object to a json and return respones
    return HttpResponse(json.dumps(list(messages_for_specific_user),default=DateToJson),content_type='application/json')

@api_view(['GET'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_unread_messages(request):
    """
    get all the unreaded messages of a user.

    We assume that request variable is:
        user_id {int} -- the requested user id

    Arguments:
        request {Request} -- Request object.

    Returns:
        Response -- The appropriate HttpResponse object.

    """
    # check if the request user is a superuser
    if request.user.is_superuser:

        form = UserID(request.GET)
        if form.is_valid():
            user_id = request.GET.get('user_id')   
        else:
            return HttpResponseNotFound("not valid form")

        # get user object from the user_id
        user_obj = User.objects.filter(id=user_id).first()

        if not user_obj:
            return HttpResponseNotFound("user object does not exist")
    # the user is authenticated then get the user from the request.
    else:
        user_obj = request.user

    # get all the unreaded messages that sent to the requsted user
    return HttpResponse(json.dumps(list(Message.objects.values().filter(receiver=user_obj,read=False,visible=True)),default=DateToJson),content_type='application/json')

        
@api_view(['PUT'])
@csrf_exempt
def read_message(request):
    """
    read the last message that sent to a requsted user


    We assume that request variable is:
        user_id {int} -- the requested user id

    Arguments:
        request {Request} -- Request object.

    Returns:
        Response -- The appropriate HttpResponse object.

    """
    # get the user id from the request 
    form = UserID(request.GET)
    if form.is_valid():
        user_id = request.GET.get('user_id')   
    else:
        return HttpResponseNotFound("not valid form")

    # get user object from the user_id
    user_Obj = User.objects.filter(id=user_id).first()
        
    if not user_Obj:
        return HttpResponseNotFound("user object does not exist")

    unreaded_msg_obj = Message.objects.filter(receiver=user_Obj,read=False).last()

    if not unreaded_msg_obj:
        # make the message as Ture and return it
        return HttpResponse("there is not unreaded messages for you")

    else:
        unreaded_msg_obj.read = True
        unreaded_msg_obj.save()    

    return HttpResponse(json.dumps(model_to_dict(unreaded_msg_obj),default=DateToJson),content_type='application/json')

@api_view(['DELETE'])
@csrf_exempt
def delete_message(request,user_id=None,msg_id=None):

    """
    delete a message of a requested user
    We assume that request variable is:
        user_id {int} -- the requested user id

    Arguments:
        request {Request} -- Request object.

    Returns:
        Response -- The appropriate HttpResponse object.

    """
    # get the user id and the message id from the request 
    form = DeleteMessage(request.GET)
    if form.is_valid():
        user_id = request.GET.get('user_id')  
        msg_id =  request.GET.get('msg_id')  
    else:
        return HttpResponseNotFound("not valid form")


    user_obj = User.objects.filter(id=user_id).first()        
    msg_obj = Message.objects.filter(id=msg_id,visible=True).first()

    # check if msg_obj and user_obj exists
    if not msg_obj or not user_obj:
        return HttpResponseNotFound("message or user object does not exist")

        # if the sender or the receiver equal to the user name in the request, we delete the message.
    if msg_obj.sender == user_obj or msg_obj.receiver == user_obj:
        msg_obj.visible = False
        msg_obj.save()

        return HttpResponse("The message was deleted successfully")
    else:
        return HttpResponseNotFound("user id is not equal to the sender or the reciver")

    