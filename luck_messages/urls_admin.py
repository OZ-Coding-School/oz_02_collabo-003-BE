from django.urls import path
from .views import *


urlpatterns = [
    # path('main/<str:user_birth>&<str:user_MBTI>', TodayLuck.as_view(), name='TodayLuck'),
    # path('zodiac_all/<str:attribute1>', findTodayZodiacMessages.as_view(), name='findTodayZodiacMessages'),
    # path('star_all/', findTodayStarMessages.as_view(), name='findTodayStarMessages'),
    # path('mbti_all/', findTodayMbtiMessages.as_view(), name="findTodayMbtiMessages"),
  
    path('today/<str:luck_date>', FindSomedayTodayMessages.as_view(), name='FindSomedayTodayMessages'),
    path('zodiac/<str:luck_date>', FindSomedayZodiacMessages.as_view(), name='FindSomedayZodiacMessages'),
    path('star/<str:luck_date>', FindSomedayStarMessages.as_view(), name='FindSomedayStarMessages'),
    path('mbti/<str:luck_date>', FindSomedayMbtiMessages.as_view(), name="FindTodayMbtiMessages"),
]