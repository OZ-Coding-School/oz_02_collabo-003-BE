from django.urls import path
from .views import TodayLuck

urlpatterns = [
    path('<str:user_birth>&<str:user_MBTI>', TodayLuck.as_view(), name='TodayLuck'),
]