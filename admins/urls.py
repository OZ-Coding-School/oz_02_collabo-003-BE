from django.urls import path
from .views import EditLuckMessage, AdminUsersSignup, AdminUsers

urlpatterns = [
    path('msg/', EditLuckMessage.as_view(), name='EditLuckMessage'),
    path('', AdminUsers.as_view(), name='AdminUsers'),
    path('signup/', AdminUsersSignup.as_view(), name='AdminUsersSignup'),
]