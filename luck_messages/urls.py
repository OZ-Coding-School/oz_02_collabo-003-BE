from django.urls import path
from .views import *


urlpatterns = [
    path('today/<str:luck_date>', findSomedayTodayMessages.as_view(), name='findSomedayTodayMessages'),  
    path('zodiac_all/<str:attribute1>', findTodayZodiacMessages.as_view(), name='findTodayZodiacMessages'),
    path('zodiac/<str:luck_date>', findSomedayZodiacMessages.as_view(), name='findSomedayZodiacMessages'),
    path('star_all/', findTodayStarMessages.as_view(), name='findTodayStarMessages'),
    path('star/<str:luck_date>', findSomedayStarMessages.as_view(), name='findSomedayStarMessages'),  
    path('mbti_all/', findTodayMbtiMessages.as_view(), name="findTodayMbtiMessages"),
    path('mbti/<str:luck_date>', findSomedayMbtiMessages.as_view(), name="findTodayMbtiMessages"),
    path('main/<str:user_birth>&<str:user_MBTI>', TodayLuck.as_view(), name='TodayLuck'),
]