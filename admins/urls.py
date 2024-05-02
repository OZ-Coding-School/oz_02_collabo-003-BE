from django.contrib import admin
from django.urls import path
from .views import TodayMessage

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('today/<int:msg_id>', TodayMessage.as_view(), name='updateTodayMessage'),

]