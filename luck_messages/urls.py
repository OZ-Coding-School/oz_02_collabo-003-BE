from django.contrib import admin
from django.urls import path
from .views import findSomedayStarMessages

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('star_all/<str:luck_date>', findSomedayStarMessages.as_view(), name='findSomedayStarMessages'),

]