from MessagingSystem.models import Message
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from datetime import date
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
import json

@api_view(['POST'])
@csrf_exempt
def write_message(request):
    """
    write a new message by user to other user

    Arguments
    ----------
    request - we are expecting the following parameters:
        sender : str
            the user that will be the "sender" of the message (need to be integer)
        receiver : str
            the user that will be the "receiver" of the message (need to be integer)
        message : str
            content of the message
        subject : str
            The subject of the message 

    Returns
    -------
    HttpResponse
    """

    # get request info from the body.
    sender = request.POST.get('sender')
    receiver = request.POST.get('receiver')
    msg = request.POST.get('msg')
    subject = request.POST.get('subject')

    # get the sender and the receiver as a User obj
    if RepresentsInt(sender) and RepresentsInt(receiver):
        sender_user_Obj = User.objects.filter(id=sender).first()
        receiver_user_Obj = User.objects.filter(id=receiver).first() 
    else:
        return HttpResponse("sender and reciver parameters should be a integer numbers",status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # check if the sender or the reciver objects does not exists
    if not sender_user_Obj or not receiver_user_Obj:
        return HttpResponseNotFound("sender or receiver does not exist")

    #Create a new message and save in db
    the_current_date = date.today()
    Message.objects.create(sender=sender_user_Obj,receiver=receiver_user_Obj,message=msg,subject=subject,creation_date=the_current_date)

    return HttpResponse("The message was created successfully")

@api_view(['GET'])
@csrf_exempt
def get_all_messages(request):
    """
    Receive all messages for a specific user

    Arguments
    ----------
    request - we are expecting the following parameters:
        user_id : str
            the user that we want to receive heis all messages 
    Returns
    -------
    HttpResponse
        a json object that contains all the messages of the specific user
        or a empty dict if doesn't have any messages

    """
    authentication_classes = (TokenAuthentication,)
    # get the user name from the request
    user_id = request.GET.get('user_id',None)

    # get user object from the user_id and check validation
    if RepresentsInt(user_id):
        user_Obj = User.objects.filter(id=user_id).first()
    else:
        return HttpResponse("user_id should be a integer number",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    if not user_Obj:
        return HttpResponseNotFound("user object does not exist")

    # get all the messages of the specific user that requsted 
    messages_for_specific_user = Message.objects.values().filter(receiver=user_Obj,visible=True)

    # convert model object to a json
    return HttpResponse(json.dumps(list(messages_for_specific_user)),content_type='application/json')

@api_view(['GET'])
@csrf_exempt
def get_all_unread_messages(request):
    """
    get all the unreaded messages of a user that requsted.

    Parameters
    ----------
    request - we are expecting the following parameters:
        user_id : str
            the user that we will get heis unreaded messages

    Returns
    -------
    HttpResponse
        a json object that contains all the unreaded messages
        or a empty dict if doesn't have any messages

    """
    # get the user name from the request 
    user_id = request.GET.get('user_id')

    # get user object from the user_id and check validation
    if RepresentsInt(user_id):
        user_obj = User.objects.filter(id=user_id).first()
    else:
        return HttpResponse("user_id should be a integer number",status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if not user_obj:
        return HttpResponseNotFound("user object does not exist")

    # get all the unreaded messages that sent to the requsted user
    return HttpResponse(json.dumps(list(Message.objects.values().filter(receiver=user_obj,read=False,visible=True))),content_type='application/json')

        
@api_view(['PUT'])
@csrf_exempt
def read_message(request):
    """
    read the last message that sent to a requsted user

    Parameters
    ----------
    request - we are expecting the following parameters:
        user_id : str
            the user that we will get heis last message and read it

    Returns
    -------
    HttpResponse
        a json object that the message that we pick to read

    """
    # get the user name from the request 
    user_id = request.GET.get('user_id')   

    # get user object from the user_id and check validation
    if RepresentsInt(user_id):
        user_Obj = User.objects.filter(id=user_id).first()
    else:
        return HttpResponse("user_id should be a integer number",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        
    if not user_Obj:
        return HttpResponseNotFound("user object does not exist")

    unreaded_msg_obj = Message.objects.filter(receiver=user_Obj,read=False).last()

    if not unreaded_msg_obj:
        # make the message as Ture and return it
        return HttpResponse("there is not unreaded messages for you")

    else:
        unreaded_msg_obj.read = True
        unreaded_msg_obj.save()    

    return HttpResponse(json.dumps(model_to_dict(unreaded_msg_obj)),content_type='application/json')

@api_view(['DELETE'])
@csrf_exempt
def delete_message(request,user_id=None,msg_id=None):

    """
    delete a message of a requested user

    Parameters
    ----------
    request - we are expecting the following parameters:
        user_id : str
            the user that we want to delete message from heis messages

    Returns
    -------
    HttpResponse

    """
    # get the user name and the message id from the request 
    user_id = request.GET.get('user_id')  
    msg_id =  request.GET.get('msg_id')  

    # check validation of the user_id and the msg_id and get the objects
    if RepresentsInt(user_id) and RepresentsInt(msg_id):

        user_obj = User.objects.filter(id=user_id).first()        
        msg_obj = Message.objects.filter(id=msg_id,visible=True).first()
    else:
        return HttpResponse("user_id and msg_obj should be a integer numbers",status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # check if msg_obj and user_obj exists
    if not msg_obj or not user_obj:
        return HttpResponseNotFound("message or user object does not exist")

        # if the sender or the receiver equal to the user name in the request, we delete the message.
    if msg_obj.sender == user_obj or msg_obj.receiver == user_obj:
        msg_obj.visible = False
        msg_obj.save()

        return HttpResponse("The message was deleted successfully")
    


def RepresentsInt(s):
    
    """
    get if the "s" is a integer value.

    Parameters
    ----------
    s - str object the we will get from the request

    Returns
    -------
    Boolean 

    """
    try: 
        int(s)
        return True
    except ValueError:
        return False
