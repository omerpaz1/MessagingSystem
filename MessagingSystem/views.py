from MessagingSystem.models import Message
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseNotFound,HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
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
        try:
            sender_user_Obj = User.objects.filter(id=sender).first()
            receiver_user_Obj = User.objects.filter(id=receiver).first()        
        except:
            return HttpResponseNotFound("sender and reciver parameters should be a numbers")
        else:
            # check if the sender or the reciver objects does not exists
            if sender_user_Obj == None or receiver_user_Obj == None:
                return HttpResponseNotFound("sender or receiver user_id does not exist")

        #Create a new message and save in db
        the_current_date = date.today()
        try:
            msg = Message(sender=sender_user_Obj,receiver=receiver_user_Obj,message=msg,subject=subject,creation_date=str(the_current_date))
            msg.save()
        except:
            return HttpResponseServerError("there is an error when creating a new message obj")
        else:
            return HttpResponse("The message was created successfully")


@csrf_exempt
def get_all_messages(request,user_id=None):
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
    if request.method == 'GET':
        # List of messages of the requested user
        user_messages = []

        # get the user name from the request
        user_id = request.GET.get('user_id',None)

        # get user object from the user_id and check validation
        try:
            user_Obj = User.objects.filter(id=user_id).first()
        except:
            return HttpResponseNotFound("user_id should be a number")

        # get all the messages of the specific user that requsted 
        try:
            messages_for_specific_user = Message.objects.values().filter(receiver=user_Obj)
        except:
            return HttpResponseServerError("server got an error by try get data")
        
        # convert model object to a json
        return HttpResponse(json.dumps(list(messages_for_specific_user)),content_type='application/json')

@csrf_exempt
def get_all_unread_messages(request,user_id=None):
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
    if request.method == 'GET':
        # get the user name from the request 
        user_id = request.GET.get('user_id')

        # get user object from the user_id and check validation
        try:
            user_obj = User.objects.filter(id=user_id).first()
        except:
            return HttpResponseNotFound("user_id should be a number")

        if user_obj == None:
            return HttpResponseNotFound("user object does not exist")

        # get all the unreaded messages that sent to the requsted user
        return HttpResponse(json.dumps(list(Message.objects.values().filter(receiver=user_obj).filter(read=False))),content_type='application/json')

        

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
    if request.method == 'PUT':
        # get the user name from the request 
        user_id = request.GET.get('user_id')   

        # get user object from the user_id and check validation
        try:
            user_obj = User.objects.filter(id=user_id).first()
        except:
            return HttpResponseNotFound("user_id should be a number")
        else:
            if user_obj == None:
                return HttpResponseNotFound("user object does not exist")

        try:
            # pop one message from all the unreaded messages for the user
            unreaded_msg_obj = list(Message.objects.filter(receiver=user_obj).filter(read=False)).pop()
        except:
            return HttpResponseNotFound("There is not unreaded messages left")
        else:
            # make the message as Ture and return it
            unreaded_msg_obj.read = True
            unreaded_msg_obj.save()   

            return HttpResponse(json.dumps(model_to_dict(unreaded_msg_obj)),content_type='application/json')

@csrf_exempt
def delete_message(request,user_id=None,msg_id=None):

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

    if request.method == 'DELETE':

        # get the user name and the message id from the request 
        user_id = request.GET.get('user_id')  
        msg_id =  request.GET.get('msg_id')  

        # check validation of the user_id and the msg_id
        try:
            user_obj = User.objects.filter(id=user_id).first()        
            msg_obj = Message.objects.filter(id=msg_id).first()
        except:
            return HttpResponseNotFound("user_id and msg_id should be a numbers")

        # check if msg_obj and user_obj exists
        if msg_obj == None:
            return HttpResponseNotFound("message object does not exist")

        if user_obj == None:
            return HttpResponseNotFound("user object does not exist")

        # if the sender or the receiver equal to the user name in the request, we delete the message.
        if msg_obj.sender == user_obj or msg_obj.receiver == user_obj:
            try:
                msg_obj.delete()
            except:
                return HttpResponseServerError("can not delete this object")

            return HttpResponse("The message was deleted successfully")
    