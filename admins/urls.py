from django.urls import path
from .views import EditLuckMessage

urlpatterns = [
    path('msg/<int:msg_id>/update/', EditLuckMessage.as_view(), name='EditLuckMessage'),
]