from django.urls import path
from .views import ZodiacMessage
from .views import TodayMessage

urlpatterns = [
    path('today/<int:msg_id>/update/', TodayMessage.as_view(), name='updateTodayMessage'),  
    path('zodiac/<int:msg_id>/update/', ZodiacMessage.as_view(), name='updateZodiacMessage'),
]