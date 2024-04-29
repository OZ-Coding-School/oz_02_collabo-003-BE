from django.urls import path
from .views import *

urlpatterns = [
    path('zodiac_all/<str:attribute1>', findZodiacMessages.as_view(), name='findZodiacMessages'),
    path('star_all/', findStarMessages.as_view(), name='findStarMessages'),
    path('mbti_all/', findMbtiMessages.as_view(), name="findMbtiMessages")
]