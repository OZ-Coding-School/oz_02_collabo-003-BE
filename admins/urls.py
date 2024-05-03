from django.urls import path
from .views import *

urlpatterns = [
    path('login/', AdminLogin.as_view(), name='AdminLogin'),
    path('', AdminUsers.as_view(), name='AdminUsers'),
    path('signup/', AdminUsersSignup.as_view(), name='AdminUsersSignup'),
    path('msg/', EditLuckMessage.as_view(), name='EditLuckMessage'),
]