from django.urls import path
from .views import *

urlpatterns = [
    path('login/', AdminLogin.as_view(), name='AdminLogin'),
    path('signup/', AdminUsers.as_view(), name='AdminUsers'),
    path('msg/', EditLuckMessage.as_view(), name='EditLuckMessage'),
]