from django.urls import path
from .views import *


urlpatterns = [
    path('main/<str:user_birth>&<str:user_MBTI>', TodayLuck.as_view(), name='TodayLuck'),
    path('zodiac_all', FindTodayZodiacMessages.as_view(), name='FindTodayZodiacMessages'),
    path('star_all/', FindTodayStarMessages.as_view(), name='FindTodayStarMessages'),
    path('mbti_all/', FindTodayMbtiMessages.as_view(), name="FindTodayMbtiMessages"),

    # path('today/<str:luck_date>', findSomedayTodayMessages.as_view(), name='findSomedayTodayMessages'),
    # path('zodiac/<str:luck_date>', findSomedayZodiacMessages.as_view(), name='findSomedayZodiacMessages'),
    # path('star/<str:luck_date>', findSomedayStarMessages.as_view(), name='findSomedayStarMessages'),
    # path('mbti/<str:luck_date>', findSomedayMbtiMessages.as_view(), name="findTodayMbtiMessages"),
]