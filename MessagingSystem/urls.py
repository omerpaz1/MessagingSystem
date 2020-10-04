from django.urls import path
from django.conf.urls import url 


from . import views

urlpatterns = [
    path('api/new-message', views.write_message),
    path('api/get-all-messages', views.get_all_messages),
    path('api/get-all-unread-messages', views.get_all_unread_messages),
    path('api/read-message', views.read_message),
    path('api/delete-message', views.delete_message),

]