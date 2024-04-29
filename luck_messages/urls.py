from django.urls import path
from .views import *

urlpatterns = [
    path('zodiac_all/<str:attribute1>', findZodiacMessages, name='findZodiacMessages'),
    path('star_all/', findStarMessages, name='findStarMessages'),
    path('mbti_all/', findMbtiMessages , name="findMbtiMessages")
]