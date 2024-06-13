from django.urls import path
from .views import *

urlpatterns = [
    path('luck/', GptTodayLuck.as_view(), name='GptTodayLuck'),
    path('luck/terms/', GptLuckPeriod.as_view(), name='GptLuckPeriod'),
    # path('today/', GptToday.as_view(), name='GptToday'),
    # path('zodiac/', GptZodiac.as_view(), name='GptZodiac'),
    # path('star/', GptStar.as_view(), name='GptStar'),
    # path('mbti/', GptMbti.as_view(), name='GptMbti'),
]