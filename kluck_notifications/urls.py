from django.urls import path
from .views import *

urlpatterns = [
    path('push-token/', PushToken.as_view(), name='PushToken'),
]