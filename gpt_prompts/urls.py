from django.urls import path
from .views import *

urlpatterns = [
    path('<str:category>/', PromptIndividual.as_view(), name='Prompt'),
    path('<str:category>/history/<int:page>/', PromptHistory.as_view(), name='PromptHistory'),
]