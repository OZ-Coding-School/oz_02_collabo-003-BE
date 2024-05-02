from django.contrib import admin
from django.urls import path
from .views import StarMessage

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('zodiac/<int:msg_id>', StarMessage.as_view(), name='updateStarMessage'),

]