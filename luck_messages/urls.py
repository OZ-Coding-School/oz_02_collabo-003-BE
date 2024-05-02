from django.contrib import admin
from django.urls import path
from .views import TodayLuck, findTodayStarMessages, findTodayZodiacMessages

urlpatterns = [
    path('zodiac_all/<str:attribute1>', findTodayZodiacMessages.as_view(), name='findTodayZodiacMessages'),
    path('star_all/', findTodayStarMessages.as_view(), name='findTodayStarMessages'),
    path('main/<str:user_birth>&<str:user_MBTI>', TodayLuck.as_view(), name='TodayLuck'),
]
