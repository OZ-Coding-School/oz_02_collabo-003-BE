from django.urls import path
from .views import TodayMessage


urlpatterns = [
    path('today/<int:msg_id>/update/', TodayMessage.as_view(), name='updateTodayMessage'),

]