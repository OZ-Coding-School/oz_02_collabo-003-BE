from django.urls import path
from .views import *

urlpatterns = [
    path('mbti_all/', findTodayMbtiMessages.as_view(), name="findTodayMbtiMessages")
]