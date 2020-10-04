from django import forms


class MessageForm(forms.Form):
    # this from represent a new message
    sender = forms.IntegerField()
    receiver = forms.IntegerField()
    msg = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=50)


class UserID(forms.Form):
    # this form is form check if the user_id that send is type of int
    user_id = forms.IntegerField()

class MessageID(forms.Form):
    # this form is form check if the msg_id that send is type of int
    msg_id = forms.IntegerField()
