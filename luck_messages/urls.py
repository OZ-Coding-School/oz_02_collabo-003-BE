from django.urls import path
from .views import *


urlpatterns = [
    path('today/<str:luck_date>', findSomedayTodayMessages.as_view(), name='findSomedayTodayMessages'),  
    path('zodiac_all/<str:attribute1>', findTodayZodiacMessages.as_view(), name='findTodayZodiacMessages'),
    path('star_all/', findTodayStarMessages.as_view(), name='findTodayStarMessages'),
    path('mbti_all/', findTodayMbtiMessages.as_view(), name="findTodayMbtiMessages"),
    path('main/<str:user_birth>&<str:user_MBTI>', TodayLuck.as_view(), name='TodayLuck'),
]