from django.urls import path
from django.conf.urls import url 


from . import views

urlpatterns = [
    path('new-message/', views.write_message),
    path('get-all-messages/', views.get_all_messages),

]