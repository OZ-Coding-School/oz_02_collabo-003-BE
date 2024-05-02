from django.urls import path
from .views import TodayLuck

urlpatterns = [
    path('', TodayLuck.as_view(), name='TodayLuck'),
]