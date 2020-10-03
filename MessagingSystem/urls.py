from django.urls import path
from django.conf.urls import url 


from . import views

urlpatterns = [
    path('new-message', views.write_message),
    path('get-all-messages', views.get_all_messages),
    path('get-all-unread-messages', views.get_all_unread_messages),
    path('read-message', views.read_message),
    path('delete-message', views.delete_message),

]