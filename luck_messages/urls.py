from django.contrib import admin
from django.urls import path
from .views import findSomedayTodayMessages
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('today/<str:luck_date>', findSomedayTodayMessages.as_view(), name='findSomedayTodayMessages'),

]