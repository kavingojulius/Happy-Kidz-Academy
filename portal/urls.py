from django.urls import path
from .views import *

urlpatterns = [
    path('', portal, name='portal'),
    path('register/', register, name='register'),
    path('login/', log_in, name='log_in'),  
    path('logout/', logoutUser, name='logout')  
    
]