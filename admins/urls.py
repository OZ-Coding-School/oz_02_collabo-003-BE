from django.urls import path
from .views import EditLuckMessage, AdminUsers

urlpatterns = [
    path('msg/', EditLuckMessage.as_view(), name='EditLuckMessage'),
    path('signup/', AdminUsers.as_view(), name='AdminUsers'),
]