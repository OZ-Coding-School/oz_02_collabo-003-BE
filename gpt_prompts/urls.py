from django.urls import path
from .views import PromptToday #PromptTodayHistory, PromptZodiac, PromptZodiacHistory, PromptStar, PromptStarHistory, PromptMbti, PromptMbtiHistory

urlpatterns = [
    path('today/', PromptToday.as_view(), name='PromptToday'),
    # path('today/history/', PromptTodayHistory.as_view, name='PromptTodayHistory'),
    # path('zodiac/', PromptZodiac.as_view(), name='PromptZodiac'),
    # path('zodiac/history/', PromptZodiacHistory.as_view, name='PromptZodiacHistory'),
    # path('star/', PromptStar.as_view(), name='PromptStar'),
    # path('star/history/', PromptStarHistory.as_view, name='PromptStarHistory'),
    # path('mbti/', PromptMbti.as_view(), name='PromptMbti'),
    # path('mbti/history/', PromptMbtiHistory.as_view, name='PromptMbtiHistory'),
]