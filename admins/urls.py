from django.urls import path
from .views import *

urlpatterns = [
    path('login/', JWTLogin.as_view(), name='JWTlogin'),
    path('refresh/', JWTRefresh.as_view(), name='JWTRefresh'),
    path('', AdminUsers.as_view(), name='AdminUsers'),
    path('msg/', EditLuckMessage.as_view(), name='EditLuckMessage'),
    # path('signup/', AdminUsersSignup.as_view(), name='AdminUsersSignup'),
]