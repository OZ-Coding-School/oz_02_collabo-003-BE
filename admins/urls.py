from django.urls import path
from .views import EditLuckMessage

urlpatterns = [
    path('msg/', EditLuckMessage.as_view(), name='EditLuckMessage'),
]