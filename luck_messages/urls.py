from django.contrib import admin
from django.urls import path
from .views import findTodayZodiacMessages
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('zodiac_all/<str:attribute1>', findTodayZodiacMessages.as_view(), name='findTodayZodiacMessages')
]