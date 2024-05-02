
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import findTodayStarMessages, findTodayZodiacMessages

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('zodiac_all/<str:attribute1>', findTodayZodiacMessages.as_view(), name='findTodayZodiacMessages'),
    path('star_all/', findTodayStarMessages.as_view(), name='findTodayStarMessages')

]
