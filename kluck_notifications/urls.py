from django.urls import path
from .views import *

urlpatterns = [
    path('token/', PushToken.as_view(), name='PushToken'),
]