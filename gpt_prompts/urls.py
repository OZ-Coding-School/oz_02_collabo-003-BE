from django.urls import path
from .views import *

urlpatterns = [
    path('today/', PromptToday.as_view(), name='PromptToday'),
    path('zodiac/', PromptZodiac.as_view(), name='PromptZodiac'),
    path('star/', PromptStar.as_view(), name='PromptStar'),
    path('mbti/', PromptMbti.as_view(), name='PromptMbti'),
    path('<str:category>/history', PromptHistory.as_view(), name='PromptHistory'),
    path('gpt-star/', GptStar.as_view(), name='GptStar'),
    path('gpt-mbti/', GptMBTI.as_view(), name='GptMBTI'),
    # path('test/', Test.as_view(), name='GptApiTest'),
]