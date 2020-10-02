from django.urls import path
from django.conf.urls import url


from . import views

urlpatterns = [
    path('new_message/', views.write_message),
    path('get_all_messages/', views.get_all_messages),

]