from django.urls import path
from .views import *

urlpatterns = [
    path('today/', PromptToday.as_view(), name='PromptToday'),
    path('zodiac/', PromptZodiac.as_view(), name='PromptZodiac'),
    path('star/', PromptStar.as_view(), name='PromptStar'),
    path('mbti/', PromptMbti.as_view(), name='PromptMbti'),
    path('<str:category>/history', PromptHistory.as_view(), name='PromptHistory'),
]