from django.contrib import admin
from django.urls import path
from .views import findSomedayZodiacMessages
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('zodiac_all/<str:attribute1>&<str:luck_date>', findSomedayZodiacMessages.as_view(), name='findSomedayZodiacMessages')
]