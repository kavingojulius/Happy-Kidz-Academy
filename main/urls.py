from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='home'),
    path('about', about_us, name='about_us'),
    path('visionmision', visionmission, name='visionmission'),
    path('news', news, name='news'),
    path('events', events, name='events'),
    path('contact', contact_us, name='contact_us'),
    path('gallery', gallery, name='gallery'),
    path('downloads', downloads ,name='downloads'),
]