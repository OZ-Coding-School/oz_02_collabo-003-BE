
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import findTodayStarMessages

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('star_all/', findTodayStarMessages.as_view(), name='findTodayStarMessages')

]
