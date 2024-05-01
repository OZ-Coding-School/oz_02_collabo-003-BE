from django.contrib import admin
from django.urls import path
from .views import findSomedayMbtiMessages

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('mbti_all/<str:luck_date>', findSomedayMbtiMessages.as_view(), name="findTodayMbtiMessages")
]
